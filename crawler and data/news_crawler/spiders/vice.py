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


class Vice(BaseSpider):
    """Spider for Vice"""

    name = "vice"
    rotate_user_agent = True
    allowed_domains = ["www.vice.com"]
    start_urls = ["https://www.vice.com/de/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"www\.vice\.com\/de\/article\/\w.*"),
                deny=(
                    r"www\.vice\.com\/de\/page\/allgemeine-geschaftsbedingungen",
                    r"legal\.vice\.de\/impressum\-1\.html",
                    r"video\.vice\.com\/de",
                    r"company\.vice\.com\/careers\/",
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

        data_json = response.xpath("//script[@type='application/ld+json']/text()").get()
        if not data_json:
            return
        data = json.loads(data_json)
        if "@graph" not in data:
            return
        data = data["@graph"][1]
        creation_date = data["datePublished"]
        if not creation_date:
            return
        creation_date = datetime.fromisoformat(creation_date.split("T")[0])
        if self.is_out_of_date(creation_date):
            return

        paragraphs = [
            node.xpath("string()").get().strip()
            for node in response.xpath(
                '//div[@class="article__body-components"]//p[not(ancestor::div[@class="body-image__caption"])]'
            )
        ]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join([para for para in paragraphs])

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item["news_outlet"] = "vice"
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        item["creation_date"] = creation_date.strftime("%d.%m.%Y")
        last_modified = data["dateModified"]
        item["last_modified"] = datetime.fromisoformat(
            last_modified.split("T")[0]
        ).strftime("%d.%m.%Y")
        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        authors = data["author"]
        if authors:
            item["author_person"] = (
                [authors["name"]] if authors["@type"] == "Person" else list()
            )
            item["author_organization"] = (
                [authors["name"]] if authors["@type"] == "Organization" else list()
            )
        else:
            item["author_person"] = list()
            item["author_organization"] = list()

        targeting_data = response.xpath(
            '//div[@class="vice-ad__ad"]/@data-targeting'
        ).get()
        if targeting_data is not None:
            targeting_data = json.loads(targeting_data)
            news_keywords = targeting_data["keywords"]
            item["news_keywords"] = news_keywords
        else:
            item["news_keywords"] = list()

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()

        body = dict()
        if response.xpath(
            '//h2[@class="article__body-heading__heading heading2"]/span'
        ):

            headlines = [
                h2.xpath("string()").get().strip()
                for h2 in response.xpath(
                    '//h2[@class="article__body-heading__heading heading2"]/span'
                )
            ]

            text = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//div[@class="article__body-components"]//p[not(ancestor::div[@class="body-image__caption"])] | //h2[@class="article__body-heading__heading heading2"]/span'
                )
            ]

            body[""] = remove_empty_paragraphs(text[: text.index(headlines[0])])

            for i in range(len(headlines) - 1):
                body[headlines[i]] = remove_empty_paragraphs(
                    text[text.index(headlines[i]) + 1 : text.index(headlines[i + 1])]
                )

            body[headlines[-1]] = remove_empty_paragraphs(
                text[text.index(headlines[-1]) + 1 :]
            )

        else:
            # The article has no headlines, just paragraphs
            body[""] = paragraphs

        item["content"] = {"title": title, "description": description, "body": body}

        item["recommendations"] = list()

        item["response_body"] = response.body

        yield item
