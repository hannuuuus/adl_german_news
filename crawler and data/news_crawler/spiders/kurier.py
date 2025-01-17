# -*- coding: utf-8 -*-

import os
import sys
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
from datetime import datetime, timezone
from dateutil.parser import isoparse


class KurierSpider(BaseSpider):
    """Spider for kurier.at"""

    name = "kurier"
    rotate_user_agent = True
    allowed_domains = ["kurier.at"]
    start_urls = ["https://kurier.at/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r"kurier\.at\/politik\/.*",
                    r"kurier\.at\/wirtschaft\/.*",
                    r"kurier\.at\/kultur\/.*",
                    r"kurier\.at\/chronik\/.*",
                ),
                deny=(
                    r"kurier\.at\/search",
                    r"kurier\.at\/themen\/",
                    r"kurier\.at\/preview\/",
                ),
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        """
        Checks article validity. If valid, it parses the content.
        """

        creation_date = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        if creation_date:
            try:
                creation_date = creation_date.replace("Z", "+00:00")
                creation_date = datetime.fromisoformat(creation_date)
            except ValueError:
                creation_date = "nan"
        else:
            creation_date = "nan"

        paragraphs = [
            node.xpath("string()").get()
            for node in response.xpath('//section[contains(@class, "article-main")]//p')
        ]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join(paragraphs)

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item["news_outlet"] = "kurier"
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        if creation_date != "nan":
            item["creation_date"] = creation_date.strftime("%d.%m.%Y")
        else:
            item["creation_date"] = "nan"
        last_modified = response.xpath(
            '//meta[@property="article:modified_time"]/@content'
        ).get()
        if last_modified:
            try:
                item["last_modified"] = datetime.fromisoformat(
                    last_modified.split("+")[0]
                ).strftime("%d.%m.%Y")
            except ValueError:
                item["last_modified"] = "nan"
        else:
            item["last_modified"] = "nan"

        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        author_person = response.xpath(
            '//span[contains(@class, "author")]/text()'
        ).getall()
        item["author_person"] = (
            [author.strip() for author in author_person] if author_person else list()
        )

        news_keywords = response.xpath('//meta[@name="news_keywords"]/@content').get()
        item["news_keywords"] = news_keywords.split(", ") if news_keywords else list()

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()  # Extract description

        # Body as dictionary: key = headline (if available, otherwise empty string), values = list of corresponding paragraphs
        body = dict()
        if response.xpath("//h2"):

            headlines = [
                h2.xpath("string()").get().strip() for h2 in response.xpath("//h2")
            ]

            text = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//section[contains(@class, "article-main")]//p | //h2'
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
            body[""] = paragraphs

        item["content"] = {"title": title, "description": description, "body": body}

        item["response_body"] = response.body

        yield item
