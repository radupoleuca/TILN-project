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
import spacy
nlp = spacy.load("en_core_web_sm")

# from nltk.sentiment import SentimentIntensityAnalyzer
# sia = SentimentIntensityAnalyzer()
with open('TMDb_updated.csv',encoding="utf8") as file:
    f = open('date.txt','a',encoding="utf8")
    f.truncate(0)
    reader = csv.reader(file)
    sutime = SUTime(mark_time_ranges=True, include_range=True)
    results=[]
    for row in reader:
        t=row[2]
        t=t.lower()
        words = t.split()
        text=""
        for r in words:  
            if not r in stop_words:  
                text+=r+" "
        var=""
        # doc = nlp(text)
        # token_list = [token for token in doc]
        # lemmas = [f"Token: {token}, lemma: {token.lemma_}" for token in token_list ]
        #token_list[0].vector
        # if sia.polarity_scores(text)["compound"]>0:
        #     var="Pozitiv"
        # elif sia.polarity_scores(text)["compound"]<0:
        #     var="Negativ"
        # else:
        #     var="Neutral"
        textJson=json.dumps(sutime.parse(text), sort_keys=True, indent=4)
        if len(textJson)>3:
            f.write(row[0]+"\n"+textJson+"\n")
    f.close()
