from flask import Flask, render_template, request, jsonify
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
    review = str(request.args["text"])
    sentiment = predict(review, model)
    return jsonify(sentiment)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)

