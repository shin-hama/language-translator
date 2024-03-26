from bs4 import BeautifulSoup
from pathlib import Path

file = Path("./samples/index.html")


def extract_text(node) -> str:
    if node.name in ["img", "code"]:
        return ""
    if node.name == "a":
        return node.get_text(strip=True)
    return node.get_text(strip=True)


with open(file, mode="r", encoding="utf-8-sig") as f:
    soup = BeautifulSoup(f, "html.parser")

for article in soup.find_all("article"):
    for node in article.find_all(string=True):
        if node.parent.name in ["code"]:
            print(node)
            continue

        # 子要素が img のときはスキップ
        if node.parent.find("img"):
            continue
        print(node.parent.name)
        print(node)
