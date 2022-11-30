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
    while True:
        # get new suggestions TODO: get top 3 instead of only one? 
        currFringe = student.explorationTracker.fringe
        suggestions = getTopSuggestions(3, currFringe)
        print('Here are your options: ')
        for i in range(len(suggestions) - 1): # TODO: error if onl input one interest
            option = suggestions[i]
            node = option[0]
            print(i, ": ", node.title)
        choice = input('Which article would you like to read? ')
        currArticle = suggestions.pop(int(choice))[0] # take chosen article out of suggestions list
        # putSuggestionsBack(suggestions, currFringe) # put not chosen suggestions back in fringe?
        student.explorationTracker.fringe = currFringe # is this the best way to do this? idk
        print(currArticle.getURL())
        # student.updateModel(currArticle) # update student model based on what they just read 
        # TODO: error with line above
        
        # TODO: print section by section content rather than URL
        # continueInput = 'n'
        # while continueInput == 'n' and sections in selected : ?
        #     print('test')
        #     print(topSuggestion.getURL())
        #     continueInput = 'c' # for now just doing one URL for an article, so there's no nextSection
        #     # print next section
        #     # continueInput = input('Enter n to read next section, c to cancel article: ')

        cmd = input('Type n to get a new suggestion or q to quit FreeLearner: ')
        if cmd == 'q':
            break

def createInterestList(str):
    return str.split(',')

# TODO : would probably be better to do this without removing the elements from fringe, so
# we wouldn't have to put them back later... but not sure how to do that bc firstElement() or peek() 
# are only for seeing the first element...
def getTopSuggestions(num, fringe):
    # num = number of suggestions to get
    suggestions = []
    for n in range(num):
        s = fringe.delete()
        suggestions.append(s)
    return suggestions

def putSuggestionsBack(suggestions, fringe):
    for s in suggestions: # TODO: for some reason suggestions has None as last element...
        print("HERE", s)
        fringe.insert(s[0],s[1])
    return fringe

if __name__ == "__main__":
    runFreeLearnerMVP()