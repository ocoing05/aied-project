from StudentModel import StudentModel
from WikiNode import WikiNode

# *** MOCK DATA ***

# create students
student1 = StudentModel("Ingrid", "ingrid", "12345", "ioconnor@macalester.edu", ["Disney", "Dinosaurs", "Volcanoes"])

# create articles
article1 = WikiNode("Disney")
article2 = WikiNode("Penguins")
article3 = WikiNode("Volcanoes")
article4 = WikiNode("Egyptian pyramids")
article5 = WikiNode("Wolfgang Amadeus Mozart")
# when creating new nodes, if the node was added from the fringe by being linked from a previous article it would be created like this:
article6 = WikiNode("Mickey Mouse", "Disney")

# *** TEST DEFINITIONS ***

# *** WikiNode ***
def testWikiNodes():
    testSections()
    # testSummary() # TODO: api not working right atm.. need to fix
    testPrevNode()
    testKeyWords()

def testSections():
    # print(article1.getSectionTitles())
    assert 'History' in article1.getSectionTitles()
    assert 'Legacy' in article1.getSectionTitles()

def testSummary():
    # print(article4.getSummary(4))
    assert "After becoming a major success by the early 1940s" in article1.getSummary(4)

def testPrevNode():
    assert article1.prevNode == None
    assert article6.prevNode == "Disney"

def testKeyWords():
    kw = article1.getKeyWords()
    assert 'film' in kw
    assert 'Mickey Mouse' in kw
    # print("DISNEY KEY WORDS: ", kw)

# *** StudentModel ***
def testStudentModel():
    testUpdateGraph()
    # TODO: student creation, fringe updates, student interest updates, session stats

def testUpdateGraph():
    # student1 reads article1
    student1.updateGraph(article1)   
    assert len(list(student1.progressGraph.graph.nodes)) == 1
    # TODO : test that fringe was updated with linked nodes in prioritized order ?
    # student1 reads article6
    student1.updateGraph(article6)
    assert len(list(student1.progressGraph.graph.nodes)) == 2
    assert len(student1.progressGraph.graph.edges) == 1

# *** Recommender ***
def testRecommender():
    pass

# *** UI ***
def testUI():
    pass

# *** RUN TESTS ***

if __name__ == "__main__":
    testWikiNodes()
    testStudentModel()