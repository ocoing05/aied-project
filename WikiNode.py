"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia
import yake

class WikiNode:
    def __init__(self, title, prevNode):
        self.title = title

        self.page = wikipedia.page(self.title)
        # these would be like children in the tree
        self.linkedPages = self.page.links

        # parent in the tree ? ... the article they read to get this suggestion
        # not sure if this is needed
        self.prevNode = prevNode

        self.keyWords = self.getKeyWords()

    def getURL(self):
        return "https://en.wikipedia.org/wiki/" + self.title

    def getCategories(self):
        return self.page.categories

    def getContent(self):
        return self.page.content

    def getSummary(self, sentences):
        self.summary = wikipedia.summary(self.title, sentences)

    def getKeyWords(self):
        text = self.getContent()
        # use NLP to get key words for the article which can be used by recommender
        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9 # set to 0.1 to prohibit repeated words in key words
        numOfKeywords = 20
        extractor = yake.KeywordExtractor(
            lan=language, 
            n=max_ngram_size, 
            dedupLim=deduplication_threshold, 
            top=numOfKeywords, 
            features=None)

        return extractor.extract_keywords(text)