import requests
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
spell = SpellChecker()

lemmatizer = WordNetLemmatizer()






           

userInput = "I want 23 Anil Stylee and-3 The-Rasfari"
userInput = userInput.replace(" ",'-')


