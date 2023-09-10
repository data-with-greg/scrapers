# otomoto_scraper
To gather data from otomoto.pl for analysis.

## Usage:

1. Install requirements. preferably in venv [steps here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

2. Create your scraper object anf fetch the data 

```python
import yaml
import datetime
from otomoto_scraper.scraper import OtomotoScraper


if __name__ == '__main__':
    setups = yaml.safe_load(open('./scraper_setups/setup.yaml'))
    today = datetime.datetime.now().isoformat()

    for setup in setups:
        region = setup['region']
        base_url = f'https://www.otomoto.pl/osobowe/uzywane/od-2015/{region}'
        params = setup['params']
        scraper = OtomotoScraper(base_url, params)
        upload_response = scraper.fetch_all_pages_s3(
            'data-with-greg-scrapers',
            f'{scraper.__class__.__name__}/{today}/{region}/{str(params)}'
        )
```