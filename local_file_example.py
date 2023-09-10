import yaml
import datetime
from otomoto_scraper.scraper import OtomotoScraper


if __name__ == '__main__':
    setups = yaml.safe_load(open('./scraper_setups/setup.yaml'))
    today = datetime.datetime.now().isoformat()

    for setup in setups[5:7]:
        region = setup['region']
        base_url = f'https://www.otomoto.pl/osobowe/uzywane/od-2015/{region}'
        params = setup['params']
        scraper = OtomotoScraper(base_url, params)
        # assuming `./data/` already exists
        upload_response = scraper.fetch_all_pages_file(
            f'data/{scraper.__class__.__name__}_{today}_{region}_{str(params)}.csv'
        )
