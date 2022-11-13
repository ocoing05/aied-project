from ProgressGraph import ProgressGraph

class StudentModel:

    def __init__(self, studentName, username, password, email, interestKeywords) -> None:

        self.studentName = studentName # How to refer to the student
        self.username = username # self-selected unique student identifier
        self.password = password # protecting account usage
        self.email = email # for resetting password

        self.interestKeywords = {} # dictionary of interest keywords, and a value between -1.0 and 1.0 
        for interest in interestKeywords:
            self.interestKeywords[interest] = 1

        self.progressGraph = ProgressGraph()
        self.fringe = {} # Priority Queue of unopened WikiNodes adjacent to progressGraph, sorted by potential interest
        # TODO: add initial interestKeywords as WikiNode objects to the fringe if they exist as wiki articles

        self.newWords = [] # List of words identified by the student as unknown, or that they are unsure of the meaning
        currentSession = None 
        statsBySession = [] # List of sessionStats objects, helps build progress reports for students and teachers


    def getStudentName(self) -> str:

        return self.studentName

    def getInterestKeywords(self) -> dict:

        return self.interestKeywords.keys()

    def updateModel(self) -> None:

        self.updateInterestKeywords
        self.updateFringe
        self.updateProgress


    def updateInterestKeywords(self) -> None:
        
        pass

    def updateFringe(self) -> None:
        
        for key in self.Fringe:
            words = key.getKeywords()
            interestCounter = 0
            for word in words:
                # if (word is in self.studentModel.interestKeywords):
                    # interestCounter += self.studentModel.interestKeywords[word]
                pass

            potentialInterest = interestCounter / len(words)
            self.fringe[key] = potentialInterest

    def updateGraph(self, article):
        self.progressGraph.updateGraph(article)


