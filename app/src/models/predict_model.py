from src.features.build_features import preprocessing, join_words_processing

def predict(review: str, model):
    review_cleaned= preprocessing(review)
    review_cleaned_join = join_words_processing(review_cleaned)

    prediction = model.predict([review_cleaned_join])[0]

    sentiment_value = get_sentiment(prediction)
    return sentiment_value

def get_sentiment(sentiment: int):
    sent = {
        -1: "negative",
        1: "positive",
        0: "neutral"
    }
    return sent.get(sentiment)