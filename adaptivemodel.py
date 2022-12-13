"""Adaptive Model generates adaptive recommendations by utilizing a 
    1. Student Model
    2. Domain Model
    3. Session Tracker"""

from sense2vec import Sense2Vec 
import spacy
from mediawiki import MediaWiki 

from studentmodel import StudentModel
from domainmodel import DomainModel



class AdaptiveModel:
    
    def __init__(self, studentName, studentInterests) -> None:
        
        # loading natural language processing pipeline, adding sense2vec for multiword noun phrase similarity analysis 
        nlp = spacy.load('en_core_web_lg')
        s2v = nlp.add_pipe("sense2vec")
        s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")

        wiki = MediaWiki()

        self.student = StudentModel(studentName, studentInterests, nlp)
        self.domainModel = DomainModel(nlp, wiki, studentInterests)
        self.recommendations = {} # dictionary of WikiNodes and a value between 0 and 1, indicating quality
    
    def getArticles(self) -> list:
        """return a student-specific list of wikiNode pages, sorted by"""

        if (self.student == None):
            # error: no studentModel loaded
            print("No student model found.")
            return []
        else:
            self.student.updateModel()
            return self.recommendations.keys()

    def update(self, node):

        self.student.updateModel(node)
        self.domainModel.updateModel(node)

    def updateInterest(self, node, interestVal):
        self.student.updateInterestKeyword(node.title, interestVal)

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
