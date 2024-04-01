from bs4 import BeautifulSoup
from pathlib import Path


file = Path("./samples/xml/sample.xml")


def contains_japanese(text: str) -> bool:
    for character in text:
        if (
            "\u3040" <= character <= "\u309F"
            or "\u30A0" <= character <= "\u30FF"
            or "\u4E00" <= character <= "\u9FAF"
        ):
            return True
    return False


with open(file, mode="r", encoding="utf-8-sig") as f:
    soup = BeautifulSoup(f, "lxml-xml")

for node in soup.find_all(string=True):
    if not contains_japanese(node.string):
        continue

    print(node.string)
    node.replace_with("translated text")

print(soup.prettify())
