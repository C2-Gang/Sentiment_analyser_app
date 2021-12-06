from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from src.features.build_features import preprocessing, join_words_processing
from src.utils import directory_path, dump_json_object, dump_pickle
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,f1_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.utils import directory_path, load_pickle

def predict(review: str, model_type: str):
    review_cleaned= preprocessing(review)
    review_cleaned_join = join_words_processing(review_cleaned)
    model_path = f"{directory_path}models/{model_type}/{model_type}"
    model = load_pickle(model_path)

    prediction = model.predict([review_cleaned_join])[0]

    sentiment_value = get_sentiment(prediction)
    print(sentiment_value)
    return sentiment_value




def get_sentiment(sentiment: int):
    sent = {
        0: "negative",
        1: "positive"
    }
    return sent.get(sentiment)