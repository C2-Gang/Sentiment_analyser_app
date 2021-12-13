import time
from flask import Flask, render_template, request, jsonify, g
from src.models.predict_model import predict
from src.utils import directory_path, load_pickle
<<<<<<< HEAD
import os
=======
import json

>>>>>>> develop

app = Flask(__name__, template_folder='templates')
model_type = "linearsvc"
#path = f"./{model_type}"
path = f"./models/{model_type}/{model_type}"

model = load_pickle(path)


@app.route('/')
def home():
    """This function send data from HTML form to a Python script in Flask

    :return: render_template('form.html')
    :rtype:
    """
    return render_template('form.html')


@app.route('/handle',methods=['GET'])
def handle():
    """This function retrieve the text from the user, apply on it the prediction and return the sentiment.

    :return: render_template
    :rtype: render_template
    """
    review = str(request.args["piecetext"])
    sent = predict_text(review)
    return render_template('results.html', content = sent['text'] ,prediction = sent['sentiment'])


def predict_text(text: str):
    """This function do sentiment prediction on a text and return the sentiment.

    :param text: text to predict
    :type text: str
    :return: dict sent
    :rtype: dict
    """
    if ((text == '') or (text == 'None') ):
        sentiment = 'empty ! Try again'
    else:
        sentiment = predict(text, model)
    sent = {
        "text": text,
        "sentiment": sentiment}
    return sent


@app.route('/json_handle',methods=['GET'])
def json_handle():
    """This function retrieve the text from the user, apply on it the prediction and return the sentiment.
    :return: jsonify(sentiment)
    :rtype: json
    """
    review = str(request.args["piecetext"])
    return json_predict_text(review)


def json_predict_text(text: str):
    """This function do sentiment prediction on a text and return a json file.

    :param text: text to predict
    :type text: str
    :return: jsonify(sent)
    :rtype: json
    """
    if ((text == '') or (text == 'None') ):
        sentiment = 'empty ! Try again'
    else:
        sentiment = predict(text, model)
    sent = {
        "text": text,
        "sentiment": sentiment}
    return jsonify(sent)


# times
@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = time.time() - g.start
    g.request_time = diff
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)