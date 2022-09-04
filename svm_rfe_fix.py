# -*- coding: utf-8 -*-
"""SVM RFE FIX

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VKCXdDRed0mWiCzSd1iR4DdK-9JuO6CQ

#Library
"""

import pandas as pd 
import numpy as np 

#import nltk for natural language toolkit
from nltk.corpus import stopwords
import nltk 

#import re, unicode
import re, unicodedata

#import sklearn preprocessing 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

#import sklearn for modeling
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#import sklearn for model evaluation 
from sklearn.metrics import classification_report, f1_score, confusion_matrix, roc_auc_score
#import visualization module 
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

#textblob
from textblob import Word
from textblob import TextBlob

import warnings
warnings.filterwarnings('ignore')

"""#Load data kotor

##install tambahan library
"""

!pip install PyStemmer

!pip install sastrawi

nltk.download('punkt')

nltk.download('stopwords')

!pip install TextBlob
!pip install unidecode

df_kotor = pd.read_csv('/content/drive/MyDrive/project/sentimentv5.csv')

df_kotor.head(3)

df_kotor.info()

"""#Preprocessing data kotor

"""

df_kotor['Text']=df_kotor['Text'].astype(str)

"""##Cleaning"""

def cleaningText(text):
    

    text = text.replace('\n', ' ') # replace new line into space
    text = text.strip(' ') # remove characters space from both left and right text
    text = text.lower()
    text = re.compile('rt @').sub('@',text,) #remove retweet (rt)
    text = re.sub(r"(?:\@|http|www.)\S+"," ",text) #remove url
    text = re.sub(r'[^\x00-\x7f]',r'',text)
    text = text.replace("\n"," ") #remove \n
    text = text.replace("_"," ")
    text= text.replace("<a","")
    text = text.replace("</a>","")
    text = text.replace("br />",'') 
    text = text.replace("&quot",'')
    text = re.sub(r'[^\w\s]','',text)
    rpt_regex = re.compile(r"(.)\1{1,}",re.IGNORECASE)
    text = rpt_regex.sub(r"\1\1",text) #remove repeated word
    text = text.strip() #trim head and tail
    text = re.sub(' +',' ',text)#remove multiple space
    text = re.sub(r'[~^0-9]', '', text) #remove digits

    return text

df_kotor['Text'] = df_kotor['Text'].apply(cleaningText)

df_kotor.head()

# membuat fungsi untuk menghapus karakter
import itertools

def remove_repeating_characters(text):
    return ''.join(''.join(s)[:1] for _, s in itertools.groupby(text))

# check fungsi tersebut
remove_repeating_characters('oooofel')

# membuat fungsi menghilangkan alpanumeric
import re

def remove_nonalphanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text

# Check fungsi tersebut
remove_nonalphanumeric('S,,,e!!H;;at')

#membuat fungsi untuk merubah data ke lower case

def to_lower_case(text):
    return text.lower()

# Check fungsi tersebut
to_lower_case('Test ujI CobA')

#mengabungkan ke 3 fungsi tersebut menjadi proses cleaning

def cleaning(text):
    text = remove_repeating_characters(text)
    text = remove_nonalphanumeric(text)
    text = to_lower_case(text)
    
    return text

# Check fungsi tersebut
cleaning('Saya\n\n\nTekun Belajar ')

#implementasi cleaning pada dataset "text" 

df_kotor['sentiment'] = df_kotor['Text'].apply(lambda x: cleaning(x))
df_kotor.head()

"""##Tokenizing"""

def tokenizingText(text): # Tokenizing or splitting a string, text into a list of tokens
    text = word_tokenize(text) 
    return text

from nltk.tokenize import word_tokenize

df_kotor['sentiment'] = df_kotor['sentiment'].apply(tokenizingText)

df_kotor.head(3)

"""##Filtering"""

def filteringText(text): # Remove stopwors in a text
    listStopwords = set(stopwords.words('indonesian'))
    filtered = []
    for txt in text:
        if txt not in listStopwords:
            filtered.append(txt)
    text = filtered 
    return text

