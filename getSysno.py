import requests
from bs4 import BeautifulSoup

def get_synonyms(word):
    url = f"https://www.thesaurus.com/browse/{word}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    synonyms = []
    for a in soup.find_all("a", class_="css-1gyuw4i eh475bn0"):
        # for span in div.find_all("span", class_="css-133coio etbu2a32"):
        synonyms.append(a.text.strip())
    return synonyms

input_word = "Ibuprofen"
synonyms = get_synonyms(input_word)

print(f"Synonyms of {input_word}:")
for synonym in synonyms:
    print(synonym)