# -*- coding: utf-8 -*-

import os
import sys
import json
from news_crawler.spiders import BaseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

sys.path.insert(
    0,
    os.path.join(
        os.getcwd(),
        "..",
    ),
)
from news_crawler.items import NewsCrawlerItem
from news_crawler.utils import remove_empty_paragraphs


class Jungefreiheit(BaseSpider):
    """Spider for jungefreiheit"""

    name = "jungefreiheit"
    rotate_user_agent = True
    allowed_domains = ["jungefreiheit.de"]
    start_urls = ["https://jungefreiheit.de/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"jungefreiheit\.de(\/\w.*)+\/\d*\/\w.*"),
                deny=(
                    r"jungefreiheit\.de\/archiv\/",
                    r"jungefreiheit\.de\/informationen\/",
                    r"jungefreiheit\.de\/service\/",
                    r"jungefreiheit\.de\/faq\/",
                    r"jungefreiheit\.de\/aktuelle\-jf\/",
                    r"jungefreiheit\.de\/datenschutzerklaerung\/",
                    r"jungefreiheit\.de\/kategorie\/pressemitteilung\/",
                ),
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        """
        Checks article validity. If valid, it parses it.
        """
        try:
            data_json = response.xpath(
                '//script[@type="application/ld+json"]/text()'
            ).get()
            data = json.loads(data_json).get("@graph", [])
        except (TypeError, ValueError):
            data = []

        paragraphs = [
            node.xpath("string()").get().strip()
            for node in response.xpath(
                '//div[@class="elementor-widget-container"]/p[not(@*)]'
            )
        ]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join(paragraphs)

        if not self.has_min_length(text) or not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()
        item["news_outlet"] = self.name
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        try:
            last_modified = next(
                (
                    entry.get("dateModified")
                    for entry in data
                    if "dateModified" in entry
                ),
                None,
            )
            if last_modified:
                item["last_modified"] = datetime.fromisoformat(
                    last_modified.split("+")[0]
                ).strftime("%d.%m.%Y")
            else:
                item["last_modified"] = None
        except ValueError:
            item["last_modified"] = None

        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        try:
            authors = next(
                (entry.get("name") for entry in data if "name" in entry), None
            )
            if authors == "JF":
                item["author_person"] = []
                item["author_organization"] = ["JF"]
            else:
                item["author_person"] = [authors] if authors else []
                item["author_organization"] = []
        except TypeError:
            item["author_person"] = []
            item["author_organization"] = []

        item["news_keywords"] = (
            response.xpath('//meta[@property="article:tag"]/@content').getall() or []
        )

        item["content"] = {
            "title": response.xpath("//title/text()").get(),
            "description": response.xpath('//meta[@name="description"]/@content').get(),
            "body": {"": paragraphs},
            "og:site_name": response.xpath(
                '//meta[@property="og:site_name"]/@content'
            ).get(),
            "og:article:published_time": response.xpath(
                '//meta[@property="article:published_time"]/@content'
            ).get(),
        }

        recommendations = response.xpath(
            "//a[@class='ee-media ee-post__media ee-post__media--content']/@href"
        ).getall()
        item["recommendations"] = recommendations[:5] if recommendations else []

        item["response_body"] = response.body

        yield item
