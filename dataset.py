import json
from sutime import SUTime
import csv
import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
nltk.download('stopwords') 
nltk.download('punkt')
nltk.download('vader_lexicon')
stop_words = set(stopwords.words('english'))

import tensorflow as tf
import pandas as pd

from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures

devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(devices[0], True)

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model.load_weights("./movie_reviews.h5")



with open('TMDb_updated.csv',encoding="utf8") as file:
    f = open('dataset.csv','a',encoding="utf8")
    f.truncate(0)
    reader = csv.reader(file)
    sutime = SUTime(mark_time_ranges=True, include_range=True)
    results=[]
    for row in reader:
        t=row[2]
        csv=row[2]
        t=t.lower()
        words = t.split()
        text=""
        for r in words:  
            if not r in stop_words:  
                text+=r+" "
        var=""
        csv=csv.replace('"',"~")
        textJson=json.dumps(sutime.parse(text), sort_keys=True, indent=4)
        if len(textJson)>3:
            tf_batch = tokenizer(row[1], max_length=128, padding=True, truncation=True, return_tensors='tf')
            tf_outputs = model(tf_batch)
            tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
            labels = ['Negative','Positive']
            label = tf.argmax(tf_predictions, axis=1)
            label = label.numpy()
            expressi=json.loads(textJson)
            despartireText=text
            despartireText=despartireText.replace("?",".")
            despartireText=despartireText.replace("!",".")
            despartireText=despartireText.split(".")
            f.write(row[0]+",\""+row[1]+"\",\""+csv+ "\","+str(labels[label[0]])+",\"")
            for i in range(0,len(expressi)):
                if i==len(expressi)-1:
                    aux=expressi[i].get("text")
                    aux=aux.replace('"',"~")
                    f.write(expressi[i].get("text"))
                else:
                    aux=expressi[i].get("text")
                    aux=aux.replace('"',"~")
                    f.write(expressi[i].get("text")+' + ')
            f.write("\", \"")
            sentimentePropoziti=""
            for i in range(0,len(expressi)):
                for j in range(0,len(despartireText)):
                    if despartireText[j].find(expressi[i].get("text"))!=-1:
                        tf_batch = tokenizer(despartireText[j], max_length=128, padding=True, truncation=True, return_tensors='tf')
                        tf_outputs = model(tf_batch)
                        tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
                        label = tf.argmax(tf_predictions, axis=1)
                        label = label.numpy()
                        sentimentePropoziti+=(str(labels[label[0]])+" + ")
            sentimentePropoziti = sentimentePropoziti[:len(sentimentePropoziti) - 2]
            f.write(sentimentePropoziti)
            f.write("\", \n")