from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from src.utils import directory_path, dump_json_object, dump_pickle
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,f1_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

analyser = SentimentIntensityAnalyzer()

def sentiment(sentence, type):
    sentiment = []
    sum_sent = 0
    for sent in sentence:
        sent = ' '.join(sent)
        score = analyser.polarity_scores(sent)
        sentiment.append(score[type])
        sum_sent += score[type]

    return sum_sent / len(sentiment)

def get_sentiment(df: pd.DataFrame, column: str):
    df['Positive'] = df[column].map(lambda x: sentiment(x, "pos")).astype(float)
    df['Negative'] = df[column].map(lambda x: sentiment(x, "neg")).astype(float)
    return df

def sentiment_comment(comment):
    if comment["Positive"] >= comment["Negative"]:
        return 1
    else:
        return 0

def calculate_global_sentiment(df):
    dataset = df.copy()
    dataset['global_scores_dict'] = dataset['comments_join'].apply(lambda review: analyser.polarity_scores(review))
    dataset['global_scores'] = dataset['global_scores_dict'].apply(lambda comp: comp['compound'])
    dataset['comp_score_global'] = dataset['global_scores'].apply(lambda c: 1 if c >= 0 else 0)
    return dataset['comp_score_global']

def test_vader_model(df_test: pd.DataFrame):
    df_test = get_sentiment(df_test, "comments_processed")
    df_test['comp_score'] = df_test.apply(sentiment_comment, axis=1)

    evaluate_model(df_test['sentiment_score'], df_test['comp_score'], 'vader')

    df_test['comp_score_global'] = calculate_global_sentiment(df_test)
    evaluate_model(df_test['sentiment_score'], df_test['comp_score_global'], 'vader_global')



def select_model(model_type: str):
    if model_type == 'logistic':
        model = Pipeline([('tfidf', TfidfVectorizer()),
                          ('clf', LogisticRegression(penalty='l2', max_iter=500, random_state=42)), ])
       # model = LogisticRegression(penalty='l2', max_iter=500, random_state=42)
    elif model_type == 'linearsvc':
        model = Pipeline([('tfidf', TfidfVectorizer()),
                          ('clf', LinearSVC()), ])
    elif model_type == 'multinomialNB':
        model = Pipeline([('tfidf', TfidfVectorizer()),
                          ('nb', MultinomialNB()), ])
    return model


def train_test_model(model_type:str, df_train: pd.DataFrame, df_test: pd.DataFrame):
    model = select_model(model_type)

    model.fit(df_train['comments_join'], df_train['sentiment_score'])

    predictions = model.predict(df_test['comments_join'])

    dump_pickle(f"{directory_path}models/{model_type}/{model_type}", model)

    evaluate_model(df_test['sentiment_score'], predictions, model_type)


def evaluate_model(y_true: pd.DataFrame, y_pred: pd.DataFrame, model_type: str):
    f1 = f1_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Validation F1 Score  : {f1} and Accuracy Score {accuracy}")

    scores = {
        "f1_score": f1,
        "accuracy": accuracy
    }
    dump_json_object(f"{directory_path}models/{model_type}/scores.json", scores)

    print("Classification Report: \n",
          classification_report(y_true, y_pred))


def evaluate_models():
    df = pd.read_csv(f'{directory_path}data/processed/IMDB Dataset.csv')
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    print("Vader sentiment analysis")
    test_vader_model(df_test)
    print("Logistic")
    train_test_model("logistic", df_train, df_test)
    print("LinearSVC")
    train_test_model("linearsvc", df_train, df_test)
    print("multinomialNB")
    train_test_model("multinomialNB", df_train, df_test)

