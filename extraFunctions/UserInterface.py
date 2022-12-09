
from adaptivemodel import AdaptiveModel
import studentconstructor
from studentmodel import StudentModel
from domainmodel import DomainModel
import sessiontracker

import networkx as nx
import matplotlib.pyplot as plt
import time

class UserInterface:

    def __init__(self) -> None:

        self.currStudent = None
        self.recommender = AdaptiveModel()
        self.sessionTracker = sessiontracker()
        self.finished = False # is set to True if the student logs out
        self.startTime = 0 # for tracking usage
        self.endTime = 0 # for tracking usage
        self.currentNode = None

    def run(self) -> None:

        # build GUI 
        # initialize start screen (new user or login)
        # if new user
            # self.makeNewStudent() --> calls tutorial()
        # else
            # self.getStudentFromDatabase() --> calls progressReport()

        while not self.finished:
            recs = self.recommender.getRecommendations()
            self.currentNode = self.nodeSelection(recs)
            pass 
        pass

    def makeNewStudent(self) -> None:

        studentConstructor = studentconstructor()
        self.currStudent = studentConstructor.buildStudentModel()
        self.recommender.setStudentModel(self.currStudent)
        self.tutorial()

        pass

    def getStudentFromDatabase(self) -> None:

        (username, password) = self.login()
        # self.currStudent = getStudent(username, password)
        self.recommender.setStudentModel(self.currStudent)

        pass

    def login(self) -> tuple:
        """Initializes login screen, Gets and returns username and password from user."""

        # initialize login screen
        username = input("Username: ")
        password = input("\nPassword: ")

        return username, password

    def tutorial(self) -> None:
        """The tutorial function gives new students a brief guide to using the interface."""

        # continue button 
        pass

    def progressReport(self) -> None:
        """The progressReport function gives a visual representation of the progressGraph, 
        short textual representation of the last three WikiNodes visited, """
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
        pass

    def nodeSelection(self, recs) -> None:
        # gui.display(recs)
        # 
        pass
    
    def setCurrentNode(self) -> None:

        self.startTime = time.time()


if __name__ == "__main__":
    UI = UserInterface()
    UI.run()
