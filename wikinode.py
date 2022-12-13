"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""
import yake
from sense2vec import Sense2Vec
import spacy
from mediawiki import MediaWiki


class WikiNode:

    def __init__(self, title, nlp, wiki, prevNode = None, domainNode=False):
        self.domainNode = domainNode

        self.wikipedia = wiki
        self.nlp = nlp

        self.title = title
        suggestedTitle = self.wikipedia.suggest(title)
        if suggestedTitle:
            self.page = self.wikipedia.page(suggestedTitle)
            self.title = suggestedTitle
        self.keywords = self.getKeyWords()
        self.prevNode = prevNode # the article they read previously to get this suggestion; None if interestKeyword
        self.linkedPages = self.page.links
        #self.linkedPages = self._sortLinks(self.page.links) # Dictionary of links (keys) sorted by highest avg similarity to self.keywords

        if domainNode: # 
            self.wikipedia.categorytree(self.title, 2)
            self.parents = [] 
            self.children = []
            self.siblings = []
            # knownPeers are articles outside the family (not in parents, children or siblings) 
            # with high maxVal of (titleSim, keywordSim, linksSim) "wormholes" to other domains.
            # Find knownPeers by running s2v_most_similar on title, keep 
            self.knownPeers = [] 

    def setPrevNode(self, prevNode):
        self.prevNode = prevNode

    def _sortLinks(self, linkList):
        """Returns a dictionary of page links sorted by highest average similarity to self.keywords."""
        linksPrio = {}
        for link in linkList:
            totalSim = 0
            linkDoc = self.nlp(link)
            for kw in self.keywords:
                kwDoc = self.nlp(kw)
                if len(linkDoc._.s2v_phrases) != 1 or len(kwDoc._.s2v_phrases) != 1:
                    # adds the standard spacy similarity between link and keyword to totalSim
                    totalSim += linkDoc.similarity(kwDoc) 
                else:
                    # adds the sense2vec similarity between the link token and the keyword token if both in sense2vec vocabulary
                    totalSim += linkDoc._.phrases[0]._.s2v_similarity(kwDoc._.s2v_phrases[0])
            linksPrio[link] = totalSim/len(self.keywords)

        return dict(sorted(linksPrio.items(), key=lambda item: item[1]))

    def getLinkedPageTitles(self) -> dict:
        return self.linkedPages

    def getTitle(self) -> str:
        return self.title

    def toString(self) -> str:
        return self.title

    def getURL(self):
        return "https://en.wikipedia.org/wiki/" + self.title

    def getCategories(self):
        return self.page.categories

    def getContent(self):
        return self.page.content

    # returns opening sentences of article, before the sections begin
    def getSummary(self, sentences = None):
        if sentences:
            return self.wikipedia.summary(self.title, sentences)
        else:
            return self.wikipedia.summary(self.title)


    def getKeyWords(self):
        text = self.getContent()
        language = "en"
        max_ngram_size = 5 # only 1-gram so that spacy can work
        deduplication_threshold = 0.1# set to 0.1 to prohibit repeated words in key words
        numOfKeywords = 30
        extractor = yake.KeywordExtractor(lan=language,
                                            n=max_ngram_size,
                                            dedupLim=deduplication_threshold,
                                            top=numOfKeywords,
                                            features=None)
        tuples = extractor.extract_keywords(text)
        keywords = [i[0] for i in tuples]
        self.keywords = keywords
        return keywords

    def getSectionTitles(self):
        return self.page.sections
    
    def getSection(self, section):
        if section not in self.page.sections:
            return ("No section titled ", section)
        else:
            content = self.page.section(section)
            if len(content) > 0:
                return content
            else:
                return "Empty section"

# if __name__ == "__main__":

#     nlp = spacy.load('en_core_web_lg')
#     s2v = nlp.add_pipe("sense2vec")
#     s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
#     wiki = MediaWiki()
#     wiki.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone_qharring@macalester.edu' # MediaWiki etiquette

#     test = WikiNode("Dinosaurs", nlp, wiki)
#     print(test.getSummary())

#     print("LINKS")
#     print(test.linkedPages)

#     print("KEYWORDS")
#     keywords = test.getKeyWords()
#     print(keywords)

    # print("BOTH LINK AND KEYWORD")
    # print(set(test.linkedPages) & set(keywords))

    # print("SECTION TITLES")
    # print(test.getSectionTitles())

    # print("CONTENTS OF SECTION TITLED: '", test.getSectionTitles()[0], "'")
    # print(test.getSection(test.getSectionTitles()[0]))