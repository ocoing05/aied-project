
class ProgressGraph:

    def __init__(self) -> None:

        self.visited = {} # a dictionary of all the WikiNodes opened at least once by the Student

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



