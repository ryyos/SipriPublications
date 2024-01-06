from time import perf_counter
from src import Publicators
from src import logger

if __name__=='__main__':

    start = perf_counter()
    logger.info('Scraping start..')
    print()
    
    sipri = Publicators()
    sipri.main()

    logger.info(f'total scraping time: {perf_counter() - start}')