import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
nltk.download("stopwords")
import pandas as pd
from src.utils import directory_path
from bs4 import BeautifulSoup


def clean_labels(df):
    print(df.sentiment.value_counts())
    cleanup_nums = {"positive": 1, "negative": 0}
    df['sentiment_score'] = df['sentiment'].replace(cleanup_nums)
    return df

def clean_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def preprocessing(text):
    text_clear = clean_html(text)
    sents = nltk.sent_tokenize(text_clear)
    owned_stopwords = ['``', ' ', '']
    owned_stopwords.extend(stopwords.words("english"))
    words = [word_tokenize(s.lower()) for s in sents]
    sentences = [[e for e in word if not e in owned_stopwords] for word in words]
    return sentences


def join_words_processing(text):
    text = [[e for e in word if e.isalpha()] for word in text]
    data = [' '.join(ele) for ele in text]
    return ' '.join(data)

def do_preprocessing():
    dataset = pd.read_csv(f"{directory_path}data/raw/IMDB Dataset.csv")
    dataset = clean_labels(dataset)
    dataset['comments_processed'] = dataset.review.apply(preprocessing)
    dataset['comments_join'] = dataset.comments_processed.apply(join_words_processing)
    dataset.to_csv(f'{directory_path}data/processed/IMDB Dataset.csv', index=False)
