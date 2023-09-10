# div class = ooa-1t80gpj ev7e6t818



from html.parser import HTMLParser


class OtomotoHTMLParser(HTMLParser):

    DIVS = []
    SHOULD_LOAD = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'class' and attr[1] == 'ooa-1t80gpj ev7e6t818':
                self.SHOULD_LOAD = True

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

