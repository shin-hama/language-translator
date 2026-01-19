from bs4 import BeautifulSoup
from pathlib import Path


file = Path("./samples/api/IContainerBase.html")

html = """
<h6><strong>Namespace</strong>: <a class="xref text-break" href="JEOL.html">JEOL</a>.<a class="xref text-break" href="JEOL.FEMTUS.html">FEMTUS</a>.<a class="xref text-break" href="JEOL.FEMTUS.Base.html">Base</a>.<a class="xref text-break" href="JEOL.FEMTUS.Base.ModuleManagerContract.html">Module<wbr>Manager<wbr>Contract</a></h6>
"""


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
    soup = BeautifulSoup(f, "html.parser")

# soup = BeautifulSoup(html, "html.parser")

for node in soup.find_all(string=True):
    if not contains_japanese(node.string):
        continue
    print(node.parent.name)
    print(node)
