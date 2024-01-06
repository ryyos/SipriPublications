from src import Publicators
from src import logger

if __name__=='__main__':

    logger.info('Scraping start..')
    print()
    
    sipri = Publicators()
    sipri.main()