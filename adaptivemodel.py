"""
COMP 484 - Introduction to Artificial Intelligence, Fall 2022
Term Project - AI in Education: FreeLearner, presented 12/16/2022
Ingrid O'Connor and Quentin Harrington

This file: adaptivemodel.py
    Adaptive Model generates article recommendations through interactions between: 
        1. Student Model
        2. Domain Model
        3. User Interface
"""

import spacy
from mediawiki import MediaWiki 
from pathlib import Path

from studentmodel import StudentModel
from domainmodel import DomainModel

class AdaptiveModel:
    """Handles all interactions between User Interface, Student Model, and Domain Model.
    Holds a dictionary of recommended articles.
    Initializes spacy NLP and mediawiki wikipedia API objects passed to models and nodes."""
    def __init__(self, studentName, studentInterests) -> None:
        
        # loading natural language processing pipeline, adding sense2vec for multiword noun phrase similarity analysis 
        nlp = spacy.load('en_core_web_lg')
        if Path("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg").is_dir():
            print("Found s2v folder")
            s2v = nlp.add_pipe("sense2vec")
            s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
        else:
            print("sense2vec pre-trained model not found. Continuing without improved similarity measure.")
        wiki = MediaWiki()

        self.student = StudentModel(studentName, studentInterests, nlp, wiki)
        # self.domainModel = DomainModel(nlp, wiki, studentInterests)
        self.recommendations = {} # dictionary of WikiNodes and a value between 0 and 1, indicating quality
    
    def getArticles(self, num) -> list:
        """return a student-specific list of wikiNode pages"""
        return self.student.getFringe(num)


    def update(self, node):
        self.student.updateModel(node)
        # self.domainModel.updateModel(node)

    def updateInterest(self, node, interestVal):
        self.student.updateInterestKeyword(node.title, interestVal)

    def toString(self) -> str:
        return "Student Name: " + self.student.getStudentName()

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
