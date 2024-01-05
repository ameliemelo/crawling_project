import re
import json
import scrapy
import requests
from urllib.parse import quote

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
            if match:
                year = match.group()
                if year=='2004':
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
    
        authors = response.xpath('//h4[contains(text(), "Authors")]/following-sibling::p[1]/i/text()').getall()
        title = response.xpath('//div[@class="container-fluid"]/div[@class="col"]/h4/text()').get()
        #abstract_text =  ' '.join(response.xpath('//h4[contains(text(), "Abstract")]/following-sibling::*/text()').getall())

        #recup sujet
        search_query = 'Accelerated Mini-Batch Stochastic Dual Coordinate Ascent'
        formatted_query = quote(search_query)

        # Maintenant, formatted_query est prêt à être utilisé dans votre URL
        search_url_arxiv = f'https://arxiv.org/search/?query={search_query}&searchtype=title&source=header'

        
        yield response.follow(search_url_arxiv, callback=self.parse_arxiv, meta={"year": year, "title" :title})

        #pdf_link = response.xpath('//div/a[contains(text(), "Paper")]/@href').get()

        #marche pas faudra utiliser grobid surement
        #if pdf_link: info_pdf = self.extract_info(pdf_link)
            

        #yield {
            #"year": year,
            #"authors": authors,
            #"title" : title,
            #"abstract": abstract_text,
            #"info_pdf": info_pdf,

        #}




    def parse_arxiv(self,response):
        arxiv_link = response.xpath('//p[@class="list-title is-inline-block"]/a/@href').getall()
        yield response.follow(arxiv_link, callback=self.parse_subject)
        
        
        

    def parse_subject(self,response):
        subjects = response.css('td.tablecell.subjects span.primary-subject::text').getall()

        yield {"subjects": subjects}



