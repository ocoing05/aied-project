"""
COMP 484 - Introduction to Artificial Intelligence, Fall 2022
Term Project - AI in Education: FreeLearner, presented 12/16/2022
Ingrid O'Connor and Quentin Harrington

This file: wikinode.py
    Represents a node in the graph of Wikipedia articles.
    Includes title, url, summary, categories, linked pages, and content of page.
    Uses NLP on content to determine key words, which are used by recommender system.
"""
import yake
from mediawiki import MediaWiki


class WikiNode:

    def __init__(self, title, nlp, wiki, prevNode = None, domainNode=False):

        # Instantiate wikiNode attributes
        self.title = title
        self.page = None
        self.keywords = []
        self.linkedPages = {} 
        self.prevNode = prevNode # the article they read previously to get this suggestion; None if interestKeyword
        self.domainNode = domainNode # If node is in domain model
        self.wikipedia = wiki
        self.nlp = nlp
        self.hasS2V = True

        # From given title, find most appropriate wikipedia page
        suggestedTitle = self.wikipedia.suggest(title)
        # print("Desired Page: ", title, "\nPage Received: ", suggestedTitle)
        if suggestedTitle:
            self.page = self.wikipedia.page(suggestedTitle)
            self.title = suggestedTitle

        # Check if sense2vec is in pipeline
        try:
            nlp("test")._.in_s2v
        except AttributeError:
            self.hasS2V = False

        # Extract and set top 30 keywords with yake, sort links by similarity to keywords
        # -------------------------------------------------------------------------------
        text = self.getContent()
        language = "en"
        max_ngram_size = 1 # only 1-gram so that spacy can work
        deduplication_threshold = 0.5 # set to 0.1 to prohibit repeated words in key words
        numOfKeywords = 50
        extractor = yake.KeywordExtractor(lan=language,
                                            n=max_ngram_size,
                                            dedupLim=deduplication_threshold,
                                            top=numOfKeywords,
                                            features=None)
        tuples = extractor.extract_keywords(text)
        keywords = [i[0] for i in tuples]
        self.keywords = keywords
        self.sortKeywords()
        self.linkedPages = self._sortLinks(self.page.links) # Dictionary of links (keys) sorted by highest avg similarity to self.keywords
        # -------------------------------------------------------------------------------        

        # If wikiNode is in the domain model, set domain hierarchy details
        if domainNode: # 
            self.catTree = self.wikipedia.categorytree(self.title, 1)
            self.parents = [] 
            self.children = []
            self.siblings = []
            # knownPeers are articles outside the family (not in parents, children or siblings) 
            # with high maxVal of (titleSim, keywordSim, linksSim) "wormholes" to other domains.
            # Find knownPeers by running s2v_most_similar on title, keep 
            self.knownPeers = [] 
        
        print("node initiated.")

    def sortKeywords(self):
        nodeDoc = self.nlp(self.title)
        kwDict = {}
        for kw in self.keywords:
            kwDoc = self.nlp(kw)
            if not kwDoc.has_vector:
                continue
            
            if self.hasS2V and nodeDoc[0:]._.in_s2v and kwDoc[0:]._.in_s2v:
                # adds the sense2vec similarity between the link token and the keyword token if both in sense2vec vocabulary
                kwDict.update({kw:nodeDoc[0:]._.s2v_similarity(kwDoc[0:])})
            else:
                kwDict.update({kw:nodeDoc.similarity(kwDoc)})
        self.keywords = list(dict(sorted(kwDict.items(), key=lambda x:x[1], reverse=True)).keys())

    def setPrevNode(self, prevNode):
        self.prevNode = prevNode

    def _sortLinks(self, linkList):
        """Returns a dictionary of page links sorted by highest average similarity to self.keywords."""
        linksPrio = {}

        for link in linkList:
            totalSim = 0
            linkDoc = self.nlp(link)
            if not linkDoc.has_vector:
                continue
            # print("Link: ", linkDoc)
            for kw in self.keywords:
                kwDoc = self.nlp(kw)
                if not kwDoc.has_vector:
                    continue
                # print("\tKeyword: ", kwDoc)
                if self.hasS2V and linkDoc[0:]._.in_s2v and kwDoc[0:]._.in_s2v:
                    # adds the sense2vec similarity between the link token and the keyword token if both in sense2vec vocabulary
                    sim = linkDoc[0:]._.s2v_similarity(kwDoc[0:])
                    # print("\tSimilarity: ", sim)
                    totalSim += sim
                else:
                    # adds the standard spacy similarity between link and keyword to totalSim
                    sim = linkDoc.similarity(kwDoc) 
                    # print("\tSimilarity: ", sim)
                    totalSim += sim
                                        
            linksPrio[link] = totalSim/len(self.keywords)

        return dict(sorted(linksPrio.items(), key=lambda x:x[1], reverse=True))

    def getLinkedPageTitles(self, numLinks=None) -> list:

        linkTitles = list(self.linkedPages.keys())
        if numLinks:
            shortList = []
            for x in range(0, numLinks-1):
                shortList.append(linkTitles[x])
            linkTitles = shortList

        return linkTitles

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
        return self.keywords

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

if __name__ == "__main__":
    pass
    # nlp = spacy.load('en_core_web_lg')
    # s2v = nlp.add_pipe("sense2vec")
    # s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
    # wiki = MediaWiki()
    # wiki.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone_qharring@macalester.edu' # MediaWiki etiquette

    # test = WikiNode("Dinosaurs", nlp, wiki)

    # print("KEYWORDS")
    # keywords = test.getKeyWords()
    # print(keywords)

    # print("LINKS")
    # print(test.getLinkedPageTitles(20))

    # print("BOTH LINK AND KEYWORD")
    # print(set(test.linkedPages) & set(keywords))

    # print("SECTION TITLES")
    # print(test.getSectionTitles())

    # print("CONTENTS OF SECTION TITLED: '", test.getSectionTitles()[0], "'")
    # print(test.getSection(test.getSectionTitles()[0]))