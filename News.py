import requests
from bs4 import BeautifulSoup


def get_bbc_headlines():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = soup.find_all('h2')

        if headlines:
            news_list = [headline.text.strip() for headline in headlines[:5]]
            return news_list
        else:
            print("No headlines found with the specified class.")
            return []
    else:
        return f"Failed to retrieve news. Status code: {response.status_code}"