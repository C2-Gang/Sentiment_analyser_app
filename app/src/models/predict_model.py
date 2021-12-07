from src.features.build_features import preprocessing, join_words_processing
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