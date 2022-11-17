import StudentModel
import DomainModeling

class Recommender:
    
    def __init__(self) -> None:
        
        self.studentModel = None
        self.recommendations = {} # dictionary of WikiNodes and a value between 0 and 1, indicating quality, ordered by quality 

    def setStudentModel(self, studentModel) -> None:
        
        self.studentModel = studentModel


    def getRecommendations(self) -> list:

        if (self.studentModel == None):
            # error: no studentModel loaded
            return []
        else:
            return self.recommendations.keys()

    def generateNewRecommendations(self) -> None:
        
        if (self.studentModel == None):
            # error: no studentModel loaded
            pass
        else:
            
            # self.studentModel.getFringe
            pass

# Notes:

# student model fringe queue sorted only based on interests
# then goes in here to be also sorted by whatever aspect we choose to prioritize
# the domain model wiki noncyclic graph could also be input in here 
# going higher into hierarchy vs lower vs somewhere altogether different domain

# compare student progress graph with ontology graph to see which are explored
# maybe just get the top n in the student's queue to go into Recommender
# take articles from student queue and sort those into categories based on domains in ontology model