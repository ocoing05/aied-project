import networkx as nx
from WikiNode import WikiNode

class ProgressGraph:
    # maybe we should rename to ProgressTracker instead since it holds graph, fringe, etc. 
    # and isn't just the actual graph object ?

    def __init__(self) -> None:

        self.visited = {} # a dictionary of all the WikiNodes opened at least once by the Student
        self.graph = None # graph representing articles read
        # Example visited item:
        #   {Dinosaurs : [1000(time first opened), ]}

    def update(self, wikiNode) -> None:

        # self.visited[wikiNode] = [listOfSpecialKeywords]
        # if self.fringe contains wikiNode, remove it
        # add wikiNode.fringeSet to self.fringe
        pass

    def getExplored(self) -> set:

        return self.visited.keys()

    def updateKey(key) -> None:

        # set 

        pass

    def updateVisited(self, wikiNode) -> None:

        if not self.isVisited(wikiNode):
            self.visited[wikiNode] = (elapsedTime, erosionTime, 1, numTests)
        else:
            (elapsedTime, erosionTime, numVisits, numTests) = self.visited[wikiNode]
            numVisits += 1
            self.visited[wikiNode] = (elapsedTime, erosionTime, numVisits, numTests)

        self.visited[wikiNode] = []

        pass

    def isVisited(self, key) -> bool:

        return self.visited.has_key(key)

    # called after a student reads a new article
    def updateGraph(self, node): # is this what update is supposed to be?
        if not self.graph: # is the student does not have a graph yet/hasn't read any articles yet
            self.graph = nx.Graph()
        # update explored graph
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)
        # update fringe queue
        # something like the lines below, but ranked based on interests / NLP / key words ?
        # for pg in node.linkedPages:
            # studentFringe.add(WikiNode(pg, node.title)) # should add the node object to keep track of parent node, not just the title
        # update student interests ?

