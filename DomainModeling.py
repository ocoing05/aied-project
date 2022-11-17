"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia
import yake
import spacy
from sense2vec import Sense2Vec
from FoxQueue import PriorityQueue

# from owlready2 import *

class KnowledgeGraph:

    def __init__(self) -> None:

        self.visited = PriorityQueue()
        self.fringe = PriorityQueue()

    def update(self, wikiNode) -> None:

        self._updateVisited(wikiNode)
        # self.visited[wikiNode] = [listOfSpecialKeywords]
        # if self.fringe contains wikiNode, remove it
        # add wikiNode.fringeSet to self.fringe
        pass

    def getExplored(self) -> set:

        return self.visited.keys()

    def updateKey(key) -> None:

        # set 

        pass

    def _updateVisited(self, wikiNode) -> None:

        if not wikiNode.isVisited():
            wikiNode.setAsVisited()
        else:
            (elapsedTime, erosionTime, numVisits, numTests) = self.visited[wikiNode]
            numVisits += 1
            self.visited[wikiNode] = (elapsedTime, erosionTime, numVisits, numTests)

        self.visited[wikiNode] = []

        pass

class WikiNode:

    def __init__(self, title, prevNode = None, visited=False):

        self.elapsedTime = 0
        self.erodedTime = 0
        self.numVisits = 0
        self.numSectionTests = 0

        self.title = title

        self.visited  = visited 

        self.page = wikipedia.page(self.title, auto_suggest=False)
        # these would be like children in the tree
        self.linkedPages = self.page.links

        # parent in the tree ? ... the article they read to get this suggestion
        # not sure if this is needed
        self.prevNode = prevNode
        self.parentNode = self._getParent()
        self.siblings = [] # 
        self.peers = [] # 

        self.keyWords = self.getKeyWords()

    def getURL(self):
        return "https://en.wikipedia.org/wiki/" + self.title

    def getCategories(self):
        return self.page.categories

    def _getParent(self):
        """Queries the wikiNode title in the noncyclic Wikipedia knowledge graph,
        and returns the one node that is the parent of this wikiNode."""
        pass

    def getContent(self):
        return self.page.content

    def getSummary(self, sentences):
        self.summary = wikipedia.summary(self.title, sentences)

    def getSectionTitles(self):
        return self.page.sections

    def getKeyWords(self):
        text = self.getContent()
        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9 # set to 0.1 to prohibit repeated words in key words
        numOfKeywords = 100
        extractor = yake.KeywordExtractor(
            lan=language, 
            n=max_ngram_size, 
            dedupLim=deduplication_threshold, 
            top=numOfKeywords, 
            features=None)
        tuples = extractor.extract_keywords(text)
        keywords = [i[0] for i in tuples]

        return keywords

    def setAsVisited(self) -> None:
        self.numVisits = 1
        self.visited = True

    def isVisited(self) -> bool:
        
        return self.visited

    def updateStats(statDict) -> None:

        
        pass


if __name__ == "__main__":

    # graph? : https://networkx.org/documentation/stable/tutorial.html

    # onto = get_ontology("file:///Users/quentinharrington/Desktop/COMP484/aied-project/wiki_cats_full_non_cyclic_v1.owl")
    # onto.load()
    # ontoList = list(onto.classes())
    # print(ontoList)

    # TESTING / EXAMPLES

    nlp = spacy.load('en_core_web_lg')
    s2v = nlp.add_pipe("sense2vec")
    s2v.from_disk("/path/to/s2v_reddit_2015_md")


    doc1 = nlp("Alien")
    doc2 = nlp("Extraterrestrial")

    print(doc1.similarity(doc2))

    # test = WikiNode("Aliens")

    # print("LINKS")
    # print(test.linkedPages)

    # print("KEYWORDS")
    # keywords = test.getKeyWords()
    # print(keywords)

    # print("BOTH LINK AND KEYWORD")
    # print(set(test.linkedPages) & set(keywords))

    # print("SECTION TITLES")
    # print(test.getSectionTitles())
