'''
Runs MVP of FreeLearner
'''

from studentmodel import StudentModel

def runFreeLearnerMVP():
    print('Welcome to FreeLearner!')
    name = input('What is your name? ')
    print('Hi, ', name, '!')
    print('Please write a list of things that you would like to learn about.')
    print('This list should be separated by commas but no spaces, like this: Dinosaurs,Science,Disney')
    interestStr = input('What are your interests? \n')
    student = StudentModel(name, '', '', '', createInterestList(interestStr))
    # pseudocode...
    # create recommender object
    # loop until student says quit:
    #   get top suggestions based on student and recommender objects
    #   print options and then let student select article
    #   print sections and let them decide to continue article or stop ?
    #   if continue, print next section... loop until article ends
    #   if stop, then call student.update() with node for article read

def createInterestList(str):
    return str.split(',')

if __name__ == "__main__":
    runFreeLearnerMVP()