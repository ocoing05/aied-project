"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia
import yake
import spacy
from sense2vec import Sense2Vec
import networkx as nx
from FoxQueue import PriorityQueue
from WikiNode import WikiNode

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

    # called after a student reads a new article
    def updateGraph(self, node): # is this what update is supposed to be?
        if not self.graph: # is the student does not have a graph yet/hasn't read any articles yet
            self.graph = nx.Graph()
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)
        # TODO: update fringe queue
        # something like the lines below, but ranked based on interests / NLP / key words ?
        # for pg in node.linkedPages:
            # studentFringe.add(WikiNode(pg, node.title)) # should add the node object to keep track of parent node, not just the title
        # TODO: update student interests

if __name__ == "__main__":

    onto = get_ontology("file:///Users/quentinharrington/Desktop/COMP484/aied-project/wiki_cats_full_non_cyclic_v1.owl")
    onto.load()
    ontoList = list(onto.classes())
    print(ontoList)
    
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
