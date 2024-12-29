from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import nltk

# Initialize Flask app
app = Flask(__name__)

# Ensure necessary NLTK resources are downloaded
nltk.download('stopwords')

# Hybrid Spam Filter class
class HybridSpamFilter:
    def __init__(self, heuristic_file, reputation_file):
        self.vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
        self.model = MultinomialNB()
        self.heuristic_rules = self.load_heuristic_rules(heuristic_file)
        self.blacklisted_domains = self.load_reputation_list(reputation_file)

    def load_heuristic_rules(self, file_path):
        with open(file_path, 'r') as file:
            return [line.strip().lower() for line in file.readlines()]

    def load_reputation_list(self, file_path):
        with open(file_path, 'r') as file:
            return [line.strip().lower() for line in file.readlines()]

    def train_model(self, training_file):
        data = pd.read_csv(training_file)
        X = self.vectorizer.fit_transform(data['text'])
        self.model.fit(X, data['spam'])

    def heuristic_filter(self, email):
        for keyword in self.heuristic_rules:
            if keyword in email.lower():
                return True
        return False

    def reputation_filter(self, sender_email):
        domain = sender_email.lower().strip().split("@")[-1]
        return domain in self.blacklisted_domains

    def predict(self, email, sender_email):
        if self.heuristic_filter(email):
            return "Spam"
        if self.reputation_filter(sender_email):
            return "Spam"
        email_vector = self.vectorizer.transform([email])
        prediction = self.model.predict(email_vector)
        return "Spam" if prediction[0] == 1 else "Not Spam"

# Initialize filter system
heuristic_file = "heuristic_rules.txt"
reputation_file = "blacklisted_domains.txt"
training_file = "training_data.csv"

filter_system = HybridSpamFilter(heuristic_file, reputation_file)
filter_system.train_model(training_file)

@app.route('/')
def home():
    return render_template('frontend.html')

@app.route('/classify', methods=['POST'])
def classify_email():
    data = request.get_json()
    email_content = data.get('emailContent')
    sender_email = data.get('senderEmail')
    result = filter_system.predict(email_content, sender_email)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
