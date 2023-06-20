


def get_reddit(item):
    type_list = ['link', 'comment', 'sr']
    print(f"\nSearching for {item}...\n")

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
            if medicine in href:
                if "https://" in href and not "login" in href:
                    articles.append(href)

    # print(f"---------- About {medicine} ----------\n")
    for article in articles:
        print(f'Discussion found! About {medicine} on {article}')
        time.sleep(0.01)

    print(f"\nFound {len(articles)} discussions about {medicine}\n")
        
print('\n\n*** The program finished. Thank you :) ***\n')