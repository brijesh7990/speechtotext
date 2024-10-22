from flask import Flask, request, jsonify
import requests
import json
import base64
from flask_cors import CORS
import sqlite3
from googletrans import Translator
from nltk.sentiment import SentimentIntensityAnalyzer



app = Flask(__name__)
CORS(app)

sia = SentimentIntensityAnalyzer()
translator = Translator()

# Translate text
translation = translator.translate("નરેન્દ્ર મોદી", src='gu', dest='en')

# Access the translated text
translated_text = translation.text
print("Translated Text:", translated_text)

# Perform sentiment analysis on the translated text
if translated_text:  # Check if translation was successful
    sentiment_scores = sia.polarity_scores(translated_text)
    compound_score = sentiment_scores['compound']
    print("compound_score", compound_score)
else:
    print("Translation failed or returned None.")
