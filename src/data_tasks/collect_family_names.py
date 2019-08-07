import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
source = "https://www.radixindex.com/hu/vezeteknevek"
starter = requests.get(source, headers={"User-Agent": ua.random}).content
ssoup = BeautifulSoup(starter, "lxml")
links = ssoup.find_all("a")
links = [l["href"] for l in links]
links = [
    l
    for l in links
    if l.startswith("https://www.radixindex.com/hu/vezeteknevek/abc_szerinti_mutato/")
]

with open("data/interim/vezeteknevek.txt", "w") as outfile:
    for link in links:
        content = requests.get(link, headers={"User-Agent": ua.random}).content
        soup = BeautifulSoup(content, "lxml")
        namelinks = soup.find_all("a")
        names = [
            l.text
            for l in namelinks
            if l["href"].startswith("/hu/vezeteknevek/vezeteknev/")
        ]
        for name in names:
            outfile.write(name + "\n")
