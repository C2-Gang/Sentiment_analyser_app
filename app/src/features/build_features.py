import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
nltk.download("stopwords")
import pandas as pd
from src.utils import directory_path
import re
import numpy as np
import contractions
from src.models.vocabulary import DIC_VOCABULARY

def clean_labels(df):
    print(df.sentiment.value_counts())
    cleanup_nums = {"negative": -1, "neutral":0, "positive": 1}
    df['sentiment_score'] = df['sentiment'].replace(cleanup_nums)
    return df

def clean_text(text):
    text = str(text).lower()
    text = contractions.fix(text)
    text = re.sub(r"@[A-Za-z0-9]+", ' ', text)
    text = re.sub(r"[^a-zA-Z.!?]", ' ', text)
    text = re.sub(r" +", ' ', text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    text = re.sub(html, "", text)
    text = re.sub(r'[^\x00-\x7f]', r'', text)
    return text


def preprocessing(text):
    text_clear = clean_text(text)
    sents = nltk.sent_tokenize(text_clear)
    owned_stopwords = ['``', ' ', '']
    owned_stopwords.extend(stopwords.words("english"))
    words = [word_tokenize(s.lower()) for s in sents]
    STOPWORDS = stopwords.words('english') + [ 'ure',
        'u', 'ü', 'ur', '4', '2', "http", 'com']
    words = [[DIC_VOCABULARY[e]  if e in DIC_VOCABULARY else e for e in word]  for word in words]
    sentences = [[e for e in word if not e in STOPWORDS] for word in words]

    return sentences


def join_words_processing(text):
    text = [[e for e in word if e.isalpha()] for word in text]
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