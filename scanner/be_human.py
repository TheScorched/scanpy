import requests
import time
import random

# url here
url = 'http://example.com'

# user-agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    # if desired add more User-Agent strings here
]
  
# simulate human-like browsing
def simulate_human_browsing(session, url):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': url  
    }
    try:
        response = session.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        time.sleep(random.uniform(5, 15))
    except requests.RequestException as e:
        print(f"Error: {e}")

# re-use of TCP connection
with requests.Session() as session:
    for _ in range(5):  # total requests
        simulate_human_browsing(session, url)
