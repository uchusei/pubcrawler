import requests
from bs4 import BeautifulSoup
import json

def scrape_publishers():
    base_url = "https://isbn.kb.se/sok/"
    query = "förlag"
    page = 1
    web_app_url = 'https://script.google.com/macros/s/AKfycbxCZGHPvOhV4xshtmU2Z0f7WNSXkCS-lYEmWIoGp8WDkMD-pmbvVJMz6KdSNf36uw1_uQ/exec'

    while True:
        url = f"{base_url}?query={query}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        publishers = soup.find_all('div', class_='panel panel-default')
        for publisher in publishers:
            name_tag = publisher.find('h3')
            if "(Ej aktiv)" in name_tag.text:
                continue

            name = name_tag.text.strip()
            email = None
            web = None
            for p_tag in publisher.find_all('p'):
                if 'E-post:' in p_tag.text:
                    email = p_tag.text.replace('E-post:', '').strip()
                if p_tag.find('a', href=True):
                    web = p_tag.find('a', href=True)['href']

            if email and any(domain in email for domain in ['gmail.com', 'hotmail.com', 'outlook.com', 'live.com', 'yahoo.com', 'yahoo.se', 'telia.com', 'glocalnet.net', 'swipnet.se', 'live.se', 'bredband.net', 'brevet.nu', 'tele2.se', 'comhem.se', 'algonet.se', 'zeta.telenordia.se', 'hotmail.se', 'live.se', 'home.se', 'comhem.com', 'icloud.com', 'icloud.se']):
                continue

            data = {
              'type': 'KB',
              'name': name,
              'email': email,
              'web': web
            }

            requests.post(web_app_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

        next_page_link = soup.find('a', href=lambda href: href and f"page={page+1}" in href)
        if not next_page_link:
            break
        page += 1

if __name__ == "__main__":
    scrape_publishers()
