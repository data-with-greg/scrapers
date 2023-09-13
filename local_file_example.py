import re
import yaml
import datetime
from otomoto_scraper.scraper import OtomotoScraper


def replace_special(string):
    return re.sub('[^a-zA-Z0-9_]', '', string)


if __name__ == '__main__':
    setups = yaml.safe_load(open('./scraper_setups/setup.yaml'))
    today = datetime.datetime.now().isoformat()

    for setup in setups[5:6]:
        region = setup['region']
        base_url = f'https://www.otomoto.pl/osobowe/uzywane/od-2015/{region}'
        params = setup['params']
        scraper = OtomotoScraper(base_url, params)
        # assuming `./data/` already exists
        upload_response = scraper.fetch_all_pages_file(
            f'data/{scraper.__class__.__name__}_{replace_special(today)}_{region}_{replace_special(str(params))}.csv'
        )
