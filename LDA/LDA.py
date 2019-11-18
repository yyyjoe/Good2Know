import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
from gensim import corpora, models

n_topics = 1

# Load and Merge Data
fileNames = ['process-activism.csv', 'process-charity.csv', 'process-donate.csv', 'process-volunteer.csv']
li = []
for fileName in fileNames:
    data = pd.read_csv(fileName, error_bad_lines=False)
    li.append(data)
data = pd.concat(li, axis=0, ignore_index=True)
data_text = data[['Text']]
data_text['index'] = data_text.index
documents = data_text

print("# Documents = " + str(len(documents)))
print(documents[:5])



# Load WordNet and Set stemmer
nltk.download('wordnet')
stemmer = PorterStemmer()


# Define stemmer and Process
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result
processed_docs = documents['Text'].map(preprocess)



# Create Bag of Words Dataset
dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=1000)


# Create Corpus
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]



# TF-IDF
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]




# LDA by BOW
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=n_topics, id2word=dictionary, passes=2, workers=2)
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))


# LDA TF-IDF
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=n_topics, id2word=dictionary, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))







