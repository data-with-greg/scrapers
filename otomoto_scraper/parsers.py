from html.parser import HTMLParser


class OtomotoListingParser(HTMLParser):
    SHOULD_LOAD_DATA = False
    SEARCHED_TAG = ''

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return NotImplementedError

    def handle_endtag(self, tag: str) -> None:
        return NotImplementedError

    def handle_data(self, data: str) -> None:
        return NotImplementedError


class OtomotoListingNameAndUrlParser(OtomotoListingParser):

    URL = None
    NAME = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for k, v in attrs:
            if k == 'class' and v.replace('""', '"') == 'ev7e6t89 ooa-1xvnx1e er34gjf0':
                self.SHOULD_LOAD_DATA =True

        if self.SHOULD_LOAD_DATA and tag == 'a':
            for k, v in attrs:
                if k == 'href':
                    self.URL = v.replace('""', '"')

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.NAME = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingIsHighlightedParser(OtomotoListingParser):

    IS_HIGHLIGHTED = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for k, v in attrs:
            if k == 'class' and v.replace('""', '"') == 'ooa-1wmudpx':
                self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA and data == 'Wyróżnione':
            self.IS_HIGHLIGHTED = True
            self.SHOULD_LOAD_DATA = False


class OtomotoListingParamParser(OtomotoListingParser):

    PARAM_VALUE = None

    def __init__(self, param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param = param

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'dd':
            for k, v in attrs:
                if k == 'data-parameter' and v.replace('""', '"') == self.param:
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.PARAM_VALUE = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListinPriceCurrencyParser(OtomotoListingParser):

    MAP = {
        'price': 'ev7e6t82 ooa-bz4efo er34gjf0',
        'currency': 'ev7e6t81 ooa-1e3jyoe er34gjf0'
    }
    VALUE = None
    def __init__(self, price_or_currency, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price_or_currency = price_or_currency

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {'h3', 'p'}:
            for k, v in attrs:
                if k == 'class' and v.replace('""', '"') == self.MAP[self.price_or_currency]:
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.VALUE = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingPricePlacementParser(OtomotoListingParser):

    PRICE_PLACEMENT = None
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'p':
            for k, v in attrs:
                if k == 'class' and v.replace('""', '"') == 'e1xj1nw30 ooa-77y3u4 er34gjf0':
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.PRICE_PLACEMENT = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingSellerParser(OtomotoListingParser):

    SELLER = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'li':
            for k, v in attrs:
                if k == 'class' and v.replace('""', '"') == 'ooa-17lclzg ef7ufbq5':
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.SELLER = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingRegionParser(OtomotoListingParser):

    REGION = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'p':
            for k, v in attrs:
                if k == 'class' and v.replace('""', '"') == 'ooa-gmxnzj':
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA and not self.REGION:
            self.REGION = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingDetailsParser(OtomotoListingParser):

    DETAILS = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'p':
            for k, v in attrs:
                if k == 'class' and v.replace('""', '"') == 'ev7e6t88 ooa-17thc3y er34gjf0':
                    self.SHOULD_LOAD_DATA = True

    def handle_data(self, data: str) -> None:
        if self.SHOULD_LOAD_DATA:
            self.DETAILS = data
            self.SHOULD_LOAD_DATA = False


class OtomotoListingFullParser:

    PARAMS = [
        'mileage', 'gearbox', 'year', 'fuel_type',
    ]

    PRICE_CURRENCY = [
        'price', 'currency'
    ]

    def __init__(self, listing):
        self.listing = listing

    def parse(self):
        parser = OtomotoListingNameAndUrlParser()
        parser.feed(self.listing)
        self.NAME, self.URL = parser.NAME, parser.URL

        parser = OtomotoListingIsHighlightedParser()
        parser.feed(self.listing)
        self.IS_HIGHLIGHTED = parser.IS_HIGHLIGHTED

        for param in [
            'mileage', 'gearbox', 'year', 'fuel_type',
        ]:
            parser = OtomotoListingParamParser(param)
            parser.feed(self.listing)
            setattr(self, param.upper(), parser.PARAM_VALUE)

        for param in [
            'price', 'currency'
        ]:
            parser = OtomotoListinPriceCurrencyParser(param)
            parser.feed(self.listing)
            setattr(self, param.upper(), parser.VALUE)

        parser = OtomotoListingPricePlacementParser()
        parser.feed(self.listing)
        self.PRICE_PLACEMENT = parser.PRICE_PLACEMENT

        parser = OtomotoListingSellerParser()
        parser.feed(self.listing)
        self.SELLER = parser.SELLER

        parser = OtomotoListingRegionParser()
        parser.feed(self.listing)
        self.REGION = parser.REGION

        parser = OtomotoListingDetailsParser()
        parser.feed(self.listing)
        self.DETAILS = parser.DETAILS

    def to_dict(self):
        self.parse()
        return {k.lower(): v for k, v in self.__dict__.items() if k != 'listing'}

    def __str__(self):
        return '\n'.join(f'{k}: {v}' for k, v in self.to_dict().items())


if __name__ == '__main__':
    SAMPLE_DIV = "<article class=""ooa-1t80gpj ev7e6t818"" data-id=""6114385372"" data-media-size=""large"" data-orientation=""horizontal""><style data-emotion=""ooa 1rnjex3"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1rnjex3{display:grid;border-radius:4px 4px 0 0;padding:16px;-webkit-column-gap:16px;column-gap:16px;background-color:#FFFFFF;}[data-highlighted] .ooa-1rnjex3{background-color:#ECF5FE;}[data-orientation=""horizontal""] .ooa-1rnjex3{row-gap:16px;grid:""thumbnail title price"" auto ""thumbnail content price"" auto ""thumbnail content price"" 1fr ""thumbnail content actions"" auto/minmax(auto, var(--media-width)) 1fr minmax(165px, 20%);}[data-orientation=""horizontal""][data-media-size=""large""] .ooa-1rnjex3{margin-left:auto;margin-right:auto;--media-width:388px;}@media (max-width: 1023px){[data-orientation=""horizontal""][data-media-size=""large""] .ooa-1rnjex3{--media-width:240px;}}@media (max-width: 767px){[data-orientation=""horizontal""][data-media-size=""large""] .ooa-1rnjex3{--media-width:328px;grid:""thumbnail thumbnail price"" auto ""title title actions"" auto ""content content content"" 1fr/1fr 1fr auto;}}@media (max-width: 575px){[data-orientation=""horizontal""][data-media-size=""large""] .ooa-1rnjex3{--media-width:328px;grid:""thumbnail thumbnail thumbnail"" auto ""price price price"" auto ""title title actions"" auto ""content content content"" 1fr/1fr 1fr auto;}}[data-orientation=""horizontal""][data-media-size=""small""] .ooa-1rnjex3{--media-width:240px;}@media (max-width: 767px){[data-orientation=""horizontal""][data-media-size=""small""] .ooa-1rnjex3{--media-width:160px;grid:""thumbnail thumbnail price"" auto ""title title actions"" auto ""content content content"" 1fr/1fr 1fr auto;}}@media (max-width: 1023px){[data-orientation=""horizontal""][data-media-size=""small""] .ooa-1rnjex3{--media-width:144px;}}@media (max-width: 575px){[data-orientation=""horizontal""][data-media-size=""small""] .ooa-1rnjex3{--media-width:160px;grid:""thumbnail price price"" auto ""title title actions"" auto ""content content content"" 1fr/minmax(50%, 1fr) minmax(90px, 50%) auto;}}[data-orientation=""vertical""] .ooa-1rnjex3{row-gap:16px;grid:""thumbnail"" ""price"" ""title"" ""content"" ""actions"";grid-template-columns:100%;}</style><section class=""ooa-1rnjex3 ev7e6t817""><style data-emotion=""ooa 10sl00i"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-10sl00i{position:relative;grid-area:thumbnail;border-radius:4px;overflow:hidden;aspect-ratio:4/3;position:relative;width:100%;background:#EBECEF;z-index:3;}[data-orientation=""horizontal""] .ooa-10sl00i{max-width:var(--media-width);}.ooa-10sl00i button{top:50%;z-index:3;}.ooa-10sl00i:hover button{-webkit-transition:all 0.3s ease;transition:all 0.3s ease;opacity:1;}</style><div class=""ooa-10sl00i e1j52kpv9""><style data-emotion=""ooa 959mto"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">[data-orientation=""horizontal""] .ooa-959mto>div:first-of-type,.ooa-959mto [data-testid=""carousel-container""]{position:relative;max-width:var(--media-width);aspect-ratio:4/3;}</style><style data-emotion=""ooa lalai8"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-lalai8{-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-flex-direction:column;-ms-flex-direction:column;flex-direction:column;width:100%;}[data-orientation=""horizontal""] .ooa-lalai8>div:first-of-type,.ooa-lalai8 [data-testid=""carousel-container""]{position:relative;max-width:var(--media-width);aspect-ratio:4/3;}</style><div class=""e1j52kpv4 ooa-lalai8""><style data-emotion=""ooa 1h7b6p7"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1h7b6p7{overflow:hidden;width:100%;}</style><div class=""ooa-1h7b6p7""><style data-emotion=""ooa 7wsc2v"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-7wsc2v{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-transform:translateX(0%);-moz-transform:translateX(0%);-ms-transform:translateX(0%);transform:translateX(0%);-webkit-transition:-webkit-transform 0.4s ease;transition:transform 0.4s ease;}</style><div class=""ooa-7wsc2v"" data-testid=""carousel-container""><style data-emotion=""ooa 17rb9mp"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-17rb9mp{-webkit-flex:1 0 100%;-ms-flex:1 0 100%;flex:1 0 100%;}</style><div aria-selected=""true"" class=""ooa-17rb9mp""><style data-emotion=""ooa 1mkj7ar"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1mkj7ar{display:block;height:100%;width:100%;position:relative;}</style><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><style data-emotion=""ooa ze54v0"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-ze54v0{object-position:center;object-fit:cover;border-radius:4px;aspect-ratio:4/3;width:100%;height:100%;}</style><style data-emotion=""ooa 182tnzm"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-182tnzm{visibility:visible;object-position:center;object-fit:cover;border-radius:4px;aspect-ratio:4/3;width:100%;height:100%;}</style><img alt=""alt"" class=""e1j52kpv7 ooa-182tnzm"" loading=""eager"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImJydThkZ25jbnV3NTEtT1RPTU9UT1BMIn0.ukCO1JARbFisiBOk9OvZi0TUEOUx7c0trW6_jrV6mu8/image;s=644x461""/></a></div><div aria-selected=""false"" class=""ooa-17rb9mp""><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><img alt=""alt"" class=""e1j52kpv7 ooa-182tnzm"" loading=""lazy"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IngwcHdldDM1MHNnNy1PVE9NT1RPUEwifQ.RAqicFlsU2EgA-yy6M8vujCfXS6REHNJo7KdNHfmHHU/image;s=644x461""/></a></div><div aria-selected=""false"" class=""ooa-17rb9mp""><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><img alt=""alt"" class=""e1j52kpv7 ooa-182tnzm"" loading=""lazy"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InFja3NqaHp2c3ZtcTMtT1RPTU9UT1BMIn0.xPr-2MUEuwiYYxWqvJnjFiYCxBqwCU9Rn3n4qiSGdaA/image;s=644x461""/></a></div><div aria-selected=""false"" class=""ooa-17rb9mp""><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><img alt=""alt"" class=""e1j52kpv7 ooa-182tnzm"" loading=""lazy"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjViZDh5eWUzczg5dC1PVE9NT1RPUEwifQ.nJ3WttkaSDEGyWSX7ADDW0owvVPWzUNxIxmQWITVOXo/image;s=644x461""/></a></div><div aria-selected=""false"" class=""ooa-17rb9mp""><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><img alt=""alt"" class=""e1j52kpv7 ooa-182tnzm"" loading=""lazy"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InlndHpreWFvc2E3Zi1PVE9NT1RPUEwifQ.rd0ItJiOeT7MEbmVZKPGIJRUPZkOnt3VzBAXcfcibOA/image;s=644x461""/></a></div><div aria-selected=""false"" class=""ooa-17rb9mp""><a class=""ooa-1mkj7ar e1j52kpv0"" href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html""><img alt=""see more"" class=""e1j52kpv7 ooa-182tnzm"" loading=""lazy"" src=""//statics.otomoto.pl/optimus-storage/a/otomotopl/images/listing/gallery-cta.svg""/></a></div></div></div><style data-emotion=""ooa 4yyn24"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-4yyn24{color:#020309;height:32px;width:32px;top:initial;bottom:initial;background:#FFFFFF;border-radius:4px;cursor:pointer;color:#DCDDE0;opacity:0;-webkit-transition:all 0.3s ease;transition:all 0.3s ease;margin-left:8px;}</style><style data-emotion=""ooa 1fjj731"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1fjj731{background:none;border:none;bottom:0;margin:0;padding:4px;position:absolute;top:0;left:0;color:#020309;height:32px;width:32px;top:initial;bottom:initial;background:#FFFFFF;border-radius:4px;cursor:pointer;color:#DCDDE0;opacity:0;-webkit-transition:all 0.3s ease;transition:all 0.3s ease;margin-left:8px;}</style><button aria-label=""Previous slide"" class=""e1j52kpv3 ooa-1fjj731"" disabled="""" type=""button""><svg class=""ooa-15wjrqi"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""m15.547 2-1.305 1.27L6 11.293v1.414l8.242 8.022L15.547 22H17v-1.414l-1.305-1.271L8.18 12l7.515-7.316L17 3.414V2z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg></button><style data-emotion=""ooa 1qsidqu"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1qsidqu{color:#020309;height:32px;width:32px;top:initial;bottom:initial;background:#FFFFFF;border-radius:4px;cursor:pointer;opacity:0;-webkit-transition:all 0.3s ease;transition:all 0.3s ease;margin-right:8px;}</style><style data-emotion=""ooa 1lq575q"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1lq575q{background:none;border:none;bottom:0;margin:0;padding:4px;position:absolute;top:0;right:0;color:#020309;height:32px;width:32px;top:initial;bottom:initial;background:#FFFFFF;border-radius:4px;cursor:pointer;opacity:0;-webkit-transition:all 0.3s ease;transition:all 0.3s ease;margin-right:8px;}</style><button aria-label=""Next slide"" class=""e1j52kpv2 ooa-1lq575q"" type=""button""><svg class=""ooa-15wjrqi"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""M7 2v1.414l1.271 1.27L15.586 12l-7.315 7.315L7 20.585V22h1.414l1.27-1.271L17 13.414l1-1v-.827l-3.942-3.942v-.001L9.686 3.271 8.413 2z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg></button><style data-emotion=""ooa 1cfv2wd"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1cfv2wd{position:absolute!important;bottom:0;}.ooa-1cfv2wd ol{margin:0;}.ooa-1cfv2wd ol li{position:relative;}.ooa-1cfv2wd ol li::after{display:block;content:"""";height:100%;width:100%;top:50%;left:50%;-webkit-transform:scale(2.5);-moz-transform:scale(2.5);-ms-transform:scale(2.5);transform:scale(2.5);}</style><div class=""ooa-1cfv2wd e1j52kpv5""><style data-emotion=""ooa 1o4a2sa"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1o4a2sa{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;-webkit-justify-content:center;justify-content:center;margin:32px 0 0;padding:0;}</style><ol class=""ooa-1o4a2sa""><style data-emotion=""ooa 12weay4"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-12weay4{border:solid 3px;border-color:#020309;border-radius:4px;cursor:pointer;display:inline-block;height:8px;margin:0 4px 16px;width:8px;border-color:#FFFFFF;}</style><li class=""ooa-12weay4"" data-testid=""indicator-0""></li><style data-emotion=""ooa 1u3whs7"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1u3whs7{border:solid 1px;border-color:#020309;border-radius:4px;cursor:pointer;display:inline-block;height:8px;margin:0 4px 16px;width:8px;border-color:#FFFFFF;}</style><li class=""ooa-1u3whs7"" data-testid=""indicator-1""></li><li class=""ooa-1u3whs7"" data-testid=""indicator-2""></li><li class=""ooa-1u3whs7"" data-testid=""indicator-3""></li><li class=""ooa-1u3whs7"" data-testid=""indicator-4""></li><li class=""ooa-1u3whs7"" data-testid=""indicator-5""></li></ol></div><style data-emotion=""ooa 12ucnaz"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-12ucnaz{background:#FFFFFF;color:#020309;}</style><style data-emotion=""ooa kieaiu"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-kieaiu{-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;border-radius:12px;bottom:8px;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-flex-flow:row nowrap;-webkit-flex-flow:row nowrap;-ms-flex-flow:row nowrap;flex-flow:row nowrap;padding:4px 8px;position:absolute;right:8px;background:#FFFFFF;color:#020309;}</style><div class=""ooa-kieaiu""><style data-emotion=""ooa 1moilzm"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1moilzm{height:16px;width:16px;margin-right:8px;color:inherit;}</style><svg class=""ooa-1moilzm"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""m15.72 3 1 3H21l1 1v13l-1 1H3l-1-1V7l1-1h4.28l1-3h7.44zm-1.44 2H9.72l-1 3H4v11h16V8h-4.72l-1-3zM12 8c2.757 0 5 2.243 5 5s-2.243 5-5 5-5-2.243-5-5 2.243-5 5-5zm0 2c-1.655 0-3 1.345-3 3s1.345 3 3 3 3-1.345 3-3-1.345-3-3-3z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg><style data-emotion=""ooa ev2y9w"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-ev2y9w{font-size:12px;line-height:14px;color:inherit;margin:0;}</style><p class=""ooa-ev2y9w er34gjf0"">1<!-- --> / <!-- -->6</p></div></div></div><style data-emotion=""ooa 1jgmfmo"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1jgmfmo{grid-area:title;display:grid;}</style><div class=""ooa-1jgmfmo ev7e6t812""><style data-emotion=""ooa 1jxof7b"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1jxof7b{white-space:nowrap;overflow:hidden;font-weight:600;text-overflow:ellipsis;}.ooa-1jxof7b>a{position:static!important;color:#020309;}.ooa-1jxof7b>a::after{position:absolute;z-index:1;content:"""";inset:0;}</style><style data-emotion=""ooa 1xvnx1e"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1xvnx1e{font-size:16px;line-height:20px;color:#020309;margin:0;white-space:nowrap;overflow:hidden;font-weight:600;text-overflow:ellipsis;}.ooa-1xvnx1e>a{position:static!important;color:#020309;}.ooa-1xvnx1e>a::after{position:absolute;z-index:1;content:"""";inset:0;}</style><h1 class=""ev7e6t89 ooa-1xvnx1e er34gjf0""><a href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html"" rel=""noreferrer"" target=""_self"">Mercedes-Benz GLE 300 d 4-Matic</a></h1><style data-emotion=""ooa 1sgl6gl"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1sgl6gl{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#66676C;}[data-orientation=""horizontal""] .ooa-1sgl6gl{font-weight:400;font-size:12px;line-height:14px;}[data-orientation=""vertical""] .ooa-1sgl6gl{font-weight:400;font-size:12px;line-height:14px;}</style><style data-emotion=""ooa 17thc3y"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-17thc3y{font-size:14px;line-height:18px;color:#020309;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#66676C;}[data-orientation=""horizontal""] .ooa-17thc3y{font-weight:400;font-size:12px;line-height:14px;}[data-orientation=""vertical""] .ooa-17thc3y{font-weight:400;font-size:12px;line-height:14px;}</style><p class=""ev7e6t88 ooa-17thc3y er34gjf0"">1 993 cm3 • 272 KM • GLE 300 d 4-Matic</p></div><style data-emotion=""ooa d3dp2q"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-d3dp2q{grid-area:content;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-flex-flow:column nowrap;-webkit-flex-flow:column nowrap;-ms-flex-flow:column nowrap;flex-flow:column nowrap;row-gap:16px;}</style><div class=""ooa-d3dp2q ev7e6t816""><style data-emotion=""ooa kciok9"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-kciok9{--items-gap:8px;--closed-height:56px;max-height:none;overflow:hidden;position:relative;}</style><div class=""ev7e6t815 ooa-kciok9 e4zik2l2""><style data-emotion=""ooa 1w54fmr"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1w54fmr{list-style:none;padding:0;margin:0 0 0 -1px;float:right;width:100%;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-flex-wrap:wrap;-webkit-flex-wrap:wrap;-ms-flex-wrap:wrap;flex-wrap:wrap;gap:var(--items-gap);}</style><ul class=""ooa-1w54fmr e4zik2l1""><li class=""ooa-0 e4zik2l0""><style data-emotion=""ooa 1r0pwxd"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1r0pwxd{background-color:#BDE0FF;height:24px;padding:2px 8px;}.ooa-1r0pwxd>div{font-size:14px;line-height:14px;}</style><style data-emotion=""ooa 1kep8r0"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1kep8r0{-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;border:none;border-radius:4px;box-shadow:none;cursor:pointer;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;font-family:system-ui,-apple-system,""Segoe UI"",Roboto,Helvetica,Arial,sans-serif;line-height:18px;padding:7px 16px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;background:#DCDDE0;cursor:pointer;outline:none;pointer-events:none;background-color:#BDE0FF;height:24px;padding:2px 8px;}.ooa-1kep8r0:disabled{color:#A1A2A5;cursor:default;pointer-events:none;}.ooa-1kep8r0:disabled svg{color:#A1A2A5;}.ooa-1kep8r0:focus-visible:not(:active){outline:4px solid #BDE0FF;}.ooa-1kep8r0>div{font-size:14px;line-height:14px;}</style><button class=""e4zik2l4 ooa-1kep8r0"" role=""button""><div class=""ooa-1wmudpx"">Wyróżnione</div></button></li></ul></div><style data-emotion=""ooa 13lipl2"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">[data-orientation=""horizontal""] .ooa-13lipl2{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-flex-wrap:wrap;-webkit-flex-wrap:wrap;-ms-flex-wrap:wrap;flex-wrap:wrap;gap:8px 18px;}[data-orientation=""vertical""] .ooa-13lipl2{display:grid;-webkit-column-gap:16px;column-gap:16px;row-gap:4px;grid-template-columns:auto;grid-template-rows:max-content;grid-template-areas:""a b"";}</style><dl class=""ooa-13lipl2 ev7e6t87""><dt class=""ooa-eivff4 ev7e6t86"">Przebieg</dt><style data-emotion=""ooa 1smopdt"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1smopdt{height:18px;display:grid;grid-auto-flow:column;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;grid-template-columns:max-content;-webkit-column-gap:6px;column-gap:6px;font-weight:400;font-size:14px;line-height:18px;white-space:nowrap;}[data-orientation=""vertical""] .ooa-1smopdt{min-width:101px;}.ooa-1smopdt>svg{height:auto;width:auto;}</style><dd class=""ooa-1smopdt ev7e6t85"" data-parameter=""mileage""><svg class=""ooa-51p4fw"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""m16.474 4 5.897 16.083h-2.13L14.343 4h2.13zm-6.446 0L4.13 20.083H2L7.898 4h2.13zm2.982 11v4h-2v-4h2zm0-4.958v3h-2v-3h2zm0-4.042v2h-2V6h2z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg>30 429 km</dd><dt class=""ooa-eivff4 ev7e6t86"">Rodzaj paliwa</dt><dd class=""ooa-1smopdt ev7e6t85"" data-parameter=""fuel_type""><svg class=""ooa-51p4fw"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""m13 2 1 1v7h1c1.206 0 3 .799 3 3v6c.012.449.195 1 1 1 .806 0 .988-.55 1-1.011V6.42l-1.408-1.38H16L15 4l1-.96h3.408L22 5.58V19c0 1.206-.799 3-3 3-2.2 0-3-1.794-3-3v-6c0-.806-.55-.99-1.011-1H14v10H3V3l1-1h9zm-1 2H5v16h7V4zm-1.003 1v4H6V5h4.997z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg>Diesel</dd><dt class=""ooa-eivff4 ev7e6t86"">Skrzynia biegów</dt><dd class=""ooa-1smopdt ev7e6t85"" data-parameter=""gearbox""><svg class=""ooa-51p4fw"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""M21 5a2 2 0 0 0-4 0c0 .738.405 1.376 1 1.723v3.863l-.414.414H13V6.745A1.991 1.991 0 0 0 14.042 5a2 2 0 0 0-4 0c0 .721.385 1.348.958 1.7V11H6V6.723A1.994 1.994 0 0 0 5 3a1.994 1.994 0 0 0-1 3.723v10.554c-.595.347-1 .984-1 1.723a2 2 0 0 0 4 0c0-.739-.405-1.376-1-1.723V13h5v4.3a1.99 1.99 0 0 0-.958 1.7 2 2 0 0 0 4 0A1.99 1.99 0 0 0 13 17.255V13h5.414L20 11.414v-4.69c.595-.348 1-.986 1-1.724"" fill=""currentColor"" fill-rule=""evenodd""></path></svg>Automatyczna</dd><dt class=""ooa-eivff4 ev7e6t86"">Rok produkcji</dt><dd class=""ooa-1smopdt ev7e6t85"" data-parameter=""year""><svg class=""ooa-51p4fw"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""M8.006 2v1h8.007V2h2.002v1h2.984L22 4v17l-1 1H3l-1-1V4l1-1h3.004V2h2.002zm11.992 8H4.002v10h15.996V10zM7.505 12a1.5 1.5 0 1 1 .001 3 1.5 1.5 0 0 1 0-3.001zM6.004 5H4.002v3h15.996V5h-1.983v1l-1.001 1-1.001-1V5H8.006v1L7.005 7 6.004 6V5z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg>2022 </dd></dl><style data-emotion=""ooa 1o0axny"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1o0axny{display:grid;row-gap:8px;grid-auto-flow:row;}</style><dl class=""ooa-1o0axny ev7e6t84""><style data-emotion=""ooa 16w655c"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-16w655c{font-weight:400;font-size:12px;line-height:14px;display:grid;grid-auto-flow:column;grid-template-columns:max-content;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-column-gap:6px;column-gap:6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}.ooa-16w655c>svg{height:auto;width:auto;}</style><dd class=""ooa-16w655c ev7e6t83""><style data-emotion=""ooa ex9lao"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-ex9lao{font-size:12px;line-height:14px;}</style><style data-emotion=""ooa gmxnzj"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-gmxnzj{color:#020309;font-family:system-ui,-apple-system,""Segoe UI"",Roboto,Helvetica,Arial,sans-serif;font-weight:400;-webkit-text-decoration:none;text-decoration:none;font-size:12px;line-height:14px;}</style><p class=""ooa-gmxnzj"">Sękocin Nowy (Mazowieckie)</p></dd><dd class=""ooa-16w655c ev7e6t83""><p class=""ooa-gmxnzj"">Podbite </p></dd></dl><style data-emotion=""ooa zqnl66"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-zqnl66{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-flex-direction:column;-ms-flex-direction:column;flex-direction:column;gap:16px;}</style><article class=""ooa-zqnl66 ef7ufbq9""><style data-emotion=""ooa 1aqz693"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1aqz693{display:grid;gap:8px;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));}@media (min-width: 1280px){.ooa-1aqz693{grid-template-columns:repeat(auto-fill, minmax(300px, 1fr));}}</style><ol class=""ooa-1aqz693 ef7ufbq10""><style data-emotion=""ooa txxb35"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-txxb35{-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-webkit-justify-content:space-between;justify-content:space-between;width:100%;cursor:pointer;padding:8px;border:1px solid #DCDDE0;border-radius:4px;position:relative;}.ooa-txxb35>img{max-width:112px;}.ooa-txxb35 a::after{position:absolute;z-index:1;content:"""";inset:0;}</style><li class=""ooa-txxb35 ef7ufbq8""><style data-emotion=""ooa jz6npm"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-jz6npm{font-weight:400;font-size:12px;line-height:14px;display:grid;grid-auto-flow:column;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;grid-template-columns:auto 1fr;-webkit-column-gap:6px;column-gap:6px;white-space:nowrap;}.ooa-jz6npm>svg{height:auto;width:auto;}</style><div class=""ooa-jz6npm ef7ufbq6""><style data-emotion=""ooa tcvvct"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-tcvvct{object-fit:contain;object-position:left;max-width:152px;height:24px;}</style><style data-emotion=""ooa phxfl2"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-phxfl2{visibility:visible;object-fit:contain;object-position:left;max-width:152px;height:24px;}</style><img alt=""RENAULT KRUBAGROUP Autoryzowany koncesjoner Renault i Dacia"" class=""e719ay80 ooa-phxfl2"" loading=""lazy"" src=""https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjUxZW51aHBicGw2NDMtT1RPTU9UT1BMIn0.nQNzklnXeUIyKH_eFSVZl-3nJq-b84ALUt7BhyF5WyM/image;s=140x24""/></div><style data-emotion=""ooa 1xpspme"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1xpspme{font-weight:700;font-size:14px;line-height:18px;color:#0071CE;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;display:grid;grid-template-columns:1fr auto;white-space:nowrap;}.ooa-1xpspme>svg{margin-left:8px;color:#0071CE;height:auto;width:auto;}</style><a class=""ooa-1xpspme ef7ufbq7"" href=""https://kruba.otomoto.pl"">Zobacz ogłoszenia<svg class=""ooa-51p4fw"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""m8.453 22 1.305-1.27L18 12.706v-1.414L9.758 3.271 8.453 2H7v1.414l1.305 1.271L15.82 12l-7.515 7.315L7 20.587V22z"" fill=""currentColor"" fill-rule=""evenodd""></path></svg></a></li></ol><style data-emotion=""ooa zzalab"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-zzalab{display:grid;grid-template-areas:""title"" ""services"";row-gap:6px;}</style><li class=""ooa-zzalab ef7ufbq4""><style data-emotion=""ooa wwwj3"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-wwwj3{display:grid;grid-area:title;font-weight:600;font-size:14px;line-height:18px;}</style><style data-emotion=""ooa mveekp"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-mveekp{font-size:14px;line-height:18px;display:grid;grid-area:title;font-weight:600;font-size:14px;line-height:18px;}</style><style data-emotion=""ooa 1id8mfc"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1id8mfc{color:#020309;font-family:system-ui,-apple-system,""Segoe UI"",Roboto,Helvetica,Arial,sans-serif;font-weight:400;-webkit-text-decoration:none;text-decoration:none;font-size:14px;line-height:18px;display:grid;grid-area:title;font-weight:600;font-size:14px;line-height:18px;}</style><p class=""ef7ufbq3 ooa-1id8mfc"">RENAULT KRUBAGROUP Autoryzowany koncesjoner Renault i Dacia</p><style data-emotion=""ooa lpxytg"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-lpxytg{grid-area:services;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;gap:4px;-webkit-box-flex-flow:row wrap;-webkit-flex-flow:row wrap;-ms-flex-flow:row wrap;flex-flow:row wrap;}</style><ul class=""ooa-lpxytg ef7ufbq2""><style data-emotion=""ooa 1otiv30"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1otiv30{font-size:12px;}.ooa-1otiv30::before{content:""•"";margin-right:4px;}.ooa-1otiv30:first-of-type::before{display:none;}</style><li class=""ooa-1otiv30 ef7ufbq1"">Usługi finansowe</li><li class=""ooa-1otiv30 ef7ufbq1"">Naprawa samochodów</li><li class=""ooa-1otiv30 ef7ufbq1"">Usługi ubezpieczeniowe</li><li class=""ooa-1otiv30 ef7ufbq1"">Szybka naprawa</li></ul></li></article></div><style data-emotion=""ooa j0d5pq"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-j0d5pq{grid-area:price;max-width:100%;}[data-orientation=""horizontal""] .ooa-j0d5pq{text-align:right;justify-self:end;}[data-media-size=""large""] .ooa-j0d5pq{width:100%;}[data-orientation=""vertical""] .ooa-j0d5pq{text-align:left;margin-bottom:-8px;}</style><div class=""ooa-j0d5pq ev7e6t813""><div hidden=""""><a href=""https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gle-gle-300-d-4-matic-ID6FNkVU.html"">ad link</a><div><ul><li>2022 </li></ul></div></div><style data-emotion=""ooa 1t7cj0c"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1t7cj0c{display:grid;grid-template-rows:auto 1fr;-webkit-align-items:start;-webkit-box-align:start;-ms-flex-align:start;align-items:start;}[data-orientation=""horizontal""] .ooa-1t7cj0c{gap:4px;}@media (max-width: 575px){[data-large-media] .ooa-1t7cj0c{display:grid;grid-auto-flow:row;grid-template-columns:auto auto auto;}}@media (min-width: 576px){.ooa-1t7cj0c{grid-auto-flow:row;}}</style><div class=""ooa-1t7cj0c ermhljg4""><style data-emotion=""ooa 11wting"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-11wting{grid-row-start:1;margin-bottom:4px;}@media (max-width: 575px){[data-large-media] .ooa-11wting{grid-area:1/3;}}</style><style data-emotion=""ooa 1wb7q8u"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1wb7q8u{display:grid;grid-template-areas:""gross currency"" ""net net"";-webkit-column-gap:4px;column-gap:4px;}[data-orientation=""horizontal""] .ooa-1wb7q8u{grid-template-columns:1fr auto;row-gap:4px;}[data-orientation=""vertical""] .ooa-1wb7q8u{grid-template-columns:auto 1fr;text-overflow:ellipsis;}</style><div class=""ooa-1wb7q8u ev7e6t814""><style data-emotion=""ooa 1vc4ye9"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1vc4ye9{grid-area:gross;white-space:nowrap;font-weight:600;}[data-orientation=""horizontal""] .ooa-1vc4ye9{line-height:26px;justify-self:end;font-size:24px;}@media (max-width: 1023px){[data-orientation=""horizontal""] .ooa-1vc4ye9{font-size:20px;line-height:22px;}}[data-orientation=""vertical""] .ooa-1vc4ye9{font-size:20px;line-height:22px;}</style><style data-emotion=""ooa bz4efo"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-bz4efo{font-size:24px;line-height:26px;font-weight:700;color:#020309;margin:0;grid-area:gross;white-space:nowrap;font-weight:600;}[data-orientation=""horizontal""] .ooa-bz4efo{line-height:26px;justify-self:end;font-size:24px;}@media (max-width: 1023px){[data-orientation=""horizontal""] .ooa-bz4efo{font-size:20px;line-height:22px;}}[data-orientation=""vertical""] .ooa-bz4efo{font-size:20px;line-height:22px;}</style><h3 class=""ev7e6t82 ooa-bz4efo er34gjf0"">355 000</h3><style data-emotion=""ooa 11ghb62"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-11ghb62{grid-area:currency;font-weight:400;line-height:18px;font-size:14px;-webkit-align-self:center;-ms-flex-item-align:center;align-self:center;}@media (max-width: 767px){.ooa-11ghb62{font-size:12px;}}</style><style data-emotion=""ooa 1e3jyoe"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1e3jyoe{font-weight:500;font-size:16px;line-height:20px;color:#020309;margin:0;grid-area:currency;font-weight:400;line-height:18px;font-size:14px;-webkit-align-self:center;-ms-flex-item-align:center;align-self:center;}@media (max-width: 767px){.ooa-1e3jyoe{font-size:12px;}}</style><p class=""ev7e6t81 ooa-1e3jyoe er34gjf0"">PLN</p></div><style data-emotion=""ooa 1yf0cv5"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1yf0cv5{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;height:36px;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:end;-ms-flex-pack:end;-webkit-justify-content:flex-end;justify-content:flex-end;}</style><div class=""ooa-1yf0cv5 ermhljg0""><style data-emotion=""ooa kd0xqk"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-kd0xqk{z-index:2;position:relative;}.ooa-kd0xqk,.ooa-kd0xqk p{display:inline;}.ooa-kd0xqk>span{margin-right:4px;vertical-align:middle;}.ooa-kd0xqk p{margin:0;}@media (min-width: 1024px){.ooa-kd0xqk{grid-row-start:2;}}@media (max-width: 767px){.ooa-kd0xqk{margin:0;-webkit-box-pack:end;-ms-flex-pack:end;-webkit-justify-content:flex-end;justify-content:flex-end;}}</style><style data-emotion=""ooa wmopop"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-wmopop{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-flex-direction:row;-ms-flex-direction:row;flex-direction:row;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-top:8px;-webkit-box-pack:end;-ms-flex-pack:end;-webkit-justify-content:end;justify-content:end;z-index:2;position:relative;}@media (min-width: 768px){.ooa-wmopop{-webkit-flex-direction:row;-ms-flex-direction:row;flex-direction:row;margin-top:0;}}.ooa-wmopop,.ooa-wmopop p{display:inline;}.ooa-wmopop>span{margin-right:4px;vertical-align:middle;}.ooa-wmopop p{margin:0;}@media (min-width: 1024px){.ooa-wmopop{grid-row-start:2;}}@media (max-width: 767px){.ooa-wmopop{margin:0;-webkit-box-pack:end;-ms-flex-pack:end;-webkit-justify-content:flex-end;justify-content:flex-end;}}</style><div class=""ermhljg1 ooa-wmopop e1xj1nw31""><span><svg data-testid=""pe_icon_badge_in"" height=""0.5em"" style=""font-size:24px;color:#0071CE"" viewbox=""0 0 32 16"" width=""1em""><svg class=""ooa-1dwk0yu ew9ete61""><use href=""#icon-sprite-priceEvaluationIN""></use></svg></svg></span><style data-emotion=""ooa 41z2a4"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-41z2a4{margin-left:8px;margin-right:0;font-weight:400;font-size:12px;margin-left:4px;font-size:14px;}@media (min-width: 768px){.ooa-41z2a4{margin-left:4px;margin-right:0;font-size:14px;}}@media (max-width: 575px){.ooa-41z2a4{white-space:normal;}}</style><style data-emotion=""ooa 77y3u4"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-77y3u4{font-size:14px;line-height:18px;color:#020309;margin:0;margin-left:8px;margin-right:0;font-weight:400;font-size:12px;margin-left:4px;font-size:14px;}@media (min-width: 768px){.ooa-77y3u4{margin-left:4px;margin-right:0;font-size:14px;}}@media (max-width: 575px){.ooa-77y3u4{white-space:normal;}}</style><p class=""e1xj1nw30 ooa-77y3u4 er34gjf0"">W granicach średniej</p></div></div><style data-emotion=""ooa 109638"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-109638{grid-row-start:3;}@media (max-width: 575px){.ooa-109638:empty{visibility:hidden;}}@media (min-width: 576px){.ooa-109638:empty{display:none;}}.ooa-109638 .fin_link_list_main{text-align:right;padding:0;}@media (max-width: 575px){[data-large-media] .ooa-109638{grid-row-start:1;grid-row-end:span 2;grid-column-end:span 2;}[data-large-media] .ooa-109638 .fin_link_list_main{text-align:left;}}</style><style data-emotion=""ooa rmi0k6"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-rmi0k6{grid-row-start:3;}.ooa-rmi0k6 .fin_link_list_span_from{font-weight:normal;font-size:12px;color:#020309;}.ooa-rmi0k6 .fin_link_list_span_price{font-size:16px;color:#020309;font-weight:600;}.ooa-rmi0k6 .fin_link_list_main>a{font-size:14px;-webkit-text-decoration:underline;text-decoration:underline;}@media (max-width: 575px){.ooa-rmi0k6:empty{visibility:hidden;}}@media (min-width: 576px){.ooa-rmi0k6:empty{display:none;}}.ooa-rmi0k6 .fin_link_list_main{text-align:right;padding:0;}@media (max-width: 575px){[data-large-media] .ooa-rmi0k6{grid-row-start:1;grid-row-end:span 2;grid-column-end:span 2;}[data-large-media] .ooa-rmi0k6 .fin_link_list_main{text-align:left;}}</style><span aria-hidden=""true"" class=""ermhljg2 ooa-rmi0k6"" data-image="""" data-make="""" data-placeholder=""financing-widget"" data-price=""355000"" data-testid=""financing-widget"" data-title=""Mercedes-Benz GLE 300 d 4-Matic""></span></div></div><style data-emotion=""ooa 1wzro4r"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-1wzro4r{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-align-items:end;-webkit-box-align:end;-ms-flex-align:end;align-items:end;-webkit-box-pack:end;-ms-flex-pack:end;-webkit-justify-content:end;justify-content:end;gap:8px;-webkit-box-flex-flow:row-reverse nowrap;-webkit-flex-flow:row-reverse nowrap;-ms-flex-flow:row-reverse nowrap;flex-flow:row-reverse nowrap;grid-area:actions;}@media (min-width: 768px){.ooa-1wzro4r{-webkit-flex-direction:column-reverse;-ms-flex-direction:column-reverse;flex-direction:column-reverse;}}@media (max-width: 767px){.ooa-1wzro4r{gap:16px;-webkit-align-items:start;-webkit-box-align:start;-ms-flex-align:start;align-items:start;-webkit-align-self:start;-ms-flex-item-align:start;align-self:start;}}</style><div class=""ooa-1wzro4r ev7e6t811""><style data-emotion=""ooa dnhbnu"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-dnhbnu{width:24px;height:24px;}</style><style data-emotion=""ooa krgcpk"" nonce=""HK9DOmVmido/9NL+N91j1Q=="">.ooa-krgcpk{--displayUnderline:none;border:none;border-radius:4px;box-sizing:border-box;cursor:pointer;font-family:system-ui,-apple-system,""Segoe UI"",Roboto,Helvetica,Arial,sans-serif;font-size:16px;font-weight:700;height:48px;letter-spacing:0.7px;line-height:20px;padding-left:32px;padding-right:32px;position:relative;text-align:center;white-space:nowrap;width:auto;--mainColor:#0071CE;--outlineColor:#BDE0FF;background:transparent;color:var(--mainColor);padding-left:0;padding-right:0;width:24px;height:24px;}.ooa-krgcpk:disabled{pointer-events:none;}.ooa-krgcpk svg{color:var(--mainColor);}.ooa-krgcpk:active{--mainColor:#66676C;}.ooa-krgcpk:disabled{--mainColor:#A1A2A5;}.ooa-krgcpk:hover:not(:active){--mainColor:#66676C;}.ooa-krgcpk:focus-visible:not(:active, :hover){outline:4px solid var(--outlineColor);}</style><button class=""ev7e6t810 ooa-krgcpk"" type=""button""><span class=""ooa-ucvp6h""><span class=""ooa-1iivig8""><svg class=""ooa-1bnih2v"" height=""1em"" viewbox=""0 0 24 24"" width=""1em"" xmlns=""http://www.w3.org/2000/svg""><path d=""M20.219 10.367 12 20.419 3.806 10.4A3.96 3.96 0 0 1 3 8c0-2.206 1.795-4 4-4a4.004 4.004 0 0 1 3.868 3h2.264A4.003 4.003 0 0 1 17 4c2.206 0 4 1.794 4 4 0 .868-.279 1.698-.781 2.367M17 2a5.999 5.999 0 0 0-5 2.686A5.999 5.999 0 0 0 7 2C3.692 2 1 4.691 1 8a5.97 5.97 0 0 0 1.232 3.633L10.71 22h2.582l8.501-10.399A5.943 5.943 0 0 0 23 8c0-3.309-2.692-6-6-6"" fill=""currentColor"" fill-rule=""evenodd""></path></svg></span></span></button></div></section></article>"
    parser = OtomotoListingFullParser(SAMPLE_DIV.replace('""', '"'))
    print(parser)