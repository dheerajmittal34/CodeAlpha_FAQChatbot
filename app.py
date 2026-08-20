"""FAQ chatbot using NLTK preprocessing and cosine-similarity matching."""

import json
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from nltk.stem import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_data.json"
app = Flask(__name__)


class FAQChatbot:
    """Matches a user's question with the most similar stored FAQ question."""

    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
        "i", "in", "is", "it", "of", "on", "or", "the", "this", "to", "was", "what",
        "when", "where", "which", "who", "why", "with", "you", "your", "can", "do",
        "does", "have", "my", "me", "about", "please",
    }

    def __init__(self, faq_items):
        self.faq_items = faq_items
        self.stemmer = PorterStemmer()
        self.vectorizer = TfidfVectorizer(analyzer=self.preprocess, ngram_range=(1, 2))
        self.question_vectors = self.vectorizer.fit_transform(
            [item["question"] for item in self.faq_items]
        )

    def preprocess(self, text):
        """Clean, tokenize, remove basic stop words, and stem the input text."""
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        tokens = wordpunct_tokenize(cleaned_text)
        return [
            self.stemmer.stem(token)
            for token in tokens
            if token.isalnum() and token not in self.STOP_WORDS
        ]

    def get_response(self, user_question):
        query_vector = self.vectorizer.transform([user_question])
        similarity_scores = cosine_similarity(query_vector, self.question_vectors).flatten()
        best_index = similarity_scores.argmax()
        confidence = float(similarity_scores[best_index])

        if confidence < 0.12:
            return {
                "answer": (
                    "I could not find a close FAQ answer for that question. "
                    "Please try asking about courses, payments, certificates, passwords, "
                    "downloads, refunds, or support."
                ),
                "matched_question": None,
                "confidence": 0,
            }

        best_match = self.faq_items[best_index]
        return {
            "answer": best_match["answer"],
            "matched_question": best_match["question"],
            "confidence": round(confidence * 100),
        }


with FAQ_FILE.open(encoding="utf-8") as file:
    faq_data = json.load(file)

chatbot = FAQChatbot(faq_data)


@app.route("/")
def home():
    return render_template("index.html", suggested_questions=[item["question"] for item in faq_data[:4]])


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("message", "")).strip()

    if not question:
        return jsonify({"error": "Please type a question first."}), 400
    if len(question) > 400:
        return jsonify({"error": "Please keep your question under 400 characters."}), 400

    return jsonify(chatbot.get_response(question))


if __name__ == "__main__":
    app.run(debug=True)
