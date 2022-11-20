import networkx as nx
# import spacy

from FoxQueue import PriorityQueue
from WikiNode import WikiNode

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
        for pg in node.linkedPages:
            priority = self.getPriority(pg, studentInterests)
            self.fringe.add(WikiNode(pg, node.title), priority)
        # TODO: possibly update existing queue elements on new interest values as well???

    def getPriority(self, title, studentInterests):
        # TODO: return a priority value for title based on spacy analysis against studentInterests list

        # --- past code for reference: ---
        #     for key in self.fringe:
        #         words = key.getKeywords()
        #         interestCounter = 0
        #         for word in words:
        #             # if (word is in self.studentModel.interestKeywords):
        #                 # interestCounter += self.studentModel.interestKeywords[word]
        #         potentialInterest = interestCounter / len(words)
        #         self.fringe[key] = potentialInterest

        return 0 # TODO: change once method is implemented fully

if __name__ == "__main__":

    '''spacy / sense2vec'''
    # terminal commands:
    # pip3 install -U pip setuptools wheel
    # pip3 install -U spacy
    # python3 -m spacy download en_core_web_lg

    import spacy
    nlp = spacy.load('en_core_web_lg')
    words = ''
    tokens = nlp(words)
    for token in tokens:
        print(token.text, token.has_vector, token.vector_norm, token.is_oov)
    # has_vector: if it contains a vector representation in the model, vector_norm: the algebraic norm of the vector, is_oov: if the word is out of vocabulary.
    print(tokens[0].similarity(tokens[1]))
