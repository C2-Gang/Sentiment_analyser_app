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
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import resample

analyser = SentimentIntensityAnalyzer()

def do_sampling(df: pd.DataFrame, label: str, minority:int, majority:int, neutral):
    """This function allows you to balance unbalanced dataset.
    By specifying the downsample coefficient value,
    one can downsample its dataset.
    :param df: dataset to downsample
    :type df: pd.DataFrame
    :param label: target
    :type label: str
    :param downsample_coef: dowsampling coefficient to apply
    :type downsample_coef: float
    :return: a new df.DataFrame which has been downsample
    :rtype: df.DataFrame
    """

    df_majority = df[df[label] == majority]
    df_minority = df[df[label] == minority]
    df_neutral = df[df[label] == neutral]
    df_majority_downsampled = resample(
        df_majority, replace=True,
        n_samples=35500, random_state=1
    )
    df_up_down_sampled = pd.concat([df_majority_downsampled, df_minority, df_neutral])
    return df_up_down_sampled



def get_global_sentiment(sentiment):
    if sentiment >= 0.05:
        return 1
    elif sentiment <= - 0.05:
        return -1
    else:
        return 0

def calculate_global_sentiment(df: pd.DataFrame):
    """This function calculates vader sentiments:
    - doing the vader sentiment of each sentences and take the mean
    - doing the vader sentiment on all review

    :param df: comment value
    :type df: pd.DataFrame
    :return: dataset column
    :rtype:
    """
    dataset = df.copy()
    dataset['global_scores_dict'] = dataset['comments_join'].apply(lambda review: analyser.polarity_scores(review))
    dataset['global_scores'] = dataset['global_scores_dict'].apply(lambda comp: comp['compound'])
    dataset['comp_score_global'] = dataset['global_scores'].apply(get_global_sentiment)
    return dataset['comp_score_global']

def test_vader_model(df_test: pd.DataFrame):
    """This function evaluate vader model on test set:
    - do vader sentiments on / global
    - calculate scores (f1 - accuracy)

    :param df_test: comment value
    :type df_test: pd.DataFrame
    """
    df_test['comp_score_global'] = calculate_global_sentiment(df_test)
    evaluate_model(df_test['sentiment'], df_test['comp_score_global'], 'vader_global')



def select_model(model_type: str):
    """This function allows you to select the model.

    :param model_type: model type
    :type model_type: str
    :return: model selected
    :rtype:
    """
    if model_type == 'linearsvc':
        model =  LinearSVC()
    elif model_type == 'multinomialNB':
        model = MultinomialNB()
    elif model_type == "svm":
        model = SVC(probability=True)
    elif model_type == 'decisiontree':
        model = DecisionTreeClassifier()
    else:
        model = LogisticRegression(penalty='l2', max_iter=500, random_state=42)

    pipeline_model = Pipeline(
        [('tfidf', TfidfVectorizer()),
         ('model', model )])
    return pipeline_model


def train_test_model(model_type:str, df_train: pd.DataFrame, df_test: pd.DataFrame):
    """This function allows you to select the model, train,
    test, evaluate and store it.

    :param model_type: model type
    :type model_type: str
    :param df_train: train dataset
    :type df_train: pd.DataFrame
    :param df_test: test dataset
    :type df_test: pd.DataFrame
    """
    model = select_model(model_type)

    model.fit(df_train['comments_join'], df_train['sentiment'])

    predictions = model.predict(df_test['comments_join'])

    dump_pickle(f"{directory_path}models/{model_type}/{model_type}", model)

    evaluate_model(df_test['sentiment'], predictions, model_type)




def evaluate_model(y_true: pd.DataFrame, y_pred: pd.DataFrame, model_type: str):
    """This function allows you to evaluate the model.
    - Store scores (F1 and accuracy) in json

    :param y_true: true label
    :type y_true: pd.DataFrame
    :param y_pred: prediction
    :type y_pred: pd.DataFrame
    :param model_type: model type
    :type model_type: str
    """
    f1 = f1_score(y_true, y_pred, average="macro")
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
    """This function allows you to evaluate several models.
    """
    dataset = pd.read_csv(f'{directory_path}data/processed/train.csv').dropna(axis=0, subset=['comments_join', 'sentiment'])
    print(dataset.sentiment.value_counts())
    dataset = do_sampling(dataset, 'sentiment', -1, 1, 0)
    dataset = do_sampling(dataset, 'sentiment', -1, 0, 1)
    print(dataset.sentiment.value_counts())
    df_train, df_test = train_test_split(dataset,test_size = 0.2)

    print("Vader sentiment analysis")
    test_vader_model(df_test)
    print("Logistic")
    train_test_model("logistic", df_train, df_test)
    print("LinearSVC")
    train_test_model("linearsvc", df_train, df_test)
    print("multinomialNB")
    train_test_model("multinomialNB", df_train, df_test)
    #print("svm")
    #train_test_model("svm", df_train, df_test)
    #print("decisiontree")
    #train_test_model("decisiontree", df_train, df_test)


"""
https://www.kaggle.com/faressayah/natural-language-processing-nlp-for-beginners

The multinomial Naive Bayes classifier is suitable for classification with discrete features 
(e.g., word counts for text classification). 
The multinomial distribution normally requires integer feature counts. 
However, in practice, fractional counts such as tf-idf may also work.
"""

""" 
Logistic regression, despite its name, is a linear model for classification rather than regression. 
Logistic regression is also known in the literature as logit regression, maximum-entropy classification (MaxEnt) 
or the log-linear classifier. 
In this model, the probabilities describing the possible outcomes 
of a single trial are modeled using a logistic function.
"""