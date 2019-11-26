import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
from gensim import corpora, models
import math
import os
import json
import nltk
# nltk.download('wordnet', "/Users/jeff/nltk_data")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NUM_TOPICS=10

class LDA(object):
    def __init__(self):
        nltk.download('wordnet')
        LAD_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/lda_model.pkl")
        self.lda_model_tfidf = models.LdaModel.load(LAD_DIR)

        DIC_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/dictionary_model.dict")
        self.dictionary = corpora.Dictionary.load(DIC_DIR)

        self.stemmer = PorterStemmer()
        self.NUM_TOPICS=10
        
        #DIC_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/dataframe.csv")
        DIC_DIR = "/Users/jeff/Desktop/output.csv"
        self.db = pd.read_csv(DIC_DIR)

    # # Define stemmer and Process
    def lemmatize_stemming(self,text):
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    def preprocess(self,text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(self.lemmatize_stemming(token))
        return result

    def getLDA(self,text):

        bow = self.dictionary.doc2bow(self.preprocess(text))

        data ={}
        data["num_topics"] = self.NUM_TOPICS
        data["topics"] = {}
        data["posts"] = []

        nums_of_posts=np.zeros(self.NUM_TOPICS,dtype=float)
        topic_id = np.arange(self.NUM_TOPICS)
        percentage = np.zeros(self.NUM_TOPICS,dtype=float)
        for p in self.lda_model_tfidf[bow]:
            percentage[p[0]] = p[1]
            nums_of_posts[p[0]] = (round(p[1]*10))

        data["topics"]["labels"] = list(topic_id)
        data["topics"]["data"] = list(percentage)
        for index, row in self.db.iterrows():
            #print(nums_of_posts[row['topic']])
            if(nums_of_posts[row['topic']]>0):
                nums_of_posts[row['topic']]-=1
                data["posts"].append({'userID':row['ID'],
                                      'imgURL':row['Img_URL'],
                                      'text':row['Text'],
                                      'date':row['Date'],
                                      'like':row['Likes'],
                                     })

        app_json = json.dumps(str(data))

        return app_json