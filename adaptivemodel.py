"""Adaptive Model generates adaptive recommendations by utilizing a 
    1. Student Model
    2. Domain Model
    3. Session Tracker"""


from studentmodel import StudentModel
from domainmodel import DomainModel
from sense2vec import Sense2Vec
import spacy

class AdaptiveModel:
    
    def __init__(self, studentModel, domainModel) -> None:
        
        self.studentModel = studentModel
        self.domainModel = domainModel
        self.recommendations = {} # dictionary of WikiNodes and a value between 0 and 1, indicating quality
    
    def getRecommendations(self) -> list:

        if (self.studentModel == None):
            # error: no studentModel loaded
            return []
        else:
            return self.recommendations.keys()

# Notes:

# student model fringe queue sorted only based on interests
# then goes in here to be also sorted by whatever aspect we choose to prioritize
# the domain model wiki noncyclic graph could also be input in here 
# going higher into hierarchy vs lower vs somewhere altogether different domain

# compare student progress graph with ontology graph to see which are explored
# maybe just get the top n in the student's queue to go into Recommender
# take articles from student queue and sort those into categories based on domains in ontology model

if __name__ == "__main__":
    pass
    # nlp = spacy.load('en_core_web_lg')
    # s2v = nlp.add_pipe("sense2vec")
    # s2v.from_disk("/path/to/s2v_reddit_2015_md")

    # doc1 = s2v("Alien")
    # doc2 = s2v("Extraterrestrial")

    # print(doc1.similarity(doc2))
