import time
from flask import Flask, render_template, request, jsonify, g
from src.models.predict_model import predict
from src.utils import directory_path, load_pickle


app = Flask(__name__, template_folder='templates')
model_type = "linearsvc"
path = f"{directory_path}models/{model_type}/{model_type}"
model = load_pickle(path)

@app.route('/')
def home():
    return render_template('form.html')


@app.route('/handle',methods=['GET'])
def handle():
    review = str(request.args.get("piecetext"))
    sentiment = predict(review, model)
    sentiment_result = {
        "sentiment": sentiment
    }

    return jsonify(sentiment_result)


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

