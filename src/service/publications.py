import requests

from pyquery import PyQuery
from time import time
from datetime import datetime
from icecream import ic
from urllib import request

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
    
    
    def __curl(self, path: str,url: str):
        if url: request.urlretrieve(url, path)
    
    
    def __extract_data(self, url_article: str) -> dict:
        response = requests.get(url_article)
        html = PyQuery(response.text)
        
        BODY = html.find(selector='#sipri-2016-content')
        PDF = html.find(selector='#sipri-2016-content div.field-item.button_style a')

        path = f'data/pdf/{str(PDF.attr("href")).split("/")[-1]}'
        
        self.__curl(
            path=path, 
            url=self.__url_complement(pieces_url=PDF.attr('href')))
        
        content = {
            "url_content": url_article,
            "description": self.__parser.ex(html=BODY, selector='div.body.field--label-hidden  p').text(),
            "about_author": [
                {
                    "name": self.__parser.ex(html=author, selector='div.views-field.views-field-body a').text(),
                    "profile": self.__url_complement(self.__parser.ex(html=author, selector='div.views-field.views-field-body  a').attr('href')),
                    "avatar": self.__url_complement(self.__parser.ex(html=author, selector='div.views-field.views-field-field-image img').attr('src')),
                    "author_desc": self.__parser.ex(html=author, selector='div.field-content').text()
                } for author in BODY.find(selector='div.js-view-dom-id-32a230c39aa79ab582716775f67933cf52de0ada662b0e0866101d175816f8d6 > div')
            ],
            "file_name": PDF.attr("href").split("/")[-1] if PDF else None,
            "path_data_raw": path if "None" not in path else None
            }
        
        return content
        
    
    def main(self):
        page = 1
        response = requests.get(url=self.MAIN_URL)
        while True:
            html = PyQuery(response.text)

            self.__file.write_str(path='private/try.html', content=response.text)

            TABLE = html.find('table.cols-5.sticky-enabled')


            for row in TABLE.find('tbody tr'):
                results = {
                    "crawler_time": str(datetime.now()),
                    "crawler_time_epoch": int(time()),
                    "domain": self.MAIN_DOMAIN,
                    "link": self.MAIN_URL+html.find('#sipri-2016-content a[title="Go to next page"]').attr('href'),
                    "tags": self.MAIN_DOMAIN,
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
                    "contents": self.__extract_data(url_article=self.__url_complement(self.__parser.ex(html=row, selector='td:first-child a').attr('href')))
                }

                self.__file.write_json(path=f'data/json/{vname(results["title"])}.json', content=results)

                logger.info(f'page: {page}')
                logger.info(f'status: {response.status_code}')
                logger.info(f'link: {results["link"]}')
                logger.info(f'title: {results["title"]}')
                logger.info(f'pdf: {results["contents"]["file_name"]}')
                page+=1
                print()


            try:
                response = requests.get(self.MAIN_URL+html.find('#sipri-2016-content a[title="Go to next page"]').attr('href'))
            except Exception:
                logger.warning('content is out!')
                break


    


