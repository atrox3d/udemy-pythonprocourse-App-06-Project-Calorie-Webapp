import requests
import json
import logging
from selectorlib import Extractor

logging.basicConfig(                                                            # configure root logger
    level=logging.INFO,
    format="%(asctime)s | %(module)-15s | %(levelname)-10s | %(message)s",
    datefmt='%Y/%m/%d %H:%M:%S',
    # stream=sys.stdout
)
log = logging.getLogger(__name__)                                               # get local logger


class Temperature:
    """
    Represent a temperature value extracted from the
    https://timeanddate.com/weather webpage
    """

    base_url = 'https://timeanddate.com/weather'                                # class variables
    json_headers_path = 'headers_for_scraping.json'
    yaml_path = 'temperature.yaml'

    def __init__(self, country, city):
        self.country = country
        self.city = city

    def _build_url(self):
        url = f'{self.base_url}/{self.country}/{self.city}'                     # compose url
        log.debug('url: %s', url)
        return url

    def _load_headers(self):
        with open(self.json_headers_path) as fp:                                # load headers from json into dict
            headers = json.load(fp)
        return headers

    def _scrape(self, use_headers=False):
        url = self._build_url()
        headers = self._load_headers() if use_headers else None

        try:
            response = requests.get(url, headers=headers)                       # try to get page
            response.raise_for_status()                                         # raise exception on error
        except requests.exceptions.RequestException as re:
            log.fatal(re)
            exit(1)
        finally:
            log.debug("response.status_code: %s", response.status_code)
            log.debug("response.encoding: %s", response.encoding)
            pass

        extractor = Extractor.from_yaml_file(self.yaml_path)                    # create extractor from yaml file
        log.debug("extractor.config: %s", extractor.config)

        full_content = response.text                                            # get page as text
        raw_value = extractor.extract(full_content)                             # get dict
        log.debug("raw_value: %s", raw_value)
        return raw_value

    def get(self):
        scraped_content = self._scrape()                                        # scrape temp
        log.debug(f"scraped_content: '{scraped_content}'")

        temp = scraped_content['temp']                                          # get value
        log.debug(f"temp: '{temp}'")

        # nbsp = u'\xa0'                                                          # define unicode &nbsp;
        # value = temp[:temp.index(nbsp)]                                         # extract before &nbsp;

        value, unit = temp.split()                                              # split at &nbsp;
        log.debug(f"value, unit: '{(value, unit)}'")

        value = float(value.strip())                                            # convert stripped value to float
        log.debug(f"value: '{value}'")

        return value


if __name__ == '__main__':                                                      # test the class
    temperature = Temperature('italy', 'turin').get()
    print(f'temperature: {temperature}')
