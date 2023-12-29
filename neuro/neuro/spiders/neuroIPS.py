import re
import scrapy
import requests
from bs4 import BeautifulSoup



class NeuroSpider(scrapy.Spider):
    name = 'NeuroIPS'


    def start_requests(self):
        urls = [
            'https://papers.nips.cc/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            #met pas le texte en entier s'arrete a la ligne
            "title": response.xpath('//div[@class="card-body"]/p[@class="card-text"]/text()').getall(),
        }
        #pour aller voir les pages de chaque année
        #soucis pas dans l'ordre chronologique
        for href in response.xpath('//div[@class="col-sm"]//a/@href').getall():
            yield response.follow(href, callback=self.parse_year)


    def parse_year(self, response):
        yield {
            "year": response.xpath('//div[@class="col"]/h4/text()').get(),     
        }
        #pour aller recup chaque article
        #socuis j'ai l'impression que ca va pas chercher tous les articles avant d'aller sur une autre année
        for href in response.css('ul.paper-list a').css('::attr(href)').getall() :
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        yield {
            #recup auteur des articles
            "author": response.xpath('//h4[contains(text(), "Authors")]/following-sibling::p[1]/i/text()').get(),     
        }