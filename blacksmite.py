import requests

from pyquery import PyQuery
from time import perf_counter
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from src import Publicators
from src import logger


class Main:
    def __init__(self) -> None:
        self.__executor = ThreadPoolExecutor(max_workers=10)

        self.MAIN_URL = 'https://www.sipri.org/publications/search'

    def execute(self):
        all_page_urls = []

        response = requests.get(self.MAIN_URL)
        page = 1
        while True:
            html = PyQuery(response.text)

            try:
                url_page = self.MAIN_URL+html.find('#sipri-2016-content a[title="Go to next page"]').attr('href')
            except Exception:
                break

            logger.info(f'Fetch url page: {page}')
            page+=1

            all_page_urls.append(url_page)
            response = requests.get(url_page)


        for page_url in tqdm(all_page_urls,ascii=True, 
                                            smoothing=0.1,
                                            total=len(all_page_urls)):
            sipri = Publicators()
            self.__executor.submit(sipri.main, page_url)

        

if __name__=='__main__':

    start = perf_counter()
    logger.info('Scraping start..')
    print()
    


    logger.info(f'total scraping time: {perf_counter() - start}')