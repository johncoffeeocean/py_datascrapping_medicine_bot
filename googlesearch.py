import requests
from bs4 import BeautifulSoup

search_query = 'aspirin'
site_query = 'site:mayoclinic.org'

# url = f"https://www.google.com/search?q={search_query}+{site_query}&num=100"
url = f"https://www.google.com/search?q=medical+dictionary&rlz=1C1YTUH_enUS1052US1052&oq=medical+dic&aqs=chrome.1.69i57j0i67i650j0i512j0i67i650j0i512l2j0i67i650j69i60.3359j0j7&sourceid=chrome&ie=UTF-8"
print(url)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a')
for link in links:
    href = link.get('href')
    print(href)
