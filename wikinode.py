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
import spacy
from mediawiki import MediaWiki
from sense2vec import Sense2Vec


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
        # text = self.getContent()
        # language = "en"
        # max_ngram_size = 1 # only 1-gram so that spacy can work
        # deduplication_threshold = 0.5 # set to 0.1 to prohibit repeated words in key words
        # numOfKeywords = 50
        # extractor = yake.KeywordExtractor(lan=language,
        #                                     n=max_ngram_size,
        #                                     dedupLim=deduplication_threshold,
        #                                     top=numOfKeywords,
        #                                     features=None)
        # tuples = extractor.extract_keywords(text)
        # keywords = [i[0] for i in tuples]
        # self.keywords = keywords
        # self.sortKeywords()
        # self.linkedPages = self._sortLinks(self.page.links) # Dictionary of links (keys) sorted by highest avg similarity to self.keywords
        # FOR MVP: 
        # TODO: add mvp conditional... is sortKeywords() still needed at all
        self.linkedPages = self.page.links
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
        # FOR MVP: # TODO: add mvp conditional 
        return self.linkedPages

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

    #   1. Load:
    #       - spacy natural language processor object
    #       - sense2vec pipe object (for spacy pipeline) 
    #       - mediawiki MediaWiki wikipedia object (wikipedia is default)
    nlp = spacy.load('en_core_web_lg')
    s2vPipe = nlp.add_pipe("sense2vec")
    s2vPipe.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
    s2v = Sense2Vec().from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
    wiki = MediaWiki()
    wiki.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone_qharring@macalester.edu' # MediaWiki etiquette

    # testN1 = WikiNode("Dinosaurs", nlp, wiki)
    # testN2
    # testN3
    # testN4
    # testN5
    # testN6


    #   2. Build yake keyword extractor object
    language = "en"
    max_ngram_size = 1 # only 1-gram so that spacy can work
    deduplication_threshold = 0.5 # set to 0.1 to prohibit repeated words in key words
    numOfKeywords = 20
    extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

    #   3. Test MediaWiki and Spacy:
    #       - Get page from MediaWiki object
    #       - Make spacy nlp 'doc' of page title
    #       - Set last token in title as pageToken
    #       - Print 
    title = wiki.suggest("posthumanism")
    page = wiki.page(title)
    pageDoc = nlp(title)
    for token in pageDoc:
        pageToken = token

    print("Title : " + title + ",    pageToken : " + pageToken.text)
    print("\n")
    print("\nContent : " + page.content)
    print("\n")
    print("\nSummary : " + page.summary)
    print("\n")

    #   4. Extract keywords from content and summary with yake extractor, Print with spacy similarity val
    contentKWT = extractor.extract_keywords(page.content)
    yakeKeyWords_FromContent = [i[0] for i in contentKWT]
    summaryKWT = extractor.extract_keywords(page.summary)
    yakeKeyWords_FromSummary = [i[0] for i in summaryKWT]
    
    print("\nContent Keywords : Spacy Similarity Values : S2V Similarity Values")
    for i in range(0, len(yakeKeyWords_FromContent)):
        kw = yakeKeyWords_FromContent[i]
        kwDoc = nlp(kw)
        sim = kwDoc[0].similarity(pageToken)
        print(kw + "   " + sim)

    print("\n")

    print("\nSummary Keywords : Spacy Similarity Values : S2V Similarity Values")
    for i in range(0, len(yakeKeyWords_FromContent)):
        kw = yakeKeyWords_FromContent[i]
        kwDoc = nlp(kw)
        sim = kwDoc[0].similarity(pageToken)
        print(kw + "   " + sim)
    [print(yakeKeyWords_FromSummary[i]) for i in range(0, len(yakeKeyWords_FromSummary))]

    print("\n")

    print("\nContent Keyword Spacy NLP Values (no sense2vec component)")
    for kw in yakeKeyWords_FromContent:
        kwDoc = nlp(kw)
        for token in kwDoc:
            print(token.similarity(pageToken))

    print("\n")

    print("\nSummary Keyword Spacy NLP Values (no sense2vec component)")

    for kw in yakeKeyWords_FromSummary:
        kwDoc = nlp(kw)
        for token in kwDoc:
            print(token.similarity(pageToken))

    # print("KEYWORDS")
    # keywords = testN1.getKeyWords()
    # print(keywords)

    # print("LINKS")
    # print(testN1.getLinkedPageTitles(20))

    # print("BOTH LINK AND KEYWORD")
    # print(set(test.linkedPages) & set(keywords))

    # print("SECTION TITLES")
    # print(test.getSectionTitles())

    # print("CONTENTS OF SECTION TITLED: '", test.getSectionTitles()[0], "'")
    # print(test.getSection(test.getSectionTitles()[0]))
    pass