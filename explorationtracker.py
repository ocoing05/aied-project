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

        # # we may not need this as a priority queue since the graph is already holding all of the visited nodes & we could add any stats needed to there?
        # self.visited = PriorityQueue() 
        
        for i in initialInterests:
            try:
                self.fringe.insert(WikiNode(i), 0.0) 
            except: 
                # don't add this interest if MediaWiki can't identify the correct article to use
                continue

    # i don't think we need this since all update methods are called from student object but keeping it for rn just in case ?
    # def update(self, wikiNode) -> None:
    #     self._updateVisited(wikiNode)
    #     # self.visited[wikiNode] = [listOfSpecialKeywords]
    #     # if self.fringe contains wikiNode, remove it
    #     # add wikiNode.fringeSet to self.fringe
    #     pass

    # def getVisited(self) -> set: # alternatively, this would also be all the nodes in the graph
    #     return self.visited.keys()

    # def _updateVisited(self, wikiNode) -> None:
    #     if not wikiNode.isVisited():
    #         wikiNode.setAsVisited()
    #     else:
    #         (elapsedTime, erosionTime, numVisits, numTests) = self.visited[wikiNode]
    #         numVisits += 1
    #         self.visited[wikiNode] = (elapsedTime, erosionTime, numVisits, numTests)
    #     self.visited[wikiNode] = []
    #     pass

    def updateGraph(self, node):
        '''Called by the student model update() method after a student reads a new article. 
        Adds node to graph.'''
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)

    def updateFringe(self, node, studentInterests):
        '''Called by the student model update() method after a student reads a new article.
        Updates fringe with linked articles from node they just read. Ranked based on student interests.'''
        lp = node.linkedPages
        # kw = node.getKeyWords()
        # for pg in set(lp) & set(kw): # words that exist as both linked pages and key words of the node
         # TODO: instead of using the set of both ^ like above, maybe use keywords to rank linked pages but don't disregard completely?
        for pg in lp:
            # print(pg)
            if self.alreadyExplored(pg): # that article was already read
                continue
            pg = re.sub(r'\W+', ' ', pg) # replaces all non-alphanumeric/underscore characters w space
            if len(pg.strip().split(" ")) > 1 or not pg.isalpha(): # more than 1-gram phrases and non-letters will mess up spacy's analysis
               # TODO: logic for n-gram pages?
               # print("n-gram")
               continue
            priority = self.getPriority(pg, studentInterests)
            if priority == -1: 
                continue # ignore if does not exist in spacy nlp model
            # print(priority)
            try: 
                node = WikiNode(pg, node.title)
            except: # ignore if MediaWiki can't identify which article should be used for this title
                continue
            print(node.title, priority)
            self.fringe.insert(node, priority)

    def getPriority(self, nodeTitle, studentInterests):
        # option for future?: getKeyWords() of node and then use those to compare against studentInterests
        words = nodeTitle
        for interest in list(studentInterests.keys()):
            words = words + ' ' + interest
        # print(words)
        tokens = nlp(words)
        priority = 0
        interestTokens = tokens[1:]
        # print(tokens[0])
        if tokens[0].has_vector: 
            for i in interestTokens:
                #if i.has_vector: # TODO: should always be true ... delete later
                x = studentInterests[i.text]
                interestVal = x[1]
                # print(i)
                # print("similarity", tokens[0].similarity(i))
                # print("interest", interestVal)
                priority += (tokens[0].similarity(i)+1)*0.5 * interestVal # similarity() => -1 to 1
        else:
            return -1 # nodeTitle does not exist in nlp model, can not be analyzed
        return (1 - priority / len(interestTokens))

    def alreadyExplored(self, title):
        if title in list(self.graph.nodes):
            return True
        else:
            return False

if __name__ == "__main__":

    test = ExplorationTracker()
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,1), 'dinosaurs': (1,1)})) # highest priority
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,0.5), 'dinosaurs': (1,1)})) # smaller priority
    print(test.getPriority(WikiNode('dogs'), {'fashion': (1,1), 'winter': (1,1)})) # low priority