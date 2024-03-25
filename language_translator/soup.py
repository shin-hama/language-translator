from bs4 import BeautifulSoup
from pathlib import Path

file = Path("./samples/index.html")

with open(file, mode="r", encoding="utf-8-sig") as f:
    soup = BeautifulSoup(f, "html.parser")

for node in soup.find_all(text=True):
    if node.parent.name in ["code"]:
        print(node)
