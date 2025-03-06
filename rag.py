import sqlite3
import json

from ollama import chat
from typing import List, Dict

def json_parser(json_obj: str) -> bool:
    pass

def get_articles(db: str) -> List[Dict]:
    #Gets all articles from the Database
    pass

def select_relevant_articles(article: Dict, idx: int, question: str, model: str = "deepseek-r1:1.5b") -> bool:
    #Decides if given article is relevant
    prompt = """

        """
    pass

def final_answer(question: str, articles: List[Dict]):
    #Returns final answer to question by using the selected articles
    pass

def rag(question: str) -> str:
    articles = get_articles("DB")
    
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
