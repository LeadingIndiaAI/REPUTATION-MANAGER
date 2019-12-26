#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
from utils import *
import re
import string
from keras.models import model_from_json


# In[7]:


word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('glove.6B.50d.txt')


# In[8]:


def remove_url(text):
    text = re.sub(re.compile(r'http\S+'), "",text)
    return text

def remove_mentions(text):
    text = re.sub(re.compile(r'@\S+'), "",text)
    return text

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text


# In[9]:


maxLen=45


# In[10]:


def sentences_to_indices(X, word_to_index, max_len):
    m = X.shape[0]                                   # number of training examples
    X_indices = np.zeros((m,max_len))
    all_keys = word_to_index.keys()
    for i in range(m):                               
        sentence_words = X[i].lower().split()
        j = maxLen-len(X[i].lower().split())
        for w in sentence_words:
            if w in all_keys:
                X_indices[i, j] = word_to_index[w]
            j = j+1
  
    return X_indices


# In[11]:


json_file = open('SentClass7json.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("SentClass7weights.h5")

loaded_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
#l,a = loaded_model.evaluate(test_X_indices, test_Y)
#print(l)
#print(a)


# In[ ]:





# In[14]:


def predict_Senti(text):
    pre_processed_text = remove_url(text)
    pre_processed_text = remove_mentions(text)
    pre_processed_text = remove_punct(text)
    list_ = pre_processed_text.split()[0:45]
    pre_processed_text = " ".join(list_)
    text_list = [pre_processed_text]
    text_list_np = np.array(text_list)
    text_index = sentences_to_indices(text_list_np, word_to_index, maxLen)
    pred = loaded_model.predict(text_index)
    return (pred[0][0])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




