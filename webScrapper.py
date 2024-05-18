import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_links(html_content, base_domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        # Parse the link's domain using urlparse
        link_domain = urlparse(link['href']).netloc
        # Check if the link is within the same domain or is a relative link (no netloc)
        if link_domain == base_domain or not link_domain:
            links.add(link['href'])
    return links


def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No Title Found'
    return title

def scrape_data(start_url):
    visited_urls = set()
    data_to_save = [] 
    urls_to_visit = {start_url}
    base_domain = urlparse(start_url).netloc
    successful_fetches = 0  
    
    while urls_to_visit and successful_fetches < 10:
        current_url = urls_to_visit.pop()
        print(f"Scraping {current_url}")
        content = get_page_content(current_url)
        if content:
            successful_fetches += 1
            # Extract data from the content and add it to data_to_save
            page_title = extract_data(content)
            data_to_save.append([current_url, page_title])  # Save URL and its title
            visited_urls.add(current_url)
            for link in extract_links(content, base_domain):
                if link.startswith('/'):
                    link = f"https://{base_domain}{link}"
                if link not in visited_urls:
                    urls_to_visit.add(link)
        else:
            print(f"Failed to fetch {current_url}, not counting towards limit.")
    
    return data_to_save
def save_to_csv(data, filename='data.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Replace 'your_start_url_here' with the URL you want to start scraping from
data = scrape_data('https://docs.flutter.dev')
save_to_csv(data)