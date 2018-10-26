
# coding: utf-8

# In[10]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import re
import nltk
import numpy as np
import pandas as pd
# nltk.download('genesis')
# nltk.download('punkt')
# # # nltk.download('all')
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize
from scipy.spatial import distance

stop_words = stopwords.words('english')


import string
wordnet_lemmatizer = WordNetLemmatizer()
lemmaAdj = []
lemmaVerb = []
tagged_tokens = []
token = []
# Q1


def get_wordnet_pos(pos_tag):
    # if pos tag starts with 'J'
    if pos_tag.startswith('J'):
        # return wordnet tag "ADJ"
        return wordnet.ADJ

    # if pos tag starts with 'V'
    elif pos_tag.startswith('V'):
        # return wordnet tag "VERB"
        return wordnet.VERB

    # if pos tag starts with 'N'
    elif pos_tag.startswith('N'):
        # return wordnet tag "NOUN"
        return wordnet.NOUN

    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        # be default, return wordnet tag "NOUN"
        return wordnet.NOUN
    

def tokenize(text):
    token_count = None
    
    # converts the string into lowercase
    low_text = text.lower()

    # segments the lowercased string into tokens - Based on the requirements
    pattern = r'[a-z0-9][a-z0-9-_.@]*[a-z0-9]'
    tokens = nltk.regexp_tokenize(low_text, pattern)

    # POS
    tagged_tokens= nltk.pos_tag(tokens)

    lemmatized_words=[wordnet_lemmatizer.lemmatize          (word, get_wordnet_pos(tag))           # tagged_tokens is a list of tuples (word, tag)
          for (word, tag) in tagged_tokens \
          # remove stop words
          if word not in stop_words]
    
    token_count = nltk.FreqDist(lemmatized_words)
    return token_count 

# Q2


def find_similar_doc(doc_id, docs):

    best_matching_doc_id = None
    similarity = None
    
    dict_final = {}
    
    for idx,doc in enumerate(docs):
        dictToken = {key:value for key, value in tokenize(doc).items()}
        dict_final[idx] = dictToken

    dtm=pd.DataFrame.from_dict(dict_final, orient="index")
    dtm=dtm.fillna(0)

    tf=dtm.values
    doc_len=tf.sum(axis=1)
    tf=np.divide(tf.T, doc_len).T

    df=np.where(tf>0,1,0)

    smoothed_idf=np.log(np.divide(len(docs)+1, np.sum(df, axis=0)+1))+1    
    smoothed_tf_idf=tf*smoothed_idf
    
    similarity = 1 - distance.squareform(distance.pdist(smoothed_tf_idf, 'cosine'))

    best_matching_doc_id = np.argsort(similarity)[:,::-1][doc_id,0:2]

    
    return best_matching_doc_id, similarity


# # Q3.1
# def match_question_answer(questions, answers):

#     result = []


    
    

#     return result



if __name__ == "__main__":

     # Test Q1
    text='''contact Yahoo! at "http://login.yahoo.com", select forgot
     your password. If that fails to reset, contact Yahoo! at
     their password department 408-349-1572 -- Can't promise
     their phone department will fix, but they'll know where to
     go next. Corporate emails from Yahoo! don't come from
     their free mail system address space. Webmaster@yahoo.com
     is not a corporate email address.'''
    
    tokenize(text)
    for key, value in tokenize(text).items():
        pass
#         print(key, value)
        
     # You should get the result look like :
     # contact 2 yahoo 3 http 1 login.yahoo.com 1
     # select 1 forget 1 password 2 fail 1
     # reset 1 department 2 408-349-1572 1 promise 1
     # phone 1 fix 1 know 1 go 1
     # next 1 corporate 2 email 2 come 1
     # free 1 mail 1 system 1 address 2
     # space 1 webmaster@yahoo.com 1

    

    # Test Q2
    print("\nTest Q2")
    data = pd.read_csv("qa.csv", header=0)
    doc_id=15
    x,y = find_similar_doc(doc_id, data["question"].values.tolist())
    print(x,y)
    print(data["question"].iloc[doc_id])
    print(data["question"].iloc[x])
    
    doc_id=51
    x,y=find_similar_doc(doc_id, data["question"].values.tolist())
    print(x,y)
    print(data["question"].iloc[doc_id])
    print(data["question"].iloc[x])

#     # Test Q3
#      print("\nTest Q3.1")
#      result = match_question_answer(data["question"].values.tolist(), \
#      data["answer"].values.tolist())



