import wikipedia

page = wikipedia.page("Albert Einstein")
text = page.content

"""NLTK - RAKE"""

# import nltk
# from rake_nltk import Rake

# nltk.download('stopwords')
# nltk.download('punkt')
# rake_nltk_var = Rake()

# # print(keyword_extracted)

# rake_nltk_var.extract_keywords_from_text(text)
# keyword_extracted = rake_nltk_var.get_ranked_phrases()

# top_keywords = keyword_extracted[0:20]
# for k in top_keywords:
#     print(k)

"""YAKE"""

import yake
kw_extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 2
deduplication_threshold = 0.9 # 0.1 to prohibit repeated words in key words
numOfKeywords = 20

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)