from explorationtracker import ExplorationTracker

class StudentModel:

    def __init__(self, studentName, username, password, email, interestKeywords) -> None:

        self.studentName = studentName # How to refer to the student

        self.interestKeywords = {}  # dictionary of interest keywords, and a tuple:
                                    # first value: times updated
                                    # second value: level of interest, between -1.0 and 1.0
                                # TODO: determine if we want 0-1 or -1-1 and make sure all logic fits
                                    #
                                    # Level of interest is determined by:
                                    #   1. Summing values all values inputed for the specific keyword
                                    #   2. Dividing summed value by number of times updated

        for interest in interestKeywords:
            i = interest.lower()
            self.interestKeywords[i] = (1, 1) # initializing all interests retrieved from survey

        # explorationTracker contains explored graph, fringe queue, and visited queue(?)
        self.explorationTracker = ExplorationTracker(interestKeywords)

        # NOT FULLY IMPLEMENTED...
        self.username = username # self-selected unique student identifier
        self.password = password # protecting account usage
        self.email = email # for resetting password
        self.newWords = [] # List of words identified by the student as unknown, or that they are unsure of the meaning
        currentSession = None 
        statsBySession = [] # List of sessionStats objects, helps build progress reports for students and teachers


    def getStudentName(self) -> str:
        return self.studentName

    def getInterestKeywords(self) -> set:
        return self.interestKeywords.keys()

    def getFringe(self, numNodes) -> list:
        return self.explorationTracker.getFringe(numNodes)

    def updateModel(self, node) -> None:
        '''Called when the student reads a new article.
            Updates progress graph, student interest dictionary, and fringe queue.
            Parameter node = the WikiNode representing the article they just read.'''
        # update progress graph with new WikiNode article read
        self.explorationTracker.updateGraph(node)
        # update fringe queue with linked nodes
        self.explorationTracker.updateFringe(node, self.interestKeywords)

    def updateInterestKeyword(self, keyword, newInterestValue) -> None:
        """This function is called when a new interest value is retrieved,
        regardless of if the keyword already exists in the self.interestKeywords dictionary."""

        # add new keyword to interestKeywords
        if not keyword in self.getInterestKeywords():
            self.interestKeywords[keyword.lower()] = (1, newInterestValue)
        # update interest level in interestKeywords list
        else:
            (timesUpdated, interestLevel) = self.interestKeywords[keyword]

            newTimesUpdated = timesUpdated + 1
            newInterestLevel = (interestLevel + newInterestValue)/newTimesUpdated 
            self.interestKeywords[keyword.lower()] = (newTimesUpdated, newInterestLevel)
