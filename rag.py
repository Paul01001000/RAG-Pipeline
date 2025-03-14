import sqlite3
import json
import re

from ollama import chat
from typing import List, Dict

def json_parser(response: str) -> bool:
    def isolate_json(response: str):
        try:
            # Use a regular expression to find potential JSON objects
            response = response.replace('\n','')
            json_matches = re.findall(r"\{.*\}|\[.*\]", response) #Finds curly or square brackets
            print(json_matches)
            for match in json_matches:
                print(match)
                try:
                    # Attempt to parse each match as JSON
                    return json.loads(match)  # return the first valid json found.

                except json.JSONDecodeError:
                    # If parsing fails, continue to the next match
                    continue
            return None  # No valid JSON found.

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def json_contains_true(json_object) -> bool:
        if isinstance(json_object, dict):
            for value in json_object.values():
                if value is True:
                    return True
                if isinstance(value, (dict, list)):
                    if json_contains_true(value):
                        return True
                    
        elif isinstance(json_object, list):
            for item in json_object:
                if item is True:
                    return True
                if isinstance(item, (dict, list)):
                    if json_contains_true(item):
                        return True
                    
        return False
    
    json_object = isolate_json(response)
    print(json_object)
    return json_contains_true(json_object)

        

def select_relevant_category(category: str, question: str, model: str = "deepseek-r1:1.5b") -> bool:
    #return True
    prompt = ()
    message = [
        {
            'role': 'user',
            'content': prompt
        }
    ]
    res = chat(model,messages=message)
    try:
        content = res.message.content.split("</think>")[1]
        return json_parser(content)
    except Exception as e:
        print(f"An error occurred: {e}. Response cannot be processed")
        return False

def get_articles(question: str = "", db_path: str = "news.db") -> List[Dict]:
    #Gets all articles from the Database
    """
    news.db Data Source:
    1. Misra, Rishabh. "News Category Dataset." arXiv preprint arXiv:2209.11429 (2022).
    2. Misra, Rishabh and Jigyasa Grover. "Sculpting Data for ML: The first act of Machine Learning." ISBN 9798585463570 (2021).
    https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT DISTINCT category FROM News"
    cursor.execute(query)
    categories = cursor.fetchall()

    relevant_categories = [cat for cat, in categories if select_relevant_category(cat,question)]

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
    return json_parser(res.message.content.split("</think>")[1])

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
    print(answer)
    return answer

if __name__ == "__main__":
    question = ""
    res = rag(question)