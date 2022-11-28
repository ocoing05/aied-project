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
    print(student.explorationTracker.fringe)
    # while True:
    #     cmd = input('Type n to get a new suggestion or q to quit FreeLearner: ')
    #     if cmd == 'q':
    #         break
    #     # get new suggestions TODO: get top 3 instead of only one? 
    #     topSuggestion = student.explorationTracker.fringe.firstElement()
    #     # print options and let student select, set as selected article
    #     continueInput = 'n'
    #     # TODO: while sections in selected and continue is 'n':
    #     while continueInput == 'n':
    #         print(topSuggestion.getURL())
    #         continueInput = 'c' # for now just doing one URL for an article, so there's no nextSection
    #         # print next section
    #         # continueInput = input('Enter n to read next section, c to cancel article: ')
    #     student.update(topSuggestion) # update student model based on what they just read

def createInterestList(str):
    return str.split(',')

if __name__ == "__main__":
    runFreeLearnerMVP()