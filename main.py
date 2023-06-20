import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

articles_all = []
driver = webdriver.Chrome() 
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(options=options)

def similar_words_nlp(input_word):
    synsets = wordnet.synsets(input_word)
    # Initialize a set to store similar words
    similar_words = set()
    # Loop through each synset and add its synonyms and hyponyms to the set
    for synset in synsets:
        for lemma in synset.lemmas():
            # Add synonym to similar words set
            similar_words.add(lemma.name().lower())
            
            # Add hyponyms to similar words set
            for hyponym in lemma.synset().hyponyms():
                similar_words.add(hyponym.lemma_names()[0].lower())
    result = []
    count = 0
    for s in similar_words:
        if s != input_word:
        # if input_word not in s:
            print(s)
            result.append(s)
            count = count + 1
        if count > 5:
            break
        
    return result

def show_result(item, articles):
    for article in articles:
        print(f'Discussion found! About {item} on {article}')
        articles_all.append(article)
        time.sleep(0.03)

def get_reddit(item):
    articles = []
    type_list = ['link', 'comment', 'sr']
    # print(f"\n -- reddit.com --")
    
    for type in type_list:
        url = f"https://www.reddit.com/search/?q={item}&type={type}"
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
            if item in href:
                if "https://" in href and not "login" in href:
                    articles.append(href)

    show_result(item, articles)
    
def get_webmd(item):
    articles = []
    # print(f"\n -- https://www.webmd.com/ --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.webmd.com/search/search_results/default.aspx?query={item}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links_div = soup.find_all('div', {'class': 'search-text-container'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for div in links_div:
        link = div.find('a')
        href = link.get('href')
        classname = str(link.get('class'))
        # if (href and 'connect.mayoclinic.org/discussion' in href) and (classname and 'ch-search-result-title' in classname):
        articles.append(href)
    
    show_result(item, articles)

