import requests
from bs4 import BeautifulSoup


def scrape_company(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""

    meta = soup.find("meta", attrs={"name": "description"})

    description = meta["content"] if meta else ""

    headings = [h.text.strip() for h in soup.find_all("h1")]

    return {
        "title": title,
        "description": description,
        "headings": headings,
        "url": url
    }