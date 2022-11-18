'''
Runs MVP of FreeLearner
'''

from studentmodel import StudentModel


def runFreeLearnerMVP():
    print('Welcome to FreeLearner!')
    name = input('What is your name? ')
    print('Hi, ', name, '!')
    print('Please write a list of things that you would like to learn about.')
    print('This list should be separated by commas, like this: Dinosaurs,Science,Disney')
    interestStr = input('What are your interests? \n')
    student = StudentModel(name, '', '', '', createInterestList(interestStr))
    

# takes in a string of interests separated by commas and creates an interest list
def createInterestList(str):
    pass

if __name__ == "__main__":
    runFreeLearnerMVP()