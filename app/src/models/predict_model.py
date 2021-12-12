from src.features.build_features import preprocessing, join_words_processing

def predict(review: str, model):
    """This function allows to predict the sentiment of a text with a chosen model.

    :param review: the text we want to know the sentiment
    :type review: str
    :param model: the model we want to apply
    :type model: str
    :return: sentiment value (-1, 0 or 1)
    :rtype: int
    """
    try:
        review_cleaned = preprocessing(review)
        review_cleaned_join = join_words_processing(review_cleaned)

        prediction = model.predict([review_cleaned_join])[0]

        sentiment_value = get_sentiment(prediction)
        return sentiment_value
    except Exception:
        return "error null string."


def get_sentiment(sentiment: int):
    """This function allows to convert int sentiment into string sentiment.

    :param sentiment: the int sentiment we want to convert into string
    :type sentiment: int
    :return: sentiment string ("negative", "positive" or "neutral")
    :rtype: str
    """
    sent = {
        -1: "negative",
        1: "positive",
        0: "neutral"
    }
    return sent.get(sentiment)