from FoxQueue import PriorityQueue
from WikiNode import WikiNode
import networkx as nx

class ProgressGraph:

    def __init__(self) -> None:
        self.fringe = PriorityQueue() # unopened WikiNodes adjacent to progressGraph, sorted by potential interest
        self.graph = nx.Graph() # graph of already read articles and edges between them represent from what link they were discovered

        # we may not need this as a priority queue since the graph is already holding all of the visited nodes & we could add any stats needed to there?
        self.visited = PriorityQueue() 

    # i don't think we need this since all update methods are called from student object but keeping it for rn just in case ?
    # def update(self, wikiNode) -> None:
    #     self._updateVisited(wikiNode)
    #     # self.visited[wikiNode] = [listOfSpecialKeywords]
    #     # if self.fringe contains wikiNode, remove it
    #     # add wikiNode.fringeSet to self.fringe
    #     pass

    def getVisited(self) -> set: # alternatively, this would also be all the nodes in the graph
        return self.visited.keys()

    def _updateVisited(self, wikiNode) -> None:
        if not wikiNode.isVisited():
            wikiNode.setAsVisited()
        else:
            (elapsedTime, erosionTime, numVisits, numTests) = self.visited[wikiNode]
            numVisits += 1
            self.visited[wikiNode] = (elapsedTime, erosionTime, numVisits, numTests)
        self.visited[wikiNode] = []
        pass

    def updateGraph(self, node):
        '''Called by the student model update() method after a student reads a new article. 
        Adds node to graph.'''
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)

    def updateFringe(self, node, studentInterests):
        '''Called by the student model update() method after a student reads a new article.
        Updates fringe with linked articles from node they just read. Ranked based on student interests.'''
        # TODO: make this method work based on keyword comparison with spacy

        # past pseudocode for reference ...

        #     for key in self.fringe:
        #         words = key.getKeywords()
        #         interestCounter = 0
        #         for word in words:
        #             # if (word is in self.studentModel.interestKeywords):
        #                 # interestCounter += self.studentModel.interestKeywords[word]
        #         potentialInterest = interestCounter / len(words)
        #         self.fringe[key] = potentialInterest

        # something like the lines below, but ranked based on interests / NLP / key words ?
        # for pg in node.linkedPages:
            # studentFringe.add(WikiNode(pg, node.title)) # should add the node object to keep track of parent node, not just the title
        pass