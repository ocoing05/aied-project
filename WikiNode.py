"""
Represents a node in the graph of Wikipedia.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia

class WikiNode:
    def __init__(self, title):
        self.title = title
        self.url = "https://en.wikipedia.org/wiki/" + title
        
        page = wikipedia.page(title)
        self.summary = wikipedia.summary(title, sentences = 3)
        self.categories = page.categories
        self.linkedPages = page.links
        self.content = page.content

        # use NLP to return list of most important words/topics ?
        # to be used by recommender for identifying interests 
        # and choosing most relevant next article to choose
        self.keyWords = []

    # do we need getter functions or can we access the variables directly ??