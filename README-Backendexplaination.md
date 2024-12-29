### first we need to import some modules and libararies
```
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import nltk
```
#### Flask:
For web development.
#### pandas:
For managing and analyzing CSV data.
#### scikit-learn:
For text processing and machine learning.
#### nltk: 
For natural language processing and text filtering.
Provides a list of stopwords to filter out common words.
#### nltk.download('stopwords'): 
Ensures stopwords are available

What are Stopwords?
Definition: Stopwords are common words in a language (e.g., "the", "is", "in", "and") that usually do not carry significant meaning and are often excluded from text processing tasks to focus on more meaningful words.
Why Remove Stopwords?: Stopwords can reduce noise in text data when analyzing or building models, as they don't contribute much to the context or meaning.

Flask App Initialization
```
app = Flask(__name__)
```
Spam Filter Class
```
class HybridSpamFilter:
```
A class combining:

Heuristic Filtering: Detects spam based on specific keywords.
Reputation Filtering: Flags emails from known spam domains.
Machine Learning: Uses a Naive Bayes model trained on labeled email data.

Constructor: Initialization
```
def __init__(self, heuristic_file, reputation_file):
    self.vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
    self.model = MultinomialNB()
    self.heuristic_rules = self.load_heuristic_rules(heuristic_file)
    self.blacklisted_domains = self.load_reputation_list(reputation_file)
```
#### self.vectorizer:
Prepares to convert email text into numerical vectors.
#### self.model:
A Naive Bayes classifier instance.
#### self.heuristic_rules: 
Loads spam-related keywords from a file.
#### self.blacklisted_domains:
Loads a list of blacklisted email domains.

### Loading Heuristic Rules and Reputation Data
```
def load_heuristic_rules(self, file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file.readlines()]

def load_reputation_list(self, file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file.readlines()]
```




