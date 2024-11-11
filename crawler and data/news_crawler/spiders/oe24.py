# -*- coding: utf-8 -*-

import os
import sys
import json
from news_crawler.spiders import BaseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

sys.path.insert(0, os.path.join(os.getcwd(), "..", ))
from news_crawler.items import NewsCrawlerItem
from news_crawler.utils import remove_empty_paragraphs


class Oe24Spider(BaseSpider):
    """Spider for oe24.at"""
    name = 'oe24'
    rotate_user_agent = True
    allowed_domains = ['oe24.at']
    start_urls = ['https://www.oe24.at/']

    # Define rules for extracting article links and excluding irrelevant ones
    rules = (
        Rule(
            LinkExtractor(
                allow=(r'oe24\.at\/\w+\/\w.*\.html$', r'oe24\.at/.*\.html$'),
                deny=(r'oe24\.at\/video\/\w.*\.html$',
                      r'oe24\.at\/wetter\/',
                      r'oe24\.at\/hilfe\/',
                      r'oe24\.at\/sitemap\/',
                      r'oe24\.at\/impressum\/')
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        """
        Checks article validity and extracts metadata if valid.
        """
        item = NewsCrawlerItem()

        # Extract metadata from Open Graph tags
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath('//meta[@property="og:description"]/@content').get()
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        self.logger.info(f"Parsing article: {response.url}")

        # Verify the required metadata is available
        if not title or not description or not url:
            return

        # Get publication date if available in metadata
        data_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if data_json:
            try:
                data = json.loads(data_json)
                creation_date_str = data.get('datePublished')
                if creation_date_str:
                    creation_date = self.parse_iso_date(creation_date_str)
                    if self.is_out_of_date(creation_date):
                        return
                    item['creation_date'] = creation_date.strftime('%d.%m.%Y')
                else:
                    return  # Skip if no valid date is available
            except (json.JSONDecodeError, ValueError):
                self.logger.error("Error parsing JSON data.")
                return

        # Assign other metadata fields to the item
        item['title'] = title
        item['description'] = description
        item['url'] = url
        item['crawl_date'] = datetime.now().strftime('%d.%m.%Y')

        yield item

    def parse_iso_date(self, date_str):
        """
        Parse ISO 8601 formatted date, stripping unsupported timezone notations like 'Z'.
        """
        if date_str.endswith('Z'):
            date_str = date_str[:-1]
        try:
            # Try parsing with datetime.fromisoformat
            return datetime.fromisoformat(date_str)
        except ValueError:
            # If parsing fails, raise the error to be handled in parse_item
            raise ValueError(f"Invalid date format for '{date_str}'")
