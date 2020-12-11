from flask import Flask, jsonify
import pandas as pd
import joblib
import spacy
import en_core_sci_lg
from spacy.lang.en.stop_words import STOP_WORDS
import string
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# LOAD NLP FROM PICKLE FILE
# nlp = joblib.load('nlp.pkl')

# Create a countvectorizer
# cv = CountVectorizer(max_df = 0.95, min_df = 2, stop_words = 'english')
# cv = CountVectorizer(max_df = 0.95, stop_words = 'english')


nlp = en_core_sci_lg.load(disable=['tagger', 'ner'])
nlp.max_length = 7000000

# LOAD COUNTVECTOR
cv = joblib.load('my_api/cv.pkl')

# LOAD LDA MODEL
lda = joblib.load('my_api/lda.pkl')

# LOAD COVIDDF
df = joblib.load('my_api/covid.pkl')

# LOAD NUMTOPICS
num_topics = joblib.load('my_api/num_topics.pkl')

stop_words = list(STOP_WORDS)
medical_stop_words = ['doi', 'preprint', 'copyright', 'peer', 'reviewed', 'org', 'https', 'et', 'al',
                      'author', 'figure', 'rights', 'reserved', 'permission', 'used', 'using',
                      'biorxiv', 'medrxiv', 'license', 'fig', 'fig.', 'al.', 'Elsevier', 'PMC', 'CZI', 'www']

stop_words.extend(medical_stop_words)  # Converge the 2 lists
stop_words = list(set(stop_words))  # Remove duplicates


@app.route("/")
@cross_origin()
def hello():
    return "Hello World!"


@app.route("/classify/<string:newTextData>")
@cross_origin()
def classifyNewData(newTextData):
    newCovidDF = pd.DataFrame(df)
    # newCovidDF = pd.DataFrame(covidDF)

    # nlp = outnlp

    # LOAD NLP FROM PICKLE FILE
    # nlp = joblib.load('nlp.pkl')
    # nlp = en_core_sci_lg.load(disable=['tagger','ner'])
    # nlp.max_length = 7000000

    tokens = nlp(newTextData)
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]

    # argmax() returns the indices of the maximum values
    # For each word it is saying which has the highest chance of topic it belongs to
    # It then appends the index that to the freq_lst, so that we can get the frequency of topics by body of text

    freq_lst = [i.argmax() + 1 for i in lda.transform(cv.transform(tokens))]
    # freq_lst = []
    # for i in lda.transform(cv.transform(tokens)):
    #     #print(i)
    #     freq_lst.append(i.argmax())

    cnt = Counter(freq_lst)
    # Creates a frequency counter
    # ex: Counter({4: 94, 3: 408, 0: 240, 2: 262, 5: 857, 1: 238, 6: 111})

    # CREATE DICTIONARY dynamically based on the number of topics
    temp_dict = {}

    for i in range(1, num_topics + 1):
        temp_dict['topic_' + str(i)] = []

    # Counts total occurrences, so that we can get percentages for occurences per topic
    # Returns a dictionary with the highest occuring, highest rated topics
    total = sum(cnt.values())

    for i in range(1, len(temp_dict) + 1):
        # print(i)
        try:
            temp_dict['topic_' + str(i)].append(cnt[i] / total)
        except:
            temp_dict['topic_' + str(i)].append(None)

    # Filter for data that has values
    lstfilters = []  # Will capture filteres for the covidDF
    filteredDict = {}  # will create a new dict with sorted values, Can be used to display confidence levels for request
    for key in sorted(temp_dict, key=temp_dict.get, reverse=True):
        # print(temp_dict[key][0])
        if temp_dict[key][0] > 0:
            # print(key)
            filteredDict[key] = [temp_dict[key][0]]
            lstfilters.append(f'(newCovidDF.{key} >= {temp_dict[key][0]})')

    # Create a filtered DF
    for i in lstfilters:
        if len(newCovidDF[eval(i)]) > 0:
            newCovidDF = newCovidDF[eval(i)]

    newCovidDF['matched_topics'] = json.dumps(filteredDict)

    # We can choose top 5 recommendations
    # We are sorting by the filtered dictionary, highest match first

    responseJson = newCovidDF.sort_values(by=[i for i in filteredDict.keys()], ascending=False).head(5)[
        ['title', 'authors', 'doi', 'matched_topics']].to_json(orient='records')
    # responseJson = newCovidDF.sort_values(by=[i for i in filteredDict.keys()], ascending=False).head(5)[['title','authors','doi']].to_dict('records')

    # responseJson['requestValues'] = filteredDict

    return responseJson


if __name__ == '__main__':
    app.run()
