import requests
import json
import time
import os
from finance.StockRecord import StockRecord

class YahooFinance:
    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.info = None
        self.records = None
        self.events = None
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }

    def get_chart(self, period1: int, period2: int,
                  interval: str = "1d",
                  include_prepost: bool = True,
                  events: str = "div|split|earn",
                  lang: str = "fr-FR",
                  region: str = "FR",
                  source: str = "cosaic") -> dict:
        """
        Fetch chart data from Yahoo Finance.
        """
        url = self.BASE_URL.format(symbol=self.symbol)
        params = {
            "period1": period1,
            "period2": period2,
            "interval": interval,
            "includePrePost": str(include_prepost).lower(),
            "events": events,
            "lang": lang,
            "region": region,
            "source": source,
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limited (429). Retrying after 5 seconds...")
            time.sleep(5)
            return self.get_chart(period1, period2, interval, include_prepost, events, lang, region, source)
        else:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")

    def save_chart(self, data: dict, period1: int, period2: int) -> str:
        """
        Save chart data to a JSON file inside the 'charts' directory.
        """
        os.makedirs("charts", exist_ok=True)
        filename = f"charts/{self.symbol}-{period1}-{period2}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
        return filename

    def load_chart_from_file(self, period1: int, period2: int) -> dict:
        """
        Load chart data from an existing file.
        """
        filename = f"charts/{self.symbol}-{period1}-{period2}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                #print(f"Loaded data from {filename}")
                return json.load(f)
        return None

    def get_or_load_chart(self, period1: int, period2: int, **kwargs) -> dict:
        """
        If chart file exists ? load from disk.
        Otherwise ? fetch from Yahoo Finance and save to file.
        """
        cached_data = self.load_chart_from_file(period1, period2)
        if cached_data is not None:
            return cached_data

        data = self.get_chart(period1, period2, **kwargs)
        self.save_chart(data, period1, period2)
        return data
    def get_histories(self, period1: int, period2: int, **kwargs):
        data = self.get_or_load_chart(period1, period2, **kwargs)
        self.info = data['chart']['result'][0]['meta'];
        self.events = data['chart']['result'][0]['events'];
		
        timestamps = data['chart']['result'][0]['timestamp']
        volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
		
		
        self.records = [StockRecord(ts, vol, cls) for ts, vol, cls in zip(timestamps, volumes, closes)]
        return self
