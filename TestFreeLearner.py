from studentmodel import StudentModel
from wikinode import WikiNode
from explorationtracker import ExplorationTracker
from mediawiki import MediaWiki
import spacy
from sense2vec import Sense2Vec, Sense2VecComponent
import yake

# *** MOCK DATA ***

# create students
student1 = StudentModel("Ingrid", "ingrid", "12345", "ioconnor@macalester.edu", ["Disney", "Dinosaurs", "Volcanoes"])
student2 = StudentModel("Quentin Harrington", 
                        "quentinroyal", 
                        "password",
                        "qharring@macalester.edu", 
                        ["Computers", "Sustainability", "Ecology", "Soccer", "Urbanism", "Architecture", "Plants", "Psychology"])

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
    testSummary()
    testPrevNode()
    testKeyWords()

def testSections():
    assert 'History' in article1.getSectionTitles()
    assert 'Legacy' in article1.getSectionTitles()
    assert article1.getSection('History') == 'Empty section'
    assert "Bob Iger introduced D23 in 2009" in article1.getSection("2005–2020: Bob Iger's leadership, expansion, and Disney+")

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
    testStudentCreation()
    # TODO: student creation, fringe updates, student interest updates, session stats

def testStudentCreation():
    student2 = StudentModel("test", "test", "12345", "test@test.com", ["Dogs", "Dinosaurs", "Volcanoes", "Disney"])
    assert student2.getStudentName() == 'test'
    assert 'Dogs' in student2.getInterestKeywords()
    assert 'Volcanoes' in student2.getInterestKeywords()
    # TODO : test fringe creation

# *** ExplorationTracker ***
def testExplorationTracker():
    testGraph()
    testFringe()

def testGraph():
    student1.updateModel(article1)
    assert len(list(student1.progressGraph.graph.nodes)) == 1
    # TODO : test that fringe was updated with linked nodes in prioritized order ?
    # and test that the student interests were updated correctly
    # student1 reads article6
    student1.updateModel(article6)
    assert len(list(student1.progressGraph.graph.nodes)) == 2
    assert len(student1.progressGraph.graph.edges) == 1

def testFringe():
    testPriorityRankings()
    testUpdateFringe()

def testPriorityRankings():
    et = ExplorationTracker([])
    priority1 = et.getPriority('Science', {'math': (1,1), 'physics': (1,1)})
    priority2 = et.getPriority('Science', {'dogs': (1,1), 'Disney': (1,1)})
    priority3 = et.getPriority('Science', {'math': (1,0.5), 'physics': (1,0.5)})
    priority4 = et.getPriority('Science', {'math': (1,0.5), 'physics': (1,0.8)})
    assert priority1 < priority2
    assert priority1 < priority3
    assert priority4 < priority3
    priority5 = et.getPriority('ndlsajncjxdsfjvdk', {'math':(1,1)})
    assert priority5 == -1
    
def testUpdateFringe():
    pass

# *** Recommender ***
def testRecommender():
    pass

# *** UI ***
def testUI():
    pass

# *** spacy and sense2vec ***
def testSpacy():

    # doc = s2vNLP("A sentence about natural language processing.")
    # assert doc[3:6].text == "natural language processing"
    # freq = doc[3:6]._.s2v_freq
    # vector = doc[3:6]._.s2v_vec
    # most_similar = doc[3:6]._.s2v_most_similar(3)
    # print(freq)
    # print(most_similar)

    # doc = s2vNLP("A sentence about Facebook and Google.")
    # for ent in doc.ents:
    #     assert ent._.in_s2v
    #     most_similar = ent._.s2v_most_similar(3)
    # print(most_similar
    pass

def testMediaWiki():
    """Testing:
        1. For each articleTitle:
            a. Initialize wikiNode for page
            b. Initialize spacy doc for page title
            c. Initialize spacy doc for page summary
            d. Build dictionary of links and their similarity to summary, normalized to title <-> summary similarity
                1. 

    """

    wikipedia = MediaWiki()

    # create natural language processing elements
    # controlNLP = spacy.load("en_core_web_lg")
    s2vNLP = spacy.load("en_core_web_lg")
    s2v = s2vNLP.add_pipe("sense2vec")
    s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")

    randomArticles = {} # Dictionary of random article titles (keys) and their links sorted by (values)
    for articleTitle in ["FIFA World Cup", "ambulatory", "ducks", "internet", "United States Department of Defense", "urban planning"]:
        print("======================")
        print("Title: " + articleTitle)
        wikiNode = WikiNode(articleTitle)
        summary = wikiNode.getSummary()
        titleDoc = s2vNLP(articleTitle)
        summaryDoc = s2vNLP(summary)
        print(titleDoc.similarity(summaryDoc))

        # titleToken = s2vNLP(articleTitle)._.s2v_phrases
        # if len(titleToken) != 1:
        #     break
        # print(titleToken)

        # summaryTokens_withDup = s2vNLP(summary)._.s2v_phrases
        # summaryTokens = []
        # for token in summaryTokens_withDup:
        #     if token in summaryTokens:
        #         continue
        #     else:
        #         summaryTokens.append(token)
        

        # print(summaryTokens)


        # linkSimDict = {} 
        # links = wikiNode.getLinkedPageTitles
        # for link in links:
        #     linkDoc = s2vNLP(link)
        # UAWords = []
        # for token in doc:
        #     if token.is_alpha and not token.is_oov and not token.is_stop and token.text not in UAWords:
        #         UAWords.append(token.text)
        # print(UAWords)
        # print("======================")
        
        
        # links = wikiNode.getLinkedPageTitles
        # links.sort(key=_sortFunc)
        # randomArticles[wikiNode] = links

def _sortFunc():
    # text = self.getContent()
    language = "en"
    max_ngram_size = 1 # only 1-gram so that spacy can work
    deduplication_threshold = 0.1 # set to 0.1 to prohibit repeated words in key words
    numOfKeywords = 100
    extractor = yake.KeywordExtractor(
        lan=language, 
        n=max_ngram_size, 
        dedupLim=deduplication_threshold, 
        top=numOfKeywords, 
        features=None)
    # tuples = extractor.extract_keywords(text)
    # keywords = [i[0] for i in tuples]
    # self.keywords = keywords
    # return keywords
    pass

# *** RUN TESTS ***

if __name__ == "__main__":

    # testWikiNodes()
    # testStudentModel()
    # testExplorationTracker()
    # testRecommender()
    # testUI()
    # testSpacy()
    testMediaWiki()
    print("All tests pass.")