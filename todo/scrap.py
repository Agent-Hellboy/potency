
import requests
from bs4 import BeautifulSoup
import time
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 
 
def fetch_results(search_term, number_results, language_code): 
    escaped_search_term = search_term.replace(' ', '+')
 
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()
 
    return search_term, response.text
 

    
	
def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
 
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
 
        link = result.find('a', href=True)
        title = result.find('h3')
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword,'link': link,'rank': rank, 'title': title, 'description': description})
                rank += 1
    return found_results
    
    
def scrape_google(search_term, number_results, language_code):
    keyword, html = fetch_results(search_term, number_results, language_code)
    results = parse_results(html, keyword)
    return results
        
 
# keywords = ['python']
# data = []
# for keyword in keywords:
# 	try:
# 		results = scrape_google(keyword, 10, "en")
# 		for result in results:
# 		    data.append(result)
# 	finally:
# 		time.sleep(10)

    
