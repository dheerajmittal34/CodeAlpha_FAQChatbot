# CodeAlpha FAQ Chatbot

A web-based FAQ chatbot for the fictional **EduLearn** online course platform. It uses Natural Language Processing (NLP) to match a user's question to the most relevant stored FAQ answer.

## Features

- Simple and responsive chat user interface
- FAQ data stored in a JSON file
- Text cleaning and tokenization using **NLTK**
- Stop-word removal and stemming using NLTK's `PorterStemmer`
- FAQ matching with **TF-IDF vectorization** and **cosine similarity**
- Displays the best matching FAQ question for transparency
- Friendly fallback answer when no close match is found

## Technology used

- Python
- Flask
- NLTK
- scikit-learn
- HTML, CSS, and JavaScript

## Run locally

1. Open Command Prompt in this project folder.
2. Install the required libraries:

   ```cmd
   pip install -r requirements.txt
   ```

3. Start the application:

   ```cmd
   python app.py
   ```

4. Open this link in a browser:

   ```text
   http://127.0.0.1:5000
   ```

## Project structure

```text
CodeAlpha_FAQChatbot/
├── app.py                 # Flask app, NLP preprocessing, and cosine matching
├── faq_data.json          # Questions and answers used by the chatbot
├── requirements.txt       # Python dependencies
├── templates/index.html   # Chat UI
└── static/
    ├── style.css          # Design and responsive layout
    └── script.js          # Browser chat interaction
```
