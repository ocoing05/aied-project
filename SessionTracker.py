import SessionStats
import time 

class SessionTracker:

    def __init__(self) -> None:

        self.sessionStats = SessionStats()
        self.startTime = 0
        self.currNode = None
        pass

    def startTiming(self, wikiNode) -> None:
        
        self.currNode = wikiNode
        self.startTime = time.time()

