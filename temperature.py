import requests
from selectorlib import Extractor

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(module)-15s | %(levelname)-10s | %(message)s",
    datefmt='%Y/%m/%d %H:%M:%S',
    # stream=sys.stdout
)
log = logging.getLogger(__name__)


class Temperature:
    """
    Represent a temperature value extracted from the
    https://timeanddate.com/weather webpage
    """
    def __init__(self, country, city, base_url='https://timeanddate.com/weather'):
        self.country = country
        self.city = city
        self.base_url = base_url

    def get(self):
        url = f'{self.base_url}/{self.country}/{self.city}'                     # compose url
        log.debug('url: %s', url)

        try:
            response = requests.get(url)                                        # try to get page
            response.raise_for_status()                                         # raise exception on error
        except requests.exceptions.RequestException as re:
            log.fatal(re)
            exit(1)
        finally:
            log.debug("response.status_code: %s", response.status_code)
            log.debug("response.encoding: %s", response.encoding)
            pass

        extractor = Extractor.from_yaml_file('temperature.yaml')                # create extractor from yaml file
        log.debug("extractor.config: %s", extractor.config)

        value = extractor.extract(response.text)['temp']                        # get value from dict
        log.debug("value: %s", value)

        nbsp = u'\xa0'                                                          # define unicode &nbsp;
        value = value[:value.index(nbsp)]                                       # extract before &nbsp;
        log.debug(f"value: '{value}'")

        value = float(value)                                                    # convert value to float
        log.debug(value)

        return value


if __name__ == '__main__':
    temperature = Temperature('italy', 'turin').get()
    print(f'temperature: {temperature}')
