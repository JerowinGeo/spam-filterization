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
#### Why Remove Stopwords?
Stopwords can reduce confusion in text data when analyzing or building models, as they don't contribute much to the context or meaning.

### Flask App Initialization
```
app = Flask(__name__)
```

### Spam Filter Class
```
class HybridSpamFilter:
```

as it is a hybrid filter it contain more than one type of filter in this filter it contains the following below;

#### Heuristic Filtering: 
Detects spam based on specific keywords. it uses the keywords in the data set that is loaded and classifies the mail.
#### Reputation Filtering: 
finds the emails from known spam domains. that is it classify based on the senders email(for example if the email is from a suspicious sender the mail will be considered a spam.)
#### Machine Learning: 
Uses a Naive Bayes model trained on labeled email data.(it uses the given dataset and trains the model to classify the spam mail)

### Constructor: Initialization
```
def __init__(self, heuristic_file, reputation_file):
    self.vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
    self.model = MultinomialNB()
    self.heuristic_rules = self.load_heuristic_rules(heuristic_file)
    self.blacklisted_domains = self.load_reputation_list(reputation_file)
```
#### self.vectorizer:
Prepares to convert email text into numerical vectors.that is it converts the text to a matrix format by using known vocabularies
#### self.model:
A Naive Bayes classifier instance. it uses the training and exisiting dataset and classifies.
#### self.heuristic_rules: 
Loads spam-related keywords from a file. this dataset is used in heuristic filter.
#### self.blacklisted_domains:
Loads a list of blacklisted email domains. this dataset is used in reputation filter.

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
first it checks for heuristic filter and if it is spam it shows as spam .
orelse it goes and checks using reputation filtering if it true it shows spam.
then go for the third type of filter which is using naive bayes and it is true, it shows as spam ,if it is not spam it shows as not spam.

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
it is used to bind the url path with the backend that is to connect frontend program(html program) with backend.

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





