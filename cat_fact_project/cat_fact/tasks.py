# cat_facts/tasks.py
import requests
import dramatiq

@dramatiq.actor
def fetch_cat_fact():
    response = requests.get('https://cat-fact.herokuapp.com/facts')
    facts = response.json()
    return facts
