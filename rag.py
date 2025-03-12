import sqlite3
import json

from ollama import chat
from typing import List, Dict

def json_parser(json_obj: str) -> bool:
    pass

def select_relevant_category(category: str, question: str, model: str = "deepseek-r1:1.5b") -> bool:
    return True
    prompt = ()
    message = [
        {
            'role': 'user',
            'content': prompt
        }
    ]
    res = chat(model,messages=message)
    return json_parser(res.message.content)

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

    relevant_categories = [cat for cat in categories if select_relevant_category(cat,question)]

    #SELECT headline,short_description,date FROM News WHERE category in ('cat1','cat2',...) LIMIT 20;
    query = "SELECT headline,short_description,date FROM News WHERE category in ( " + ",".join(["?"]*len(relevant_categories)) + " ) LIMIT 20"
    cursor.execute(query,relevant_categories)
    rows = cursor.fetchall()

    articles = [{"headline":headline, "short_description":short_description, "date":date} for headline,short_description,date in rows]
    conn.close()
    return articles


def select_relevant_article(article: Dict, question: str, model: str = "deepseek-r1:1.5b") -> bool:
    #Decides if given article is relevant
    return True
    prompt = ()
    message = [
        {
            'role': 'user',
            'content': prompt
        }
    ]
    res = chat(model,messages=message)
    return json_parser(res.message.content)

def final_answer(question: str, articles: List[Dict],model: str = "deepseek-r1:1.5b") -> str:
    #Returns final answer to question by using the selected articles
    prompt = ()
    message = [
        {
            'role': 'user',
            'content': prompt
        }
    ]
    res = chat(model,messages=message)
    return res.message.content

def rag(question: str) -> str:
    print("Start searching for interesting articles.")
    articles = get_articles(question)

    print(f"{len(articles)} are retrieved.")

    relevant_articles = []
    for idx, article in enumerate(articles,start=1):
        print(f"Reading article {idx}.")
        if select_relevant_article(article,question):
            relevant_articles.append(article)
            print(f"Article {idx} is relevant.")
        else:
            print(f"Article {idx} is not relevant.")

    answer = final_answer(question,relevant_articles)
    return answer

if __name__ == "__main__":
    question = ""
    res = rag(question)
    print(res)
