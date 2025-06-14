import requests
import json
import time

# STEP 1: Target URL
url = "https://discourse.onlinedegree.iitm.ac.in/latest.json"

# STEP 2: Replace with fresh cookies
cookies = {
    "_t": "rb%2FFLfk%2B%2Fd2ARFs8ZQdjq7ZvdMCfkf%2Fhm%2Fbkc1Es7p7ePvLW9x1tUlgVh%2F7THTzrERo9bQpgbbegKu4q05EItyF4i22j6%2BtkRqjHiRCf0xIAALr9PX9Ozn%2Far3zKDecagHTJfSgWL1XT013ex5n7AkWqmSKKasveFoiqzJ7QAOGTNFglyABYnVLpGfJYVKNrdGyGEm8lyCxEZMDBRrc8putriICEvBZIeGISmhk%2FmJHOZJEXHIWcE27brm0bF5QDVVJhqDXBXHdgRKiYbGf53m37Vh9gQms%2BsI4y3%2FecwhQBAIFpIINKyNcXq9zi4Ank--CoRl8ljqCJI42K%2FK--xrUwMBqTU6a9erOqz86V0A%3D%3D",
    "_forum_session": "%2FmHsx0hxl%2BI02Qh5kt5155Z2Ef9SjtN4jqECrQ5gjXJmA7ZkhyzQ8tw%2BJzDCdQiZiO%2FKE%2FPyzFrs4Tt8sbQxeKA%2Ba9TJTDZpNxWl0XryzysDtcaCi%2FRLnyjB1DF99zb75sACIOdakO4ShMa%2BCe8UnMMq4q%2F59hPlMbe%2F59YbH008zAoo4Cv4e15R2W9Dtzpgjhwhs7pAt3XKqAPv5ETRwZh6Gm0HUdS9oN%2F68HTZPez59E4yamb9ITEOTOEIINr9n6zFAwNFwH9IpBbvvgms3R8XhnycgSp2MV9dUMmWK4%2Fv3RuceHZFDfu%2F32hkRvs2zPM1%2BYDn49%2Bd9JxvvryUUgG7oPHhjnTpciCRo0qf4f7UueYMEM7u32oVFR2Wdw%3D%3D--jm%2BAMhKRmsMlZ0tC--BetcpyVHH0MheIjCxw7vDw%3D%3D"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# Helper function
def user_profile_url(username):
    return f"https://discourse.onlinedegree.iitm.ac.in/u/{username}.json"

# STEP 3: Fetch latest.json
response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    print("✅ Found users. Fetching profiles...\n")
    data = response.json()
    users = data.get("users", [])
    print(f"✅ Found {len(users)} users. Fetching profiles...\n")

    all_profiles = []

    for i, user in enumerate(users):
        username = user.get("username")
        if not username:
            continue

        print(f"🔍 [{i+1}/{len(users)}] Fetching profile for @{username}")

        try:
            profile_response = requests.get(user_profile_url(username), headers=headers, cookies=cookies, timeout=10)
            profile_response.raise_for_status()

            udata = profile_response.json().get("user", {})
            profile = {
                "username": username,
                "name": udata.get("name"),
                "created_at": udata.get("created_at"),
                "bio_raw": udata.get("bio_raw"),
                "trust_level": udata.get("trust_level"),
                "profile_views": udata.get("profile_view_count", 0),
                "likes_given": udata.get("likes_given", 0),
                "likes_received": udata.get("likes_received", 0),
                "badges": udata.get("badge_count", {}),
            }
            all_profiles.append(profile)

        except requests.exceptions.SSLError as ssl_err:
            print(f"❌ SSL Error for @{username}: {ssl_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"⚠️ Request failed for @{username}: {req_err}")
        except Exception as e:
            print(f"‼️ Unexpected error for @{username}: {e}")

        time.sleep(1.5)  # Respectful delay

    # Save final data
    with open("user_profiles.json", "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, indent=2)
    print("\n📁 Saved all user profiles to 'user_profiles.json'.")

else:
    print("❌ Failed to fetch data from /latest.json")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
