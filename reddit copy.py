import requests
from bs4 import BeautifulSoup
import time

medicine_names = ['paracetamol', 'aspirin', 'ibuprofen']
# search_terms = {'paracetamol': ['pain relief', 'fever'], 
#                 'aspirin': ['blood thinner', 'heart attack'], 
#                 'ibuprofen': ['anti-inflammatory', 'arthritis']}
search_limit = 50
type_list = ['link', 'comment', 'sr']
print("Please wait. \n")

for medicine in medicine_names:

    print(f"\nSearching for {medicine}...\n")
    articles = []
    # search_term = ' OR '.join(search_terms[medicine])
    
    while len(articles) < search_limit:
        # url = f"https://www.reddit.com/search/?q={medicine}+{search_term}&type=comment"
        for type in type_list:
            url = f"https://www.reddit.com/search/?q={medicine}&type={type}"
            response = requests.get(url)
            html = response.content

            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and '/r/' and '/comments' in href:
                    if 'https://www.reddit.com/' in href:
                        articles.append(href)
                    else:
                        articles.append("https://www.reddit.com" + href)

            for link in links:
                href = link.get('href')
                if medicine in href:
                    if "https://" in href and not "login" in href:
                        articles.append(href)

    # print(f"---------- About {medicine} ----------\n")
    for article in articles:
        print(f'Discussion found! About {medicine} on {article}')
        time.sleep(0.01)

    print(f"\nFound {len(articles)} discussions about {medicine}\n")
        
print('\n\n*** The program finished. Thank you :) ***\n')