from nltk.corpus import stopwords
list_stopwords = stopwords.words('indonesian')

#remove stopword pada list token
def stopwords_removal(words):
    return [word for word in words if word not in list_stopwords]

df_kotor['sentiment'] = df_kotor['sentiment'].apply(stopwords_removal)



"""##Stopword"""

#Menghapus Stopword Untuk Menghapus Kata-Kata Yang Kurang Bernilai Dalam Sebuah Document Dengan Beberapa Langkah Dibawah Ini

from nltk.corpus import stopwords

# ----------------------- NLTK Stopword Dengan Bahasa Indonesia -------------------------------
# get stopword indonesia
list_stopwords = stopwords.words('indonesian')


# ---------------------------- Menambahkan Stopword Secara Manual  ------------------------------------
# Tambahan Stopword
list_stopwords.extend(["dh", "rp","yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                       '&amp', 'yah'])


# Convert List Kedalam Dictionary
list_stopwords = set(list_stopwords)


#Fungsi Untuk Menghapus Stopword
def stopwords_removal(words):
    return [word for word in words if word not in list_stopwords]

df_kotor['sentiment'] = df_kotor['sentiment'].apply(stopwords_removal) 
df_kotor.head(3)

"""##Stemming"""

#stemming
def stemmingText(text): 
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = [stemmer.stem(word) for word in text]
    return text

# Commented out IPython magic to ensure Python compatibility.
# %%time
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# df_kotor['sentiment'] = df_kotor['sentiment'].apply(stemmingText)

df_kotor.head()

"""#Load data Bersih"""

df  =  pd.read_excel('/content/drive/MyDrive/project/svm/data4000.xlsx')

df.head(3)

#menghilangkan netral
df = df[df.label != 'neutral']
df.head(3)

df.drop(['Unnamed: 0', 'Unnamed: 3'], axis=1, inplace=True)

df.reset_index()
df.head(3)

df['label'].value_counts()

"""#EDA"""

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

show_wordcloud(df['text_clean'])

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
df_len = [len(x) for x in df['text_clean']]
pd.Series(df_len).hist()
plt.show()
pd.Series(df_len).describe()

#label encoding
from sklearn import preprocessing
def label_encoder(data):
    le = preprocessing.LabelEncoder()
    data = le.fit_transform(data)
    return data

df['label'] = label_encoder(df['label'])
df.head(3)

#negatif = 0 positif =1
df['label'].value_counts()

"""#preprocessing data bersih"""

#def tokenizingText(text): 
 #   text = word_tokenize(text) 
  #  return text

#def filteringText(text): # Remove stopwors in a text
 #   listStopwords = set(stopwords.words('indonesian'))
  #  filtered = []
   # for txt in text:
    #    if txt not in listStopwords:
     #       filtered.append(txt)
    #text = filtered 
    #return text

#from nltk.tokenize import word_tokenize
#df['text_clean'] = df['text_clean'].apply(tokenizingText)
#df['text_clean'] = df['text_clean'].apply(filteringText)

"""#Pembobotan TF-IDF"""

#fidf = TfidfVectorizer()
#response = tfidf.fit_transform(df['text_clean'])

#feature_names = tfidf.get_feature_names()
#for col in response.nonzero()[1]:
 #   print (feature_names[col], ' - ', response[0, col])

#import sklearn preprocessing 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

#Membuat object TF-IDF
tfidf = TfidfVectorizer()

#Membuat variabel x dan y
x_df = df['text_clean']
y_df = df['label']

x = np.array(x_df)
y = np.array(y_df)

#tfidf vectorizer
x_tfidf = tfidf.fit_transform(x)

#train test split using tfidfvectorizer 
train_x_tfidf, test_x_tfidf, train_y, test_y = train_test_split(x_tfidf, y, test_size=0.30, random_state=42)

#hasil pembobota
train_x_tfidf.shape

#hasil pembobotan
print(train_x_tfidf)

"""#Model SVM Biasa"""

from sklearn.svm import SVC
svm = SVC(C=10, kernel='linear')
model_svmbiasa = svm.fit(train_x_tfidf,train_y)

svm_prediction =  model_svmbiasa.predict(test_x_tfidf)

from sklearn.metrics import classification_report , confusion_matrix , accuracy_score
svm_acc = accuracy_score(svm_prediction,test_y)
svm_acc

print(classification_report(test_y, svm.predict(test_x_tfidf)))

from sklearn.metrics import multilabel_confusion_matrix
y_preds = model_svmbiasa.predict(test_x_tfidf)
multilabel_confusion_matrix(test_y, y_preds )

"""##cross val"""

from sklearn.model_selection import cross_val_score

scores = cross_val_score(model_svmbiasa, test_x_tfidf, test_y, cv=5)

print(scores)

"""#Model SVM RFE"""

from sklearn.feature_selection import RFE
from sklearn.svm import SVC
svc =  SVC(C=1, kernel="linear",gamma="scale", verbose=False, max_iter=1000, decision_function_shape="ovr")

rfe = RFE(svc, step=0.10)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_predict = rfe.fit(train_x_tfidf,train_y)
# featureidx = y_predict.get_support()

accuracy = []
accuracy.append(rfe.score(test_x_tfidf, test_y))

print(classification_report(test_y, y_predict.predict(test_x_tfidf)))

from sklearn.metrics import multilabel_confusion_matrix
y_preds = y_predict.predict(test_x_tfidf)
multilabel_confusion_matrix(test_y, y_preds )

"""##Confusion Matrix"""

print(classification_report(test_y, y_predict.predict(test_x_tfidf)))

#%%time
#from sklearn.metrics import accuracy_score
#from sklearn.model_selection import cross_val_score,train_test_split,LeaveOneOut


#X = np.array(x_df)
#y = np.array(y_df)

#loo = LeaveOneOut()
#loo.get_n_splits(X)
#LeaveOneOut()

#accuracy = []

#for train_index, test_index in loo.split(X):
#  X_train, X_test = pd.DataFrame(X[train_index]), pd.DataFrame(X[test_index]) # use this for training the model
#  y_train, y_test = y[train_index].ravel(), y[test_index].ravel() # use this for testing the model

#  SVM = LinearSVC()
#  model = SVM.fit(train_x_tfidf,train_y) # fit the model using training data
#  accuracy.append(SVM.score(test_x_tfidf, test_y))

#SVM_RFE_LE_mean = np.array(accuracy).mean()

#print(classification_report(test_y, model.predict(test_x_tfidf)))

#cm = classification_report(test_y, model.predict(test_x_tfidf))

#print(cm)

# Commented out IPython magic to ensure Python compatibility.
#mengimplementasikan testing data dan hasil prediksi dalam confusion matrix
cm = confusion_matrix(test_y, y_preds)
 
#membuat plotting confusion matrix
# %matplotlib inline
plt.figure (figsize=(10,7))
sns.heatmap(cm, annot=True)
plt.xlabel('Prediksi')
plt.ylabel('Benar')

#from sklearn.model_selection import KFold


#kfold=KFold(n_splits=5, shuffle=True, random_state=0)


#linear_svc=SVC(kernel='linear')


#linear_scores = cross_val_score(linear_svc, test_x_tfidf, test_y, cv=kfold)

#print('Stratified cross-validation scores with linear kernel:\n\n{}'.format(linear_scores))

"""##Cross Validation"""

from sklearn.model_selection import cross_val_score

scores = cross_val_score(y_predict, test_x_tfidf, test_y, cv=10)

print(scores)

"""##ROC AUC"""

# plot ROC Curve
from yellowbrick.classifier import ROCAUC
from sklearn.metrics import roc_curve

binary_classifiers = [              
    SVC()                  
]
for classifier in binary_classifiers:
    oz = ROCAUC(classifier, micro=False, macro=False, per_class=False)
    oz.fit(train_x_tfidf,train_y)
    oz.score(test_x_tfidf, test_y)
    g = oz.show()

