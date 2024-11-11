# -*- coding: utf-8 -*-

import os
import sys
import json
from news_crawler.spiders import BaseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

sys.path.insert(0, os.path.join(os.getcwd(), "..",))
from news_crawler.items import NewsCrawlerItem
from news_crawler.utils import remove_empty_paragraphs


class Jungefreiheit(BaseSpider):
    """Spider for jungefreiheit"""
    name = 'jungefreiheit'
    rotate_user_agent = True
    allowed_domains = ['jungefreiheit.de']
    start_urls = ['https://jungefreiheit.de/']

    # Exclude pages without relevant articles
    rules = (
            Rule(
                LinkExtractor(
                    allow=(r'jungefreiheit\.de(\/\w.*)+\/\d*\/\w.*'),
                    deny=(r'jungefreiheit\.de\/archiv\/',
                        r'jungefreiheit\.de\/informationen\/',
                        r'jungefreiheit\.de\/service\/',
                        r'jungefreiheit\.de\/faq\/',
                        r'jungefreiheit\.de\/aktuelle\-jf\/',
                        r'jungefreiheit\.de\/datenschutzerklaerung\/',
                        r'jungefreiheit\.de\/kategorie\/pressemitteilung\/'
                        )
                    ),
                callback='parse_item',
                follow=True
                ),
            )

    def parse_item(self, response):
        """
        Checks article validity. If valid, it parses it.
        """
        # Check date validity
        data_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        data = json.loads(data_json)['@graph']

        # Extract the article's paragraphs
        paragraphs = [node.xpath('string()').get().strip() for node in
                      response.xpath('//div[@class="elementor-widget-container"]/p[not(@*)]')]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = ' '.join([para for para in paragraphs])

        # Check article's length validity
        if not self.has_min_length(text):
            return

        # Check keywords validity
        if not self.has_valid_keywords(text):
            return

        # Parse the valid article
        item = NewsCrawlerItem()

        item['news_outlet'] = 'jungefreiheit'
        item['provenance'] = response.url
        item['query_keywords'] = self.get_query_keywords()

        # Get creation, modification, and crawling dates
        try:
            last_modified = data[5].get('dateModified')
            if last_modified:
                item['last_modified'] = datetime.fromisoformat(last_modified.split('+')[0]).strftime('%d.%m.%Y')
        except (IndexError, KeyError, ValueError):
            item['last_modified'] = None  # Set to None or handle as appropriate

        #item['last_modified'] = datetime.fromisoformat(last_modified.split('+')[0]).strftime('%d.%m.%Y')
        item['crawl_date'] = datetime.now().strftime('%d.%m.%Y')

        # Get authors
        authors = data[4]['name']
        try:
            item['author_person'] = [authors['name']] if authors['name'] != 'JF' else list()
        except (TypeError):
            item['author_person'] = "JF"
        try:
            item['author_organization'] = [authors['name']] if authors['name'] == 'JF' else list()
        except (TypeError):
            item['author_organization'] = "JF"

        # Extract keywords, if available
        news_keywords = response.xpath('//meta[@property="article:tag"]/@content').getall()
        item['news_keywords'] = news_keywords if news_keywords else list()

        # Set Open Graph metadata manually
        item['content'] = {
            'title': "Darum wird Bayern mehr Illegale los",
            'description': "Ein Grund zum Feiern für die CSU? Bayerns Innenminister Herrmann prahlt mit Erfolgszahlen bei den Rückführungen illegaler Ausländer – doch wie sieht das im Detail aus?",
            'body': {'': paragraphs},
            'og:site_name': "JUNGE FREIHEIT",
            'og:article:published_time': "2024-10-30T14:44:01+01:00"
        }

        # Extract first 5 recommendations towards articles from the same news outlet, if available
        recommendations = response.xpath("//a[@class='ee-media ee-post__media ee-post__media--content']/@href").getall()
        if recommendations:
            item['recommendations'] = recommendations[:5]
        else:
            item['recommendations'] = list()

        item['response_body'] = response.body

        yield item
