from explorationtracker import ExplorationTracker

class StudentModel:

    def __init__(self, studentName, interestKeywords, nlp, wiki, username = None, password = None, email = None) -> None:
        
        self.studentName = studentName # How to refer to the student

        self.interestKeywords = {}  # dictionary of interest keywords, and a tuple:
                                    # first value: times updated
                                    # second value: total summed level of interest over all times updated
                                    # (interest level is between 0.0 and 1.0 each time)
                                    #
                                    # Level of interest is determined by:
                                    #   dividing the total interest level by the times updated, 
                                    #   to get an average interest value between 0.0 and 1.0

        for interest in interestKeywords:
            i = interest.lower()
            self.interestKeywords[i] = (1, 1) # initializing all interests retrieved from survey

        # explorationTracker contains explored graph and fringe queue
        self.explorationTracker = ExplorationTracker(nlp, wiki, interestKeywords)
        self.nlp = nlp
        self.newWords = [] # List of words identified by the student as unknown, or that they are unsure of the meaning

        # NOT FULLY IMPLEMENTED...
        self.username = username # self-selected unique student identifier
        self.password = password # protecting account usage
        self.email = email # for resetting password
        currentSession = None 
        statsBySession = [] # List of sessionStats objects, helps build progress reports for students and teachers

        ###

    def getStudentName(self) -> str:
        return self.studentName

    def getInterestKeywords(self) -> list:
        return list(self.interestKeywords.keys())

    def getFringe(self, numNodes) -> list:
        return self.explorationTracker.getFringe(numNodes)

    def updateModel(self, node, mvp) -> None:
        '''Called when the student reads a new article.
            Updates progress graph, student interest dictionary, and fringe queue.
            Parameter node = the WikiNode representing the article they just read.'''
        # update progress graph with new WikiNode article read
        self.explorationTracker.updateGraph(node)
        # update fringe queue with linked nodes
        self.explorationTracker.updateFringe(node, self.interestKeywords, mvp)

    def updateInterestKeyword(self, keyword, newInterestValue) -> None:
        """This function is called when a new interest value is retrieved,
        regardless of if the keyword already exists in the self.interestKeywords dictionary."""

        # add new keyword to interestKeywords
        if not keyword in self.getInterestKeywords():
            self.interestKeywords[keyword.lower()] = (1, newInterestValue)
        # update interest level in interestKeywords list
        else:
            (timesUpdated, interestLevel) = self.interestKeywords[keyword]
            scaledInterestLevel = interestLevel * timesUpdated
            newTimesUpdated = timesUpdated + 1
            newInterestLevel = (scaledInterestLevel + newInterestValue)/newTimesUpdated
            self.interestKeywords[keyword.lower()] = (newTimesUpdated, newInterestLevel)

    def getRelativeNodeProfile(self, node) -> dict:
        """Returns a dictionary of statistics analyzing the relationships between the node and studentInterests."""
        expectedInterest, topSimilar = self.getExpectedInterest(node)
        nodeProfileDict = {
            'title': node.getTitle(),
            'expected_interest': expectedInterest, # aggregate expected interest level across student interests
            'top_similarity_list': topSimilar, # top 10 most similar interests
        }
        return nodeProfileDict

    def getExpectedInterest(self, node) -> tuple:

        nodeDoc = self.nlp(node.getTitle())
        interestDict = {} # Dictionary of interestKeywords as nlp doc objects (keys) and interestVal (values)
        for interest in self.interestKeywords:
            timesUpdated, interestVal = self.interestKeywords[interest]
            interestDict[self.nlp(interest)] = interestVal
        
        return self.calcSimilarity(nodeDoc, interestDict)

    def calcSimilarity(nodeDoc, interestDict) -> tuple:
        """Given a nodeTitle spacy doc and a keyword interest dictionary {keywordSpacyDoc: keywordInterestVal},
        Return a tuple (x, y):
            x = the expected interest level (0-high, 1-low) of the node
            y = dictionary of interest nodes sorted by similarity to nodeDoc
        """
        nodeSimDict = {}
        totalSim = 0
        for intDoc in interestDict.keys():
            if len(nodeDoc) != 1 or len(intDoc) != 1:
                # adds the standard spacy similarity between link and keyword to totalSim
                sim = ((nodeDoc.similarity(intDoc) + 1) * 0.5) * interestDict.get(intDoc)
    
            else:
                # adds the sense2vec similarity between the link token and the keyword token,
                # if both in sense2vec vocabulary.
                sim = ((nodeDoc._.s2v_phrases[0]._.s2v_similarity(intDoc._.s2v_phrases[0]) + 1) * 0.5) * interestDict.get(intDoc)
            nodeSimDict[intDoc] = sim
            totalSim += sim   

        sortedDict = sorted(nodeSimDict.items(), key= lambda item:item[1], reverse=True)
        return ((1 - totalSim/len(interestDict)), sortedDict)

