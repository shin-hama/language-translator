from pathlib import Path
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


html_doc = """
<ul>
  <li>
    Quick Start
    <ul>
      <li><a href="#loading-modules">Loading Modules</a></li>
      <li><a href="#hello-world">Hello World</a></li>
      <li><a href="#creating-gui">Creating GUI</a></li>
    </ul>
  </li>
</ul>
"""


def parse(element: Tag | NavigableString) -> str:
    if element.name == "li":
        return parse_li(element)
    else:
        return "element.get_text(strip=True)"


def parse_li(li):
    """
    リストアイテム(li)のテキストを返す
    ※ li内の入れ子リストは除外する (重複するため)
    """
    buffer = []
    for child in li:
        if isinstance(child, NavigableString):
            buffer.append(child.get_text(strip=True))
        elif isinstance(child, Tag):
            # リスト構造ではない child のみ返り値に含める
            if child.find_all("li") == []:
                buffer.append(child.get_text(strip=True))
    return "".join(buffer).strip().rstrip("\r\n")


def replace_parent_text(element, new_text):
    for child in element.children:
        if isinstance(child, NavigableString):
            child.replace_with(new_text)


root_dir = Path("./samples")
file = Path(root_dir / "_index.html")

# with open(file, mode="r", encoding="utf-8") as f:
#     html_doc = f.read()

soup = BeautifulSoup(html_doc, "html.parser")


# 直下の ul タグ内のテキストを取得
for element in [
    elm for elm in soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"])
]:
    replace_parent_text(element, "content")

print(soup.prettify())
