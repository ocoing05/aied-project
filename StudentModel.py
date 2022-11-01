import ProgressGraph

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
        self.fringeQueue = {} # Priority Queue of unopened WikiNodes adjacent to progressGraph, sorted by potential interest
        self.newWords = [] # List of words identified by the student as unknown/that they are unsure of the meaning

    def getStudentName(self) -> str:

        return self.studentName

    def getInterestKeywords(self) -> dict:

        return self.interestKeywords.keys()

    def updateFringe(self) -> None:
        
        for key in self.fringeQueue:
            words = key.getKeywords()
            interestCounter = 0
            for word in words:
                # if (word is in self.studentModel.interestKeywords):
                    # interestCounter += self.studentModel.interestKeywords[word]
                pass

            potentialInterest = interestCounter / len(words)
            self.fringeQueue[key] = potentialInterest