def get_healthunlock(item):
    articles = []
    # print(f"\n -- https://healthunlocked.com --")
    
    try:
        url = f"https://healthunlocked.com/search/posts?query={item}&page=1&community=all"
        driver.get(url)
        time.sleep(2)
        try: 
            work = driver.find_element(By.XPATH, "//button[@id='ccc-notify-accept']")
            work.click()
            time.sleep(2)
        except:
            pass

        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links_div = soup.find_all('div', {'class': 'results-post'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for div in links_div:
        link = div.find('a')
        if (link):
            href = link.get('href')
            if (href):
                articles.append("https://healthunlocked.com" + href)
        
    show_result(item, articles)

def get_drugs(item):
    articles = []
    # print(f"\n -- https://www.drugs.com --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.drugs.com/search.php?searchterm={item}&phrase=all&language=english&results_per_page=50&sources%5B%5D=consumer&sources%5B%5D=professional&sources%5B%5D=drugimages&sources%5B%5D=interactions&sources%5B%5D=news&sources%5B%5D=fdaalerts&sources%5B%5D=newdrugapprovals&sources%5B%5D=newdrugapplications&sources%5B%5D=clinicaltrials&sources%5B%5D=cg&sources%5B%5D=natural"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'class': 'ddc-search-result-link-wrap'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        # link = div.find('a')
        href = link.get('href')
        classname = str(link.get('class'))
        # if (href and 'connect.mayoclinic.org/discussion' in href) and (classname and 'ch-search-result-title' in classname):
        articles.append(href)
    
    show_result(item, articles)

def get_everydayhealth(item):
    articles = []
    # print(f"\n -- everydayhealth.com --")
    
    # url = f"https://www.drugs.com/search.php?searchterm={item}"
    url = f"https://www.everydayhealth.com/search/?q={item}&updateesi=true"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    
    for link in links:
        href = link.get('href')
        classname = str(link.get('class'))
        if (href and 'www.everydayhealth.com' in href) and (classname and 'result-item__link' in classname):
            articles.append(href)
    
    show_result(item, articles)
    
def get_mayo(item):
    articles = []
    # print(f"\n -- connect.mayoclinic.org --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://connect.mayoclinic.org/search/discussions/?search={item}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        classname = str(link.get('class'))
        if (href and 'connect.mayoclinic.org/discussion' in href) and (classname and 'ch-search-result-title' in classname):
            articles.append(href)
    
    show_result(item, articles)

def get_medhelp(item):
    articles = []
    # print(f"\n -- www.medhelp.org --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.medhelp.org/search/expanded?cat=posts&query={item}"
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('div', {'class': 'result_name'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.find('a').get('href')
        articles.append('https://www.medhelp.org' + href)
    
    show_result(item, articles)

def get_babycenter(item):
    articles = []
    # print(f"\n -- community.babycenter.com --")
    
    try:
        url = f"https://community.babycenter.com/search?q={item}&currentTab=expert"
        driver.get(url)
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        links = soup.find_all('a', {'class': 'hoverTextOnly'})
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        classname = str(link.get('class'))
        # if (href and '/post' in href):
        articles.append(href)
    
    show_result(item, articles)

def get_patientinfo(item):
    articles = []
    # print(f"\n -- patient.info --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://patient.info/search.asp?searchTerm={item}&collections=All"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'class': 'articleSummary__titleLink'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        # if (href and '/post' in href):
        #   articles.append(href)
        articles.append('https://patient.info' + href)
        
    
    show_result(item, articles)

def get_sciencebasedmedicine(item):
    articles = []
    # print(f"\n -- https://sciencebasedmedicine.org/ --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://sciencebasedmedicine.org/?s={item}"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'rel': 'bookmark'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        if "is-robot" not in href:
            articles.append(href)
        
    show_result(item, articles)

def get_steadyhealth(item):
    articles = []
    # print(f"\n -- https://www.steadyhealth.com/ --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.steadyhealth.com/search?q={item}"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'itemprop': 'url'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        # if (href and '/post' in href):
        #   articles.append(href)
        articles.append( href)
        
    
    show_result(item, articles)

def get_healthtap(item):
    articles = []
    # print(f"\n -- www.healthtap.com --")
    
    try:
        url = f"https://www.healthtap.com/search?q={item}"
        driver.get(url)
        time.sleep(7)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        links = soup.find_all('a', {'rel': 'noopener noreferrer'})
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        classname = str(link.get('class'))
        if (href and 'https://www.healthtap.com/questions/' in href):
            articles.append(href)
    
    show_result(item, articles)
    
def get_national_libray(item):
    articles = []
    # print(f"\n -- https://vsearch.nlm.nih.gov/ --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?query={item}&v%3Aproject=nlm-main-website&_gl=1*1es199j*_ga*OTY5ODc0ODQuMTY4NjYxOTAxNw.._ga_P1FPTH9PL4MTY4NjYxOTAxNy4xLjEuMTY4NjYxOTIyMS4wLjAuMA.._ga_7147EPK006MTY4NjYxOTAxNy4xLjEuMTY4NjYxOTIzMS4wLjAuMA"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        time.sleep(3)
        # response = requests.get(url)
        
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'class': 'title'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append('https://vsearch.nlm.nih.gov' + href)
        # articles.append(link.text)
        
    
    show_result(item, articles)

def get_pubmed(item):
    articles = []
    # print(f"\n -- https://pubmed.ncbi.nlm.nih.gov --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={item}&sort=date&size=20"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'class': 'docsum-title'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append('https://pubmed.ncbi.nlm.nih.gov' + href)
        # articles.append(link.text)
        
    
    show_result(item, articles)

def get_who(item):
    articles = []
    # print(f"\n -- https://www.who.int --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.who.int/home/search?indexCatalogue=genericsearchindex1&searchQuery={item}&wordsMode=AnyWord"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links_div = soup.find_all('div', {'class': 'sf-list-vertical__item'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for div in links_div:
        href = div.find('a').get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append(href)
        # articles.append(div.find('a').text)
        
    
    show_result(item, articles)

def get_fda(item):
    articles = []
    # print(f"\n -- https://www.fda.gov --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.fda.gov/search?s={item}&items_per_page=50&sort_bef_combine=date_DESC#"
        # response = requests.get(url)
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        text = link.text
        if (href and href in text and "media/" not in href):
            articles.append(text)
        # articles.append(div.find('a').text)
        
    
    show_result(item, articles)
       
def get_drugs_forum(item):
    articles = []
    # print(f"\n -- https://drugs-forum.com --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://drugs-forum.com/search/3161086/?q={item}&o=relevance&c[p][vwcomment][displayorder]=0"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links_div = soup.find_all('div', {'class': 'listBlock main'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for div in links_div:
        href = div.find('a').get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append("https://drugs-forum.com/" + href)
        # articles.append(div.find('a').text)
        
    show_result(item, articles)

def get_ema_europe(item):

    articles = []
    # print(f"\n -- https://www.ema.europa.eu --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.ema.europa.eu/en/search/search?search_api_views_fulltext={item}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'class': 'ecl-link ecl-list-item__link'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for link in links:
        href = link.get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append("https://www.ema.europa.eu" + href)
        # articles.append(div.find('a').text)
        
    show_result(item, articles)

def get_net_mum(item):

    articles = []
    # print(f"\n -- https://www.netmums.com --")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = f"https://www.netmums.com/search?q={item}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
        
    html = response.content

    try:
        soup = BeautifulSoup(html, 'html.parser')
        links_div = soup.find_all('h3', {'class': 'card__title'})
        
    except Exception as e:
        print(f"Error: {e}")
        
    for div in links_div:
        link = div.find('a')
        href = link.get('href')
        # if (href and 'www.healthtap.com/questions/' in href):
        articles.append(href)
        # articles.append(div.find('a').text)
        
    show_result(item, articles)

def run(item):
    # # --- beautiful soap --- 
    get_reddit(item)   
    get_mayo(item)
    get_drugs_forum(item)
    get_medhelp(item)
    get_pubmed(item)
    get_net_mum(item)
    get_drugs(item) 
    get_everydayhealth(item)
    get_patientinfo(item)
    get_sciencebasedmedicine(item)
    get_steadyhealth(item)
    get_national_libray(item)
    get_who(item)
    get_fda(item)
    get_ema_europe(item)
    # # --- selenium ---        
    get_healthunlock(item) 
    get_babycenter(item)
    get_healthtap(item)

def run2(item):
    get_reddit(item)
    get_mayo(item)
    get_drugs_forum(item)
    get_medhelp(item)
    get_pubmed(item)
    get_net_mum(item)
            
def main():
    counter = 5
    while True:
        
        item = input("Enter a word: ")
        if item == "q" or item == "quit":
            exit()
            
        global articles_all
        articles_all = []    
        
        # print(f"\nSearching for {item}...\n")
        run(item)
        print("------------------------------------------------\n")
        if len(articles_all):
            print(str(len(articles_all)) + ' discussions found\n')
        else:
            print('No discussions found\n')
        
        # similar_words
        similar_words = similar_words_nlp(item)
        if similar_words:
            articles_all = []   
            print(f"\nSearching for more links related to {item}...")
            for similar_word in similar_words:
                # print(f"\n______{similar_word}______\n")
                run2(similar_word)
            if len(articles_all):
                print('\n' +str(len(articles_all)) + ' extra discussions found\n')
            else:
                print('\nNo extra discussions found\n')
        print("------------------------------------------------\n")
        print("If you want quit this program, press 'quit' or 'q'")
        print("------------------------------------------------\n")
        
        counter = counter - 1

main()