import requests
import json
import time
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

# Update the cookies here with latest _t and _forum_session values
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://discourse.onlinedegree.iitm.ac.in/",
    "Connection": "keep-alive",
    "Cookie": "_t=QHGJuFAWA9WhNMLUGBzWrHm4eFU%2Bqw7rPP0hwNhH0sJjICWRfW2zD9PUPASF1miQ7hLd9pQ%2BSQF06DurwFh0nc5xbBPVn99EoksQHYs8FOINOWldgPgvhyI6xJO0FI2ppk38HGBsnH%2BRa8XtkNyFx3R%2F7wk4C4M%2B5Mo%2BsLk7Bdg%2B2%2BV%2BusiKUVs0VE5j9%2BwX5z90ng0G57c8HnL1fOF1arnZu%2BGjfy8LpSJrSWmU8shqBOszi2xUhG0Oi1MTsgaexrvnjPKYRqyKxoP5P820mZGYfWRBdVX%2FyctAbcDyYGkNod%2BnMq%2BVkqkgTJOA5Zy9--xR9Jgfe44Di7ilaq--RKY7yqdzQ3yXwHI7WYYb4Q%3D%3D; _forum_session=e96iognu0QfobdUZzHGUfc%2BMiFZ2ZxxEhSjDberxLcsp7fiWnFBL2s6ejFa2NSzhQt0IL8zBP15uGrqs7FqyMqxBPuNrF0%2B94Z4NE4c%2BTY%2FMNIKAgGmTMQ0cWpvNebFGgPSjIsWwaMm18ZXbv1SFSFr64KLMLQlcjItWM4DRDbtovxoKaKibqfmzAi1xAjosM7b0dlkDLZpn%2F91ak982VzKZWZuttf8Hn2jY2FGwJNp3o1o6IxFIMOXurxV%2B08fQqu830J8%2Fxxq6q8h9SGj%2F9cpTxjAs4jiJER3lpiRYUqjR7I8FLZeItp0qQ9oLM1olH0M6SB5kcaJLOn5Qi1%2BWZOSWyQRLMIFPDmxWEXch1MyESWcvxxAR8m074PBYPw%3D%3D--MiQlIsxnW%2By3lccO--nf%2BSqA4Zvktleb3wGlKy1g%3D%3D"
}

START_DATE = datetime.strptime("2025-01-01", "%Y-%m-%d")
END_DATE = datetime.strptime("2025-04-14", "%Y-%m-%d")

def fetch_topics():
    topics = []
    for page in range(0, 5):  # Reduced to 5 pages to avoid SSL issues
        try:
            res = requests.get(f"{BASE_URL}/latest.json?page={page}", headers=HEADERS)
            res.raise_for_status()
            data = res.json()
            for topic in data['topic_list']['topics']:
                created_at = datetime.strptime(topic['created_at'][:10], "%Y-%m-%d")
                if START_DATE <= created_at <= END_DATE:
                    topics.append(topic['id'])
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error fetching page {page}: {e}")
            break
    return topics

def fetch_posts_from_topics(topic_ids):
    posts = []
    for topic_id in topic_ids:
        try:
            res = requests.get(f"{BASE_URL}/t/{topic_id}.json", headers=HEADERS)
            res.raise_for_status()
            data = res.json()
            for post in data['post_stream']['posts']:
                posts.append({
                    "topic_id": topic_id,
                    "username": post.get("username"),
                    "cooked": post.get("cooked"),
                    "created_at": post.get("created_at"),
                    "post_number": post.get("post_number")
                })
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error fetching topic {topic_id}: {e}")
    return posts

if __name__ == "__main__":
    print("🔄 Fetching topics...")
    topic_ids = fetch_topics()
    print(f"📅 Filtered to {len(topic_ids)} topics between 2025-01-01 and 2025-04-14")

    print("\n📝 Fetching posts from topics...")
    posts = fetch_posts_from_topics(topic_ids)

    with open("posts_data.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("\n✅ Saved all posts to 'posts_data.json'")
