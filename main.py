import nltk
import numpy as np
import json
import re
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import pickle
import random
from fuzzywuzzy import fuzz
import requests
import tensorflow as tf
from spellchecker import SpellChecker
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2EyMTQ0M2U0MDgwYzliNjMzYWZkMiIsImVtYWlsIjoiZmFkeW5hYmlsNzAxQGdtYWlsLmNvbSIsImZpcnN0bmFtZSI6IkZhZHkiLCJsYXN0bmFtZSI6Ik5hYmlsIiwiaWF0IjoxNzAyNTAyODM3LCJleHAiOjE3MDI1ODkyMzd9.UYpUsFduCtVABsn7s4z6mPTnQOH4dCXxuXhSpa8b9ug"

lemmatizer = WordNetLemmatizer()
spell = SpellChecker()


intents = json.loads(open("intents.json").read())

model = load_model("chatbot_model.h5")

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

data_file = open("intents.json").read()
intents = json.loads(data_file) 

lemmatizer = WordNetLemmatizer()




categories = ["burger","kids-meals","dessert","drinks","chicken","appetizers"]
ignore_words = ["?","!",","]

def get_correction(user_input):
    corrected_input = ''
    for i, word  in enumerate(user_input.split(' ')):
        if i == len(user_input.split(' ')) - 1:
            corrected_input += f'{spell.correction(word)}'
        else:
            corrected_input += f'{spell.correction(word)} '

    print(corrected_input)
    return corrected_input


def find_closest_title(user_input, titles):
    
    temp_similarity = 0
    top_similarity_index = []
    quantaties = []

    for i, keyword in enumerate(titles):
        for string in user_input.lower().split(' '):
          if(string in ignore_words):
              break
        current_similarity = fuzz.partial_ratio(f"{string.lower()} ",keyword.lower())
        if(current_similarity > 70):
            temp_similarity = i
            top_similarity_index.append(i)
    
    if top_similarity_index:
        return top_similarity_index
    else :
        return None
    
def extract_numeric_values(input_string):
    # Define a regular expression pattern to match numeric values
    pattern = r'\d+'

    # Use re.findall to find all matches of the pattern in the input string
    matches = re.findall(pattern, input_string)

    # Convert the matched strings to integers
    numeric_values = [int(match) for match in matches]

    return numeric_values

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
    corrected_sentence = get_correction(sentence)
    sentence_words = nltk.word_tokenize(corrected_sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#done

# Convert user_input

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

# Predict output

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

    print(classes[predicted_index])


    #If menu
    if classes[predicted_index] == "menu":
        closest_keyword = find_closest_keyword(sentence,categories,threshold=70)
        if closest_keyword is not None:
            products = requests.get(f'https://xfood.onrender.com/products?category={categories[closest_keyword]}').json()
            if len(products) == 0:
                return "We're out of stock"
            return({"msg":products,"function":"Menu"})
        

        products = requests.get('https://xfood.onrender.com/products').json()
        if len(products) == 0:
                return "We're out of stock"
       
        return({"msg":products,"function":"Menu"})

    
    #IF Order
    
    if classes[predicted_index] == "order":
        
        products = requests.get('https://xfood.onrender.com/products').json()

        titles = []

        for product in products:
            formatted_title = product["title"].replace(" ","-")
            titles.append(formatted_title)

        print(titles)

        sentence = sentence.replace(" ","-")
        print(sentence)
        productIndexes = find_closest_title(sentence,titles)
        print(productIndexes)
        qtys = extract_numeric_values(sentence)
        cart= []
        botString = ""
        for i, index in enumerate(productIndexes):
            if len(productIndexes) == 1:
                botString += f"{titles[index]} has been added to cart, Please go to payment page to checkout !"
            else:
                if i == 0:
                    botString += f"{titles[index]}, "

                elif i != (len(productIndexes) - 1) and i > 0:
                    botString += f"{titles[index]}, "
                elif i == (len(productIndexes) - 1):
                    botString += f"and {titles[index]} has been added to cart, Please go to payment page to checkout !"

            cartItem = {
                "productId":products[index]["_id"],
                "productQuantity":qtys[i],
                "price":products[index]["price"],
                "size":150,
                "extras":[]

            }
            cart.append(cartItem)
        

        return({"msg":cart,"function":"Order","botString":botString})
            

    return {"msg":output,"function":None}

