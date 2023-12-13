import requests
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
import re
spell = SpellChecker()

lemmatizer = WordNetLemmatizer()

products = requests.get('https://xfood.onrender.com/products').json()

titles = []
ignore_words = ["?","!",","," "]


for product in products:
    formatted_title = product["title"].replace(" ","-")
    titles.append(formatted_title)

print(titles)

def extract_numeric_values(input_string):
    # Define a regular expression pattern to match numeric values
    pattern = r'\d+'

    # Use re.findall to find all matches of the pattern in the input string
    matches = re.findall(pattern, input_string)

    # Convert the matched strings to integers
    numeric_values = [int(match) for match in matches]

    return numeric_values


def find_closest_keyword(user_input, titles):
    
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

           

userInput = "I want 23 Anil Stylee and-3 The-Rasfari"
userInput = userInput.replace(" ",'-')

productIndexes = find_closest_keyword(userInput,titles)
qtys = extract_numeric_values(userInput)

for i, index in enumerate(productIndexes):
    print(titles[index],"quantaty : ",qtys[i] )