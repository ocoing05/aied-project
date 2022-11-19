"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

# import wikipedia
import yake
from mediawiki import MediaWiki

class WikiNode:

    def __init__(self, title, prevNode = None):

        self.wikipedia = MediaWiki()
        self.wikipedia.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone' # MediaWiki ettiquete

        self.title = title

        # the article they read previously to get this suggestion
        self.prevNode = prevNode

        self.page = self.wikipedia.page(title)
        self.linkedPages = self.page.links
        self.keywords = []

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
            self.keywords = keywords
            return keywords

    def getSectionTitles(self):
        return self.page.sections
    
    # moved out of init method bc we don't want to generate this upon all node initializations, 
    # since some nodes may be created for fringe but never read, so all this data doesn't need to be found/saved in that case
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