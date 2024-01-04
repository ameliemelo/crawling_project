import re
import json
import scrapy
import requests


class NeuroSpider(scrapy.Spider):
    name = 'NeuroIPS'


    def start_requests(self):
        urls = [
            'https://papers.nips.cc/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        years = []
        for href in response.xpath('//div[@class="col-sm"]//a'):
            year_text = href.xpath('text()').get()
            match = re.search(r'\b\d{4}\b', year_text)  #trouver année
            print("match is",match)
            if match:
                year = match.group()
                link = href.xpath('@href').get() #recupérer le lien avec articles de l'année
                years.append({"year": year, "link": link})

        #pour aller voir les pages de chaque année
        for year_info in years:
            yield response.follow(year_info["link"], callback=self.parse_year, meta={"year": year_info["year"]})



    def parse_year(self, response):
        year = response.meta["year"] # Recupérer année
        
        # Récuperer lien article
        article_links = response.css('ul.paper-list a::attr(href)').getall()

        for article_link in article_links:
            yield response.follow(article_link, callback=self.parse_article, meta={"year": year})

    def parse_article(self, response):
        year = response.meta["year"]
        
        # Extraire les auteurs, titre, abstract
        # Ca fait pas années par années et j'arrive pas a trouver de solution 
        authors = response.xpath('//h4[contains(text(), "Authors")]/following-sibling::p[1]/i/text()').getall()
        title = response.xpath('//div[@class="container-fluid"]/div[@class="col"]/h4/text()').get()
        abstract_text =  ' '.join(response.xpath('//h4[contains(text(), "Abstract")]/following-sibling::*/text()').getall())

        pdf_link = response.xpath('//div/a[contains(text(), "Paper")]/@href').get()

        #marche pas faudra utiliser grobid surement
        #if pdf_link: info_pdf = self.extract_info(pdf_link)
            

        yield {
            "year": year,
            "authors": authors,
            "title" : title,
            "abstract": abstract_text,
            #"info_pdf": info_pdf,

        }





    def extract_info(self, pdf_link):
        full_pdf_url = f'https://papers.nips.cc{pdf_link}'
        grobid_url = 'http://localhost:8070/api/processFulltextDocument'

        # Requête à Grobid avec le contenu du PDF
        files = {'input': (full_pdf_url, requests.get(full_pdf_url).content)}
        params = {'consolidateHeader': 'true', 'consolidateCitations': 'true'}

        response = requests.post(grobid_url, files=files, params=params)
        
        # Analyser la réponse de Grobid (XML ou JSON)
        # Vous pouvez ajouter ici la logique pour extraire les informations spécifiques dont vous avez besoin
        grobid_response = response.text

        return grobid_response
