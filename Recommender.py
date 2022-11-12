import StudentModel
import WikiNode

class Recommender:
    # how does this work? wouldn't this sort of be used within student model to determine the ordering of fringe?
    # like a student model would use this class as a helper to create the fringe ?
    
    def __init__(self) -> None:
        
        self.studentModel = None
        self.recommendations = {} # dictionary of WikiNodes and a value between 0 and 1, indicating quality, ordered by quality 

    def setStudentModel(self, studentModel) -> None:
        
        self.studentModel = studentModel


    def getRecommendations(self) -> list:
        
        return self.recommendations.keys()

    def generateNewRecommendations(self) -> None:

        # self.studentModel.getFringe
        
        pass
