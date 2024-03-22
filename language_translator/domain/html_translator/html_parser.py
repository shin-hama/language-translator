from bs4 import NavigableString, Tag


class HTMLParser:
    def __init__(self):
        pass

    def parse(self, element: Tag | NavigableString) -> str:
        if element.name == "li":
            return self._parse_li(element)
        else:
            return element.get_text(strip=True)

    def _parse_li(self, li) -> str:
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

    def replace_parent_text(self, element, new_text: str):
        for child in element.children:
            if isinstance(child, NavigableString):
                child.replace_with(new_text)
