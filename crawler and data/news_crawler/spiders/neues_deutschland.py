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


class NeuesDeutschlandSpider(BaseSpider):
    """Spider for neues-deutschland"""

    name = "neues_deutschland"
    rotate_user_agent = True
    allowed_domains = ["www.nd-aktuell.de"]
    start_urls = ["https://www.nd-aktuell.de/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"www\.nd\-aktuell\.de\/artikel\/\d+\.\w.*\.html"),
                deny=(
                    r"www\.nd\-aktuell\.de\/shop\/",
                    r"www\.nd\-aktuell\.de\/leserreisen\/",
                    r"www\.nd\-aktuell\.de\/termine\/",
                    r"www\.nd\-aktuell\.de\/anzeigen\/",
                    r"www\.nd\-aktuell\.de\/jobs\/",
                    r"www\.nd\-aktuell\.de\/abo\/",
                    r"www\.nd\-aktuell\.de\/newsletter\/",
                    r"www\.nd\-aktuell\.de\/nd-ticker\/",
                    r"www\.nd\-aktuell\.de\/redaktion\/",
                    r"www\.nd\-aktuell\.de\/gastautoren\/",
                    r"www\.nd\-aktuell\.de\/kontakt\/",
                    r"www\.nd\-aktuell\.de\/tag\/",
                    r"www\.nd\-aktuell\.de\/nd_extra\/",
                    r"www\.nd\-aktuell\.de\/\w.*\.php",
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
        if "html?" in response.url:
            return

        creation_date = response.xpath('//meta[@name="date"]/@content').get()
        if not creation_date:
            return
        creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        if self.is_out_of_date(creation_date):
            return

        paragraphs = [
            node.xpath("string()").get().strip()
            for node in response.xpath(
                '//h2[preceding-sibling::h1] | //div[@class="Content"]/p'
            )
        ]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join([para for para in paragraphs])

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item["news_outlet"] = "neues_deutschland"
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        item["creation_date"] = creation_date.strftime("%d.%m.%Y")
        item["last_modified"] = creation_date.strftime("%d.%m.%Y")
        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        authors = response.xpath('//meta[@name="author"]/@content').get()
        if "neues deutschland" in authors:
            item["author_person"] = list()
            item["author_organization"] = authors.split(", ")
        elif authors:
            item["author_person"] = authors.split(", ")
            item["author_organization"] = list()
        else:
            item["author_person"] = list()
            item["author_organization"] = list()

        news_keywords = response.xpath('//meta[@name="news_keywords"]/@content').get()
        item["news_keywords"] = news_keywords.split(", ") if news_keywords else list()

        title = response.xpath('//meta[@property="og:title"]/@content').get()
        if "(neues deutschland)" in title:
            title = title.split(" (neues deutschland)")[0]
        description = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()

        body = dict()
        if response.xpath(
            '//h4[not(ancestor::div[@class="Wrap" or @class="ndPLUS-Abowerbung"])] | //h3[not(descendant::*)]'
        ):

            headlines = [
                h.xpath("string()").get().strip()
                for h in response.xpath(
                    '//h4[not(ancestor::div[@class="Wrap" or @class="ndPLUS-Abowerbung"])] | //h3[not(descendant::*)]'
                )
            ]

            text = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//h2[preceding-sibling::h1] | //div[@class="Content"]/p | //h4[not(ancestor::div[@class="Wrap" or @class="ndPLUS-Abowerbung"])] | //h3[not(descendant::*)]'
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

        recommendations = response.xpath(
            '//div[@id="List-Similar-Articles"]//a/@href'
        ).getall()
        if recommendations:
            if len(recommendations) > 5:
                recommendations = recommendations[:5]
            recommendations = [
                "https://www.nd-aktuell.de" + rec for rec in recommendations
            ]
            item["recommendations"] = recommendations
        else:
            item["recommendations"] = list()

        item["response_body"] = response.body

        yield item
