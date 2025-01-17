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


class CompactOnline(BaseSpider):
    """Spider for Compact Online"""

    name = "compact_online"
    rotate_user_agent = True
    allowed_domains = ["www.compact-online.de"]
    start_urls = ["https://www.compact-online.de/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"www\.compact\-online\.de\/\w.*"),
                deny=(
                    r"abo\.compact\-shop\.de\/",
                    r"www\.compact\-shop\.de\/",
                    r"www\.compact\-online\.de\/kontakt\/",
                    r"www\.compact\-online\.de\/spenden\/",
                    r"www\.compact\-online\.de\/digital\-pass\/",
                    r"www\.compact\-online\.de\/compact\-tv\/",
                    r"www\.compact\-online\.de\/compact\-live\/",
                    r"www\.compact\-online\.de\/newsletter\-anmeldung\/",
                    r"www\.compact\-online\.de\/werben\-in\-compact\/",
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

        creation_date = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).get()
        if not creation_date:
            return
        creation_date = datetime.fromisoformat(creation_date.split("+")[0])
        if self.is_out_of_date(creation_date):
            return

        paragraphs = [
            node.xpath("string()").get().strip()
            for node in response.xpath(
                '//div[contains(@class, "post-content")]/p | //div[contains(@class, "post-content")]/blockquote/p'
            )
        ]
        paragraphs = paragraphs[1:]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join([para for para in paragraphs])

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item["news_outlet"] = "compact_online"
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        item["creation_date"] = creation_date.strftime("%d.%m.%Y")
        last_modified = response.xpath(
            '//meta[@property="article:modified_time"]/@content'
        ).get()
        item["last_modified"] = datetime.fromisoformat(
            last_modified.split("+")[0]
        ).strftime("%d.%m.%Y")
        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        item["author_person"] = list()
        item["author_organization"] = list()
        data_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if data_json:
            data = json.loads(data_json)
            if "name" in data["@graph"][-1]:
                author = data["@graph"][-1]["name"]
                if not "COMPACT" in author:
                    item["author_person"].append([author])
                else:
                    item["author_organization"].append([author])

        item["news_keywords"] = list()

        title = response.xpath('//meta[@property="og:title"]/@content').get().strip()
        title = title.strip(" - COMPACT")
        description = (
            response.xpath('//meta[@property="og:description"]/@content').get().strip()
        )

        body = dict()
        if response.xpath('//div[starts-with(@class, "post-content")]/h4'):

            headlines = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//div[starts-with(@class, "post-content")]/h4'
                )
            ]

            text = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//div[contains(@class, "post-content")]/p | //div[contains(@class, "post-content")]/blockquote/p | //div[starts-with(@class, "post-content")]/h4'
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

        recommendations = list(
            set(
                response.xpath(
                    '//section[@class="related-posts"]//article//a/@href'
                ).getall()
            )
        )
        if recommendations:
            if len(recommendations) > 5:
                recommendations = recommendations[:5]
            item["recommendations"] = recommendations
        else:
            item["recommendations"] = list()

        item["response_body"] = response.body

        yield item
