from flask import Flask, redirect, render_template, url_for, request, jsonify
import numpy as np
import spacy
from cleantext import clean
import tensorflow as tf

nlp = spacy.load('en_core_web_sm')


def clean_text(text):   # The exact same function I have used during text preprocessing
    text = clean(text, lower=True, no_line_breaks=True, no_urls=True, no_emails=True,
                 no_phone_numbers=True, no_numbers=True, no_currency_symbols=True, no_punct=True,
                 no_emoji=True, no_digits=True, replace_with_currency_symbol="", replace_with_url="",
                 replace_with_email="", replace_with_number="", replace_with_digit="")
    doc = nlp(text)
    text = [token.lemma_ for token in doc if token.lemma_ !=
            "I" and not token.is_stop]
    return " ".join(text)


model = tf.keras.models.load_model(
    "./saved_models/lstm_model.keras")   # Loading the pre-trained model

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        review = request.json['text']
        cleaned_review = clean_text(review)
        pred = model.predict([cleaned_review])
        if pred[0][0] > 0.5:
            return jsonify('Positive')
        else:
            return jsonify('Negative')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
