# -*- coding: utf-8 -*-

import os
import sys
from news_crawler.spiders import BaseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

sys.path.insert(0, os.path.join(os.getcwd(), "..", ))
from news_crawler.items import NewsCrawlerItem
from news_crawler.utils import remove_empty_paragraphs


class KroneSpider(BaseSpider):
    """Spider for orf.at/stories"""
    #nvm they dont allow :'(
    name = 'zib'
    rotate_user_agent = True
    allowed_domains = ['www.orf.at']
    start_urls = ['https://www.orf.at/']

    # Define rules to follow relevant article URLs
    rules = (
        Rule(
            LinkExtractor(
                allow=(r'www\.orf.at\stories\+'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        """
        Checks article validity. If valid, it parses the content.
        """
        creation_date = response.xpath('//meta[@name="dc.date"]/@content').get()
        if not creation_date:
            return
        creation_date = datetime.fromisoformat(creation_date.split('+')[0])
        if self.is_out_of_date(creation_date):
            return

        paragraphs = [node.xpath('string()').get() for node in
                      response.xpath('//div/p[not(contains(@class, "article__source"))]')]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = ' '.join(paragraphs)

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item['news_outlet'] = 'orf'
        item['provenance'] = response.url
        item['query_keywords'] = self.get_query_keywords()

        item['creation_date'] = creation_date.strftime('%d.%m.%Y')
        last_modified = response.xpath('//meta[@name="last-modified"]/@content').get()
        if last_modified:
            item['last_modified'] = datetime.fromisoformat(last_modified.split('+')[0]).strftime('%d.%m.%Y')
        item['crawl_date'] = datetime.now().strftime('%d.%m.%Y')

        author_person = response.xpath('//span[contains(@class, "author")]/text()').getall()
        item['author_person'] = [author.strip() for author in author_person] if author_person else list()

        news_keywords = response.xpath('//meta[@name="keyword"]/@content').get()
        item['news_keywords'] = news_keywords.split(', ') if news_keywords else list()

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath('//meta[@property="og:description"]/@content').get()

        body = dict()
        if response.xpath('//h2'):

            headlines = [h2.xpath('string()').get().strip() for h2 in response.xpath('//h2')]

            text = [node.xpath('string()').get().strip() for node in
                    response.xpath('//div/p[not(contains(@class, "article__source"))] | //h2')]

            body[''] = remove_empty_paragraphs(text[:text.index(headlines[0])])

            for i in range(len(headlines) - 1):
                body[headlines[i]] = remove_empty_paragraphs(
                    text[text.index(headlines[i]) + 1:text.index(headlines[i + 1])])

            body[headlines[-1]] = remove_empty_paragraphs(text[text.index(headlines[-1]) + 1:])

        else:
            body[''] = paragraphs

        item['content'] = {'title': title, 'description': description, 'body': body}

        item['response_body'] = response.body

        yield item
