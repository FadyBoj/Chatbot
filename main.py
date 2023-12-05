import nltk
import numpy as np
import json
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import pickle
import random
from fuzzywuzzy import fuzz
import requests

lemmatizer = WordNetLemmatizer()

intents = json.loads(open("intents.json").read())

model = load_model("chatbot_model.h5")

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

data_file = open("intents.json").read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

categories = ["burger","kids-meals","dessert","drinks"]
ignore_words = ["?","!",","]

def find_closest_keyword(user_input, keywords, threshold=70):
    
    temp_similarity = 0
    top_similarity_index = 0

    for i, keyword in enumerate(keywords):
        for string in user_input.lower().split(' '):
          if(string in ignore_words):
              break
          current_similarity = fuzz.partial_ratio(f"{string.lower()} ",keyword.lower())
          if(current_similarity > temp_similarity):
              temp_similarity = current_similarity
              top_similarity_index = i



    if temp_similarity >= threshold:
        return top_similarity_index
    else:
        return None

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#done

def process_sentence(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = process_sentence(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    predicted_index = np.argmax(res)
    tag = classes[predicted_index]

    index=  0

    for i, intent in enumerate(intents["intents"]) :
        if intent["tag"] == tag:
            index = i
    output = random.choice(intents["intents"][index]["responses"])


    if classes[predicted_index] == "menu":
        closest_keyword = find_closest_keyword(sentence,categories,threshold=70)
        if closest_keyword is not None:
            products = requests.get(f'https://xfood.onrender.com/products?category={categories[closest_keyword]}').json()
            if len(products) == 0:
                return "We're out of stock"
            return products
        

        products = requests.get('https://xfood.onrender.com/products').json()
        if len(products) == 0:
                return "We're out of stock"
       
        return products
    

    return output


