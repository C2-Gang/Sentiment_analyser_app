import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
nltk.download("stopwords")
import pandas as pd
from src.utils import directory_path,dump_pickle
import re
import numpy as np
from src.models.vocabulary import DIC_VOCABULARY
import contractions

def clean_labels(df):
    print(df.sentiment.value_counts())
    cleanup_nums = {"negative": -1, "neutral":0, "positive": 1}
    df['sentiment_score'] = df['sentiment'].replace(cleanup_nums)
    return df

def clean_text(text):
    text = str(text).lower()
    text = contractions.fix(text)
    # http links
    text = re.sub(r"http\S+", "", text)

    # html
    html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    text = re.sub(html, "", text)

    #twitter @
    text = re.sub(r"@[A-Za-z0-9]+", ' ', text)

    # others
    text = re.sub(r'\s+', ' ', text)
    return text


def build_own_contractions():
    for k,v in DIC_VOCABULARY.items():
        contractions.add(k, v)
    #dump_pickle(f"{directory_path}models/contractions", contractions)


def clean_stopwords(words):
    STOPWORDS = stopwords.words('english')
    sentences = [[e for e in word if not e in STOPWORDS] for word in words]
    return sentences


def preprocessing(text):
    build_own_contractions()

    # first cleaning
    text_clean = clean_text(text)
    text_clear = contractions.fix(text_clean)

    sents = nltk.sent_tokenize(text_clear)
    words = [word_tokenize(s) for s in sents]

    # deeper cleaning
    sentences = clean_stopwords(words)

    # alpha
    sentences = [[e for e in word if e.isalpha()] for word in sentences]

    return sentences


def join_words_processing(text):
    data = [' '.join(ele) for ele in text]
    if len(data) <1:
        return np.nan
    else:
        return ' '.join(data)

def do_preprocessing(dataset: pd.DataFrame, file_name: str):
    dataset['comments_processed'] = dataset.text.apply(preprocessing)
    dataset['comments_join'] = dataset.comments_processed.apply(join_words_processing).astype(str)
    dataset.to_csv(f'{directory_path}data/processed/{file_name}.csv', index=False)

def preprocess_data():
    twitter_dataset = pd.read_csv(f"{directory_path}data/raw/Twitter_Data.csv")
    reddit_dataset = pd.read_csv(f"{directory_path}data/raw/Reddit_Data.csv")

    dataset = pd.concat([twitter_dataset, reddit_dataset])
    dataset = dataset.rename(columns={'category': 'sentiment', 'clean_text': 'text'})

    do_preprocessing(dataset, "train")
    print("done")