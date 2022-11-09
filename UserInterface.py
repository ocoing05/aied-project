
import Recommender
import StudentConstructor
import StudentModel
import WikiNode
import SessionTracker

class UserInterface:

    def __init__(self) -> None:

        self.currStudent = None
        self.recommender = Recommender()
        self.sessionTracker = SessionTracker()
        self.finished = False # is set to True if the student logs out
        pass

    def run(self) -> None:

        # build GUI 
        # initialize start screen (new user or login)
        # if new user
            # self.makeNewStudent() --> calls tutorial()
        # else
            # self.getStudentFromDatabase() --> calls progressReport()

        while not self.finished:
            pass
        pass

    def makeNewStudent(self) -> None:

        studentConstructor = StudentConstructor()
        self.currStudent = studentConstructor.buildStudentModel()
        self.recommender.setStudentModel(self.currStudent)
        self.tutorial()

        pass

    def getStudentFromDatabase(self) -> None:

        (username, password) = self.login()
        self.currStudent = getStudent(username, password)
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
        pass

if __name__ == "__main__":
    UI = UserInterface()
    UI.run()
