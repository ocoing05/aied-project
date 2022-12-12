'''
Runs MVP of FreeLearner
'''

from adaptivemodel import AdaptiveModel

def runFreeLearnerMVP():
    print('Welcome to FreeLearner!')
    name = input('What is your name? ')
    print('Hi, ', name, '!')
    print('Please write a list of things that you would like to learn about.')
    print('This list should be separated by commas but no spaces, like this: dinosaurs,science,disney')
    interestStr = input('What are your interests? \n')
    adaptiveModel = (name, createInterestList(interestStr))
    while True:
        cmd = input('Type n to get a new suggestion or q to quit FreeLearner: ')
        if cmd == 'q':
            break
        suggestions = adaptiveModel.getArticles()
        if suggestions == 0:
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
    student.explorationTracker.fringe.removeValue(currArticle) # remove currArticle from fringe

    print(currArticle.getURL())

    # TODO: print section by section content rather than URL ?
    # continueInput = 'n'
    # while continueInput == 'n' and sections in selected : ?
    #     print('test')
    #     print(topSuggestion.getURL())
    #     continueInput = 'c' # for now just doing one URL for an article, so there's no nextSection
    #     # print next section
    #     # continueInput = input('Enter n to read next section, c to cancel article: ')

    enjoyment = input('On a scale of 0-5, how much did you enjoy that article? ')
    student.updateInterestKeyword(currArticle.title, int(enjoyment)/5) # not sure if this is exactly what we want, but for now keep it simple?
    
    print('Updating your interests... This may take a few minutes.')
    student.updateModel(currArticle) # update student model based on what they just read 

    return student

def createInterestList(str):
    return str.lower().split(',')

if __name__ == "__main__":
    runFreeLearnerMVP()