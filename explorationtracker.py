import networkx as nx
import spacy
import re

from FoxQueue import PriorityQueue
from wikinode import WikiNode

nlp = spacy.load('en_core_web_lg')

class ExplorationTracker:

    def __init__(self, initialInterests) -> None:
        self.fringe = PriorityQueue() # unopened WikiNodes adjacent to progressGraph, sorted by potential interest
        self.graph = nx.Graph() # graph of already read articles and edges between them represent from what link they were discovered

        # we may not need this as a priority queue since the graph is already holding all of the visited nodes & we could add any stats needed to there?
        self.visited = PriorityQueue() 
        
        for i in initialInterests:
            self.fringe.insert(WikiNode(i), 0.0)
            # self.updateFringe(i, initialInterests)

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
        # TODO: before adding to fringe, make sure it doesn't exist in explored graph
        lp = node.linkedPages
        kw = node.getKeyWords()
        for pg in set(lp) & set(kw): # words that exist as both linked pages and key words
            print(pg)
            pg = re.sub(r'\W+', ' ', pg) # replaces all non-alphanumeric/underscore characters w space
            if len(pg.strip().split(" ")) > 1: # more than 1-gram phrases won't be done properly with the getPriority() logic rn
               # TODO: logic for n-gram pages?
               # print("n-gram")
               continue
            priority = self.getPriority(pg, studentInterests)
            # print(priority)
            try:
                node = WikiNode(pg, node.title)
            except:
                continue
            self.fringe.insert(node, priority)
        # TODO: possibly update existing queue elements on new interest values as well???

    def getPriority(self, nodeTitle, studentInterests):
        # option for future?: getKeyWords() of node and then use those to compare against studentInterests
        words = nodeTitle
        for interest in list(studentInterests.keys()):
            words = words + ' ' + interest
        tokens = nlp(words)
        priority = 0
        interestTokens = tokens[1:]
        if tokens[0].is_oov: # if does not exist in nlp model, return 0 interest ? # TODO: is interest 0-1 or -1 to 1?
            return 0
        for i in interestTokens:
            if i.is_oov:
                x = studentInterests[i.text]
                interestVal = x[1]
                priority += tokens[0].similarity(i) * interestVal 
        return (1 - priority / len(interestTokens))

if __name__ == "__main__":

    # TODO: does this only work for 1-gram ??

    test = ExplorationTracker()
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,1), 'dinosaurs': (1,1)})) # highest priority
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,0.5), 'dinosaurs': (1,1)})) # smaller priority
    print(test.getPriority(WikiNode('dogs'), {'fashion': (1,1), 'winter': (1,1)})) # low priority