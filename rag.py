import sqlite3
import json

from ollama import chat
from typing import List, Dict

def json_parser(json_obj: str) -> bool:
    pass

def select_relevant_categories(categories: List[str], question: str, model: str = "deepseek-r1:1.5b") -> List[str]:
    promt = ()
    return tuple(categories)

def get_articles(question: str = "", db_path: str = "news.db") -> List[Dict]:
    #Gets all articles from the Database
    """
    DB Data Source:
    1. Misra, Rishabh. "News Category Dataset." arXiv preprint arXiv:2209.11429 (2022).
    2. Misra, Rishabh and Jigyasa Grover. "Sculpting Data for ML: The first act of Machine Learning." ISBN 9798585463570 (2021).
    https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT DISTINCT category FROM News"
    cursor.execute(query)
    rows = cursor.fetchall()

    categories = [category for category, in rows]

    relevant_categories = select_relevant_categories(categories,question)


    query = f"SELECT headline,short_description,date FROM News WHERE category in {tuple(relevant_categories)} LIMIT 20"
    cursor.execute(query)
    rows = cursor.fetchall()

    articles = [{"headline":headline, "short_description":short_description, "date":date} for headline,short_description,date in rows]
    conn.close()
    return articles


def select_relevant_articles(article: Dict, idx: int, question: str, model: str = "deepseek-r1:1.5b") -> bool:
    #Decides if given article is relevant
    prompt = ()
    pass

def final_answer(question: str, articles: List[Dict]):
    #Returns final answer to question by using the selected articles
    pass

def rag(question: str) -> str:
    articles = get_articles()
    
    prompt = (
        "Hello"
        "World"
    )

    return prompt
    relevant_articles = []
    for idx, article in enumerate(articles,start=1):
        if select_relevant_articles(article,question):
            relevant_articles.append(article)

if __name__ == "__main__":
    question = ""
    res = rag(question)
    print(res)
