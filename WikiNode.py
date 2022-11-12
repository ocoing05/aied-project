"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

# pip3 install wikipedia_sections

import wikipedia
import yake

class WikiNode:
    def __init__(self, title, prevNode = None):
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

    # returns opening sentences of article, before the sections begin
    def getSummary(self, sentences):
        self.summary = wikipedia.summary(self.title, sentences)

    def getSectionTitles(self):
        return self.page.sections

    def getKeyWords(self):
        text = self.getContent()
        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9 # set to 0.1 to prohibit repeated words in key words
        numOfKeywords = 50
        extractor = yake.KeywordExtractor(
            lan=language, 
            n=max_ngram_size, 
            dedupLim=deduplication_threshold, 
            top=numOfKeywords, 
            features=None)
        tuples = extractor.extract_keywords(text)
        keywords = [i[0] for i in tuples]

        return keywords
    
    # returns dictionary containing contents of each section... api ot working right rn
    # def getSectionsContents(self):
    #     sectionContents = {}
    #     for section in self.page.sections:
    #         content = self.page.section(section)
    #         if len(content) > 0: # non-empty section
    #             sectionContents[section] = self.page.section(section)
    #     return sectionContents

# TESTING / EXAMPLES

# test = WikiNode("Dinosaurs")
# print(test.getSummary(4))

# print("LINKS")
# print(test.linkedPages)

# print("KEYWORDS")
# keywords = test.getKeyWords()
# print(keywords)

# print("BOTH LINK AND KEYWORD")
# print(set(test.linkedPages) & set(keywords))

# print("SECTION TITLES")
# print(test.getSectionTitles())