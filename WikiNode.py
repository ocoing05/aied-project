"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia
import yake
from mediawiki import MediaWiki

class WikiNode:

    def __init__(self, title, prevNode = None, domainNode=False):

        self.domainNode = domainNode

        self.wikipedia = MediaWiki()
        self.wikipedia.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone_qharring@macalester.edu' # MediaWiki etiquette

        self.title = title

        # the article they read previously to get this suggestion
        self.prevNode = prevNode

        # Should allow new wikiNode object to be created without DisabmiguationError
        suggestedTitle = self.wikipedia.suggest(title)
        if suggestedTitle:
            self.page = self.wikipedia.page(suggestedTitle)
            self.title = suggestedTitle
        self.linkedPages = self.page.links
        self.keywords = []

        if domainNode:
            self.parents = [] 
            self.children = []
            self.siblings = []
            # knownPeers are articles outside the family (not in parents, children or siblings) 
            # with high maxVal of (titleSim, keywordSim, linksSim) "wormholes" to other domains.
            # Find knownPeers by running s2v_most_similar on title, keep 
            self.knownPeers = [] 

    def getLinkedPageTitles(self):
        return self.linkedPages

    def getTitle(self):
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
        if (len(self.keywords) > 0):
            return self.keywords
        else:
            text = self.getContent()
            language = "en"
            max_ngram_size = 1 # only 1-gram so that spacy can work
            deduplication_threshold = 0.1 # set to 0.1 to prohibit repeated words in key words
            numOfKeywords = 100
            extractor = yake.KeywordExtractor(
                lan=language, 
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

if __name__ == "__main__":

    test = WikiNode("Dinosaurs")
    print(test.getSummary())

    print("LINKS")
    print(test.linkedPages)

    print("KEYWORDS")
    keywords = test.getKeyWords()
    print(keywords)

    print("BOTH LINK AND KEYWORD")
    print(set(test.linkedPages) & set(keywords))

    print("SECTION TITLES")
    print(test.getSectionTitles())

    print("CONTENTS OF SECTION TITLED: '", test.getSectionTitles()[0], "'")
    print(test.getSection(test.getSectionTitles()[0]))