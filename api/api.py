from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json
from difflib import SequenceMatcher
import re  # for stripping HTML tags

# Load your scraped data
with open("posts_data.json", "r", encoding="utf-8") as f:
    posts_data = json.load(f)

app = FastAPI()

class Query(BaseModel):
    question: str
    image: Optional[str] = None

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def strip_html(html_text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_text)

def find_relevant_posts(question, threshold=0.2):
    ranked_posts = []
    for post in posts_data:
        content = post.get("cooked", "")
        score = similarity(content, question)
        if score > threshold:
            ranked_posts.append((score, post))
    return sorted(ranked_posts, reverse=True)[:3]

@app.post("/api/")
async def get_answer(query: Query):
    question = query.question
    results = find_relevant_posts(question)

    if not results:
        return {"answer": "Sorry, I couldn't find any relevant answer.", "links": []}

    top = results[0][1]
    answer = strip_html(top["cooked"])
    links = [
        {
            "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{post['topic_id']}/{post['post_number']}",
            "text": strip_html(post["cooked"][:100]).replace("\n", " ")
        }
        for _, post in results
    ]

    return {"answer": answer, "links": links}
