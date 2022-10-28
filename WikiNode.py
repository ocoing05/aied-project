"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia

class WikiNode:
    def __init__(self, title, prevNode):
        self.title = title

        self.page = wikipedia.page(self.title)
        # these would be like children in the tree ?
        self.linkedPages = self.page.links

        # parent in the tree ? ... the article they read to get this suggestion
        # not sure if this is needed
        self.prevNode = prevNode

        self.keyWords = self.getKeyWords()

    def getURL(self):
        return "https://en.wikipedia.org/wiki/" + self.title

    def getCategories(self):
        return wikipedia.page(self.title).categories

    def getContent(self):
        return wikipedia.page(self.title).content

    def getSummary(self, sentences):
        self.summary = wikipedia.summary(self.title, sentences)

    def getKeyWords(self):
        text = self.getContent()
        # use NLP to get key words for the article which can be used by recommender
        pass