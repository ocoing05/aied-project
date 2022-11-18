from FoxQueue import PriorityQueue
import WikiNode

class ProgressGraph:

    def __init__(self) -> None:

        self.visited = PriorityQueue()
        self.fringe = PriorityQueue()

    def update(self, wikiNode) -> None:

        self._updateVisited(wikiNode)
        # self.visited[wikiNode] = [listOfSpecialKeywords]
        # if self.fringe contains wikiNode, remove it
        # add wikiNode.fringeSet to self.fringe
        pass

    def getVisited(self) -> set:

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