first we need to import some modules and libararies
```
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import nltk
```
####Flask:
For web development.
####pandas:
For managing and analyzing CSV data.
scikit-learn:
For text processing and machine learning.
####nltk: 
For natural language processing and text filtering.
Provides a list of stopwords to filter out common words.
####nltk.download('stopwords'): 
Ensures stopwords are available

What are Stopwords?
Definition: Stopwords are common words in a language (e.g., "the", "is", "in", "and") that usually do not carry significant meaning and are often excluded from text processing tasks to focus on more meaningful words.
Why Remove Stopwords?: Stopwords can reduce noise in text data when analyzing or building models, as they don't contribute much to the context or meaning.
