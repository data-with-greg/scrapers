from otomoto_scraper.scraper import OtomotoScraper
import pandas as pd

if __name__ == '__main__':
    setups = [
        {
            'region': 'swietokrzyskie',
            'params': {
                'search[filter_enum_fuel_type]': 'petrol'
            }
        },
        {
            'region': 'podkarpackie',
            'params': {
                'search[filter_enum_fuel_type]': 'petrol'
            }
        }

    ]

    dfs = []
    for setup in setups:
        region = setup['region']
        base_url = f'https://www.otomoto.pl/osobowe/uzywane/od-2015/{region}'
        params = setup['params']
        scraper = OtomotoScraper(base_url, params)
        df = scraper.fetch_all_pages_pandas()
        dfs.append(df)

    full_df = pd.concat(dfs)
    print(full_df.describe())
