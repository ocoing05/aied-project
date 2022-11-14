
class SessionStats:
    
    def __init__(self) -> None:

        self.path = [] # list of wikiNodes, where the index is the order visited 
        self.nodeStats = {} # dictionary of wikiNodes visited this session, and a list of the stats accumulated
        self.statNames = ["elapsedTime", "erosionTime", "numVisits", "numSectionTests"]

    def addToPath(self, wikiNode, statDict) -> None:
        """This function is called when the student moves from one node to another,
        and """
        self.path.append(wikiNode)

        if not self.nodeStats[wikiNode]:
            self.nodeStats[wikiNode] = statDict
        else:
            prevStats = self.nodeStats[wikiNode]
            newStats = {}
            for stat in prevStats.keys():
                prevVal = prevStats[stat] 
                newVal = statDict[stat]
                newStats[stat] = newVal + prevVal

    def getNodeStats(self, wikiNode) -> dict:
        return self.nodeStats[wikiNode]
                
