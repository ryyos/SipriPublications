import requests

from pyquery import PyQuery
from time import time, sleep
from datetime import datetime
from icecream import ic

from src.utils.parser import Parser
from src.utils.logs import logger
from src.utils.corrector import vname
from src.utils.fileIO import File


class Publicators:
    def __init__(self) -> None:
        
        self.__parser = Parser()
        self.__file = File()
        
        self.MAIN_DOMAIN = 'www.sipri.org'
        self.MAIN_URL = 'https://www.sipri.org/publications/search'
        self.BASE_URL = 'https://www.sipri.org'
    
    
    def __url_complement(self, pieces_url: str) -> str:
        try:
            return self.BASE_URL+pieces_url
        except Exception:
            return pieces_url
    
    
    def __curl(self):
        pass
    
    
    def __extract_data(self, url_article: str):
        response = requests.get(url_article)
        html = PyQuery(response.text)
        
        content = {
            "description": "",
            "about_author": "",
            "file_name": "",
            "path_data_raw": ""
            }
        
        
        
    
    def main(self):
        response = requests.get(url=self.MAIN_URL)
        ic(response)
        html = PyQuery(response.text)
        
        self.__file.write_str(path='private/try.html', content=response.text)
        
        TABLE = html.find('table.cols-5.sticky-enabled')
        
        
        for row in TABLE.find('tbody tr'):
            results = {
                "crawler_time": str(datetime.now()),
                "crawler_time_epoch": int(time()),
                "domain": self.MAIN_DOMAIN,
                "category": self.__parser.ex(html=html, selector='#sipri-2016-breadcrumbs a').text(),
                "title": self.__parser.ex(html=row, selector='td:first-child').text(),
                "author":
                    [
                        {
                            "name": PyQuery(author).text(),
                            "profile": self.__url_complement(PyQuery(author).attr('href')),
                        } for author in self.__parser.ex(html=row, selector='td:nth-child(2) a')
                    ],
                "research_locations": 
                    [
                        {
                            "area": PyQuery(location).text(),
                            "profile": self.__url_complement(PyQuery(location).attr('href'))
                        } for location in self.__parser.ex(html=row, selector='td:nth-child(4) a')
                    ],
                "publication_date": self.__parser.ex(html=row, selector='td:nth-child(3)').text(),
                "publication_type": self.__parser.ex(html=row, selector='td:last-child a').text(),
                # "contents": self.__extract_data()
            }
            
            ic(results)
            sleep(10)
    
    


