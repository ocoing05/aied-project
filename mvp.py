'''
Runs MVP of FreeLearner
'''

from studentmodel import StudentModel
import spacy
from mediawiki import MediaWiki

nlp = spacy.load('en_core_web_lg')
wiki = MediaWiki()

def runFreeLearnerMVP():
    print('Welcome to FreeLearner!')
    name = input('What is your name? ')
    print('Hi, ', name, '!')
    print('Please write a list of things that you would like to learn about.')
    print('This list should be separated by commas but no spaces, like this: Dinosaurs,Science,Disney')
    interestStr = input('What are your interests? \n')
    student = StudentModel(name, createInterestList(interestStr), nlp, wiki)
    while True:
        cmd = input('Type n to get a new suggestion or q to quit FreeLearner: ')
        if cmd == 'q':
            break
        student = getArticles(student)
        if student == 0:
            print("No suggestions.")
            break


def getArticles(student):
    '''Get new options and print URL of the chosen article. Returns updated student.'''
    suggestions = student.explorationTracker.getFringe(4)
    if len(suggestions) == 0:
        return 0
    print('Here are your options: ')
    for i in range(len(suggestions)):
        option = suggestions[i]
        node = option[0]
        priority = option[1]
        print(i, ": ", node.title, " ", priority)
    choice = input('Which article would you like to read? ')
    currArticle = suggestions.pop(int(choice))[0]
    #student.explorationTracker.fringe.removeValue(currArticle) # remove currArticle from fringe

    print(currArticle.getURL())

    enjoyment = input('On a scale of 0-5, how much did you enjoy that article? ')

    student.updateInterestKeyword(currArticle.title, int(enjoyment)/5)
    
    print('Updating your interests... This may take a few minutes.')
    student.updateModel(currArticle, True) # update student model based on what they just read 

    return student

def createInterestList(str):
    return str.split(',')

if __name__ == "__main__":
    runFreeLearnerMVP()