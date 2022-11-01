
class ProgressGraph:

    def __init__(self) -> None:

        self.visited = {} # a dictionary of all the WikiNodes opened at least once by the Student

    def update(self, wikiNode) -> None:

        # self.visited[wikiNode] = [listOfSpecialKeywords]
        # if self.fringe contains wikiNode, remove it
        # add wikiNode.fringeSet to self.fringe
        pass

    def getExplored(self) -> set:

        return self.visited.keys()

    def updateFringePriority(self) -> None:

        # set 

        pass


