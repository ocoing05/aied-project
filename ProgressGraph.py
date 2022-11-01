
class ProgressGraph:

    def __init__(self) -> None:

        self.opened = {} # a dictionary of all the WikiNodes opened at least once by the Student

    def update(self, wikiNode) -> None:

        # self.opened[wikiNode] = [listOfSpecialKeywords]
        # if self.fringe contains wikiNode, remove it
        # add wikiNode.fringeSet to self.fringe
        pass

    def getExplored(self) -> set:

        return self.opened.keys()

    def updateFringePriority(self) -> None:

        # set 

        pass


