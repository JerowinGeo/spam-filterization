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

##### What are Stopwords?
Stopwords are common words in a language (e.g., "the", "is", "in", "and") that usually do not carry significant meaning and are often excluded from text processing tasks to focus on more meaningful words.
Why Remove Stopwords?: Stopwords can reduce noise in text data when analyzing or building models, as they don't contribute much to the context or meaning.

### Flask App Initialization
```
app = Flask(__name__)
```
### Spam Filter Class
```
class HybridSpamFilter:
```
### A class combining:

#### Heuristic Filtering: 
Detects spam based on specific keywords.
#### Reputation Filtering: 
Flags emails from known spam domains.
#### Machine Learning: 
Uses a Naive Bayes model trained on labeled email data.

### Constructor: Initialization
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

### Training the Model
```
def train_model(self, training_file):
    data = pd.read_csv(training_file)
    X = self.vectorizer.fit_transform(data['text'])
    self.model.fit(X, data['spam'])
```
#### Loads a CSV containing:
text: Email content.
spam: Labels (1 for spam, 0 for not spam).
Converts email text into a numeric matrix (X) and trains the model.

### Heuristic and Reputation Filters
```
def heuristic_filter(self, email):
    for keyword in self.heuristic_rules:
        if keyword in email.lower():
            return True
    return False

def reputation_filter(self, sender_email):
    domain = sender_email.lower().strip().split("@")[-1]
    return domain in self.blacklisted_domains
```
### Heuristic Filter: 
Checks if any spam-related keyword exists in the email content.
### Reputation Filter:
Flags emails from domains in the blacklist.

### Prediction Logic
```
def predict(self, email, sender_email):
    if self.heuristic_filter(email):
        return "Spam"
    if self.reputation_filter(sender_email):
        return "Spam"
    email_vector = self.vectorizer.transform([email])
    prediction = self.model.predict(email_vector)
    return "Spam" if prediction[0] == 1 else "Not Spam"
```
### Initialize the Filter
```
heuristic_file = "heuristic_rules.txt"
reputation_file = "blacklisted_domains.txt"
training_file = "training_data.csv"

filter_system = HybridSpamFilter(heuristic_file, reputation_file)
filter_system.train_model(training_file)
```

### Flask Routes
```
@app.route('/')
def home():
    return render_template('frontend.html')
```
Renders an HTML file (frontend.html) that serves as the user interface.

### Classify Email
```
@app.route('/classify', methods=['POST'])
def classify_email():
    data = request.get_json()
    email_content = data.get('emailContent')
    sender_email = data.get('senderEmail')
    result = filter_system.predict(email_content, sender_email)
    return jsonify({"result": result})
```
#### Input: 
Accepts a POST request with email content and sender email in JSON format.
#### Processing: 
Passes the input to the HybridSpamFilter's predict method.
#### Output: 
Returns the classification result (Spam or Not Spam) as JSON.

### Run the Application
```
if __name__ == '__main__':
    app.run(debug=True)
```





