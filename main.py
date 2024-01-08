import requests
import os

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
                all_page_urls.append(url_page)
            except Exception:
                break

            logger.info(f'Fetch url page: {page}')
            page+=1

            response = requests.get(url_page)


        for page_url in tqdm(all_page_urls,ascii=True, 
                                            smoothing=0.1,
                                            total=len(all_page_urls)):
            sipri = Publicators()
            self.__executor.submit(sipri.main, page_url)
            
        self.__executor.shutdown(wait=True)

        

if __name__=='__main__':

    if not os.path.exists('data'):
        os.mkdir('data')
        os.mkdir('data/json')
        os.mkdir('data/pdf')

    start = perf_counter()
    logger.info('Scraping start..')

    main = Main()
    main.execute()
    
    logger.info(f'total scraping time: {perf_counter() - start}')