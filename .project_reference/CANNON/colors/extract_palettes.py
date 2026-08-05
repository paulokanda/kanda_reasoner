from html.parser import HTMLParser

HTML_CONTENT = """PASTE THE FULL HTML HERE"""  # Replace with the actual content

class PaletteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.in_colors = False
        self.in_span = False
        self.in_title = False
        self.title = ""
        self.colors = []
        self.palettes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and attrs.get("class") == "palette-card":
            self.in_card = True
            self.title = ""
            self.colors = []
        if self.in_card:
            if tag == "div" and attrs.get("class") == "palette-card_colors":
                self.in_colors = True
            if tag == "span":
                self.in_span = True
            if tag == "a" and "palette-card_name" in attrs.get("class", ""):
                self.in_title = True

    def handle_endtag(self, tag):
        if tag == "div" and self.in_card and not self.in_colors:
            if self.title or self.colors:
                self.palettes.append((self.title, ["#" + c for c in self.colors]))
            self.in_card = False
        if tag == "div" and self.in_colors:
            self.in_colors = False
        if tag == "span":
            self.in_span = False
        if tag == "a" and self.in_title:
            self.in_title = False

    def handle_data(self, data):
        if self.in_card and self.in_colors and self.in_span:
            self.colors.append(data.strip())
        if self.in_card and self.in_title:
            self.title = data.strip()


def main():
    parser = PaletteParser()
    parser.feed(HTML_CONTENT)
    # Print the Python list
    print("COOLORS_PALETTES = [")
    for title, colors in parser.palettes:
        print(f'    ("{title}", {colors}),')
    print("]")


if __name__ == "__main__":
    main()