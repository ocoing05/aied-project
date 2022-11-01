import StudentModel
import WikiNode

class Recommender:
    
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
