import os
import io
import logging
import requests
import multiprocessing
import pandas as pd
import boto3
from .parsers import OtomotoListingFullParser
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)


class OtomotoScraper:

    def __init__(self, base_url, params=None):
        if not params:
            params = {}
        self.session = requests.session()
        self.base_url = base_url
        self.params = params
        self.pages = self.get_last_page()

    def get_last_page(self):
        attrs = {'class': 'ooa-xdlax9 e1f09v7o0'}
        res = self.session.get(self.base_url, params=self.params)
        soup = BeautifulSoup(res.text, 'html.parser')
        pages = soup.find_all('a', attrs)
        vals = (int(i.text) for i in pages)
        return max(vals)

    def pages_params(self):
        pages_params = ({'page': i+1, 'search[order]': 'filter_float_price:desc'} for i in range(self.pages))
        return [dict(**i, **self.params) for i in pages_params]

    def fetch_page(self, params: dict = None):
        res = self.session.get(self.base_url, params=params)
        return res.text

    def parse_offers_divs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('article', {'class': 'ooa-1t80gpj ev7e6t818'})
        return [str(i) for i in divs]

    def fetch_all_pages_pandas(self):
        if self.pages > 500:
            log.warning(
                f'More than 500 pages ({self.pages}) detected. '
                f'Scraper will not collect whole data. Try to narrow the category'
            )

        pp = self.pages_params()

        with multiprocessing.Pool(8) as p:
            pages_html = p.map(self.fetch_page, pp)
            pages_items_divs = p.map(self.parse_offers_divs, pages_html)

        df = pd.DataFrame(data=(OtomotoListingFullParser(item).to_dict() for page in pages_items_divs for item in page))

        return df

    def fetch_all_pages_file(self, file_path):
        df = self.fetch_all_pages_pandas()
        df.to_csv(file_path)

    def fetch_all_pages_s3(self, s3_buket, s3_key):
        data = self.fetch_all_pages_pandas()
        file_like_object = io.StringIO()
        data.to_csv(file_like_object, index=False, header=False)
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
        res = s3.Object(s3_buket, s3_key).put(Body=file_like_object.getvalue())
        return res
