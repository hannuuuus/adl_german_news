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


class WeltSpider(BaseSpider):
    """Spider for Welt"""

    name = "welt"
    rotate_user_agent = True
    allowed_domains = ["www.welt.de"]
    start_urls = ["https://www.welt.de/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"(\/\w+)*\/article\d+\/.*\.html"),
                deny=(
                    r"(\/\w+)*\/plus\d+\/.*\.html",
                    r"(\/english-news)\/article\d+\/.*\.html",
                ),
            ),
            callback="parse_page",
            follow=True,
        ),
    )

    def parse_page(self, response):
        """
        Checks article validity. If valid, it parses it.
        """

        creation_date = response.xpath('//meta[@name="date"]/@content').get()
        if not creation_date:
            return
        creation_date = datetime.fromisoformat(creation_date[:-1])
        if self.is_out_of_date(creation_date):
            return

        paragraphs = [
            node.xpath("string()").get().strip()
            for node in response.xpath(
                '//p[not(@*) and not(ancestor::div/@class="c-page-footer__section")]'
            )
        ]
        paragraphs = remove_empty_paragraphs(paragraphs)
        text = " ".join([para for para in paragraphs])

        if not self.has_min_length(text):
            return

        if not self.has_valid_keywords(text):
            return

        item = NewsCrawlerItem()

        item["news_outlet"] = "welt"
        item["provenance"] = response.url
        item["query_keywords"] = self.get_query_keywords()

        item["creation_date"] = creation_date.strftime("%d.%m.%Y")
        last_modified = response.xpath('//meta[@name="last-modified"]/@content').get()
        item["last_modified"] = datetime.fromisoformat(last_modified[:-1]).strftime(
            "%d.%m.%Y"
        )
        item["crawl_date"] = datetime.now().strftime("%d.%m.%Y")

        authors_linked = response.xpath(
            '//span[@class="c-author__by-line"]/a/text()'
        ).getall()
        authors_unlinked = response.xpath(
            '//span[@class="c-author__by-line"]/text()'
        ).getall()
        if authors_unlinked:

            authors_unlinked = [
                author.strip(" Von WELT/ ") if " Von WELT/ " in author else author
                for author in authors_unlinked
            ]
            authors_unlinked = [author.strip(", ") for author in authors_unlinked]
            authors_unlinked = [
                author
                for author in authors_unlinked
                if author != "Von" and author != ""
            ]

        authors = authors_linked + authors_unlinked

        if authors:

            item["author_person"] = authors
            item["author_organization"] = list()
        else:
            data_json = response.xpath(
                '//script[@type="application/ld+json" and @data-qa="StructuredData"]/text()'
            ).get()
            if data_json:
                data = json.loads(data_json)
                item["author_person"] = list()
                item["author_organization"] = [data["author"]["name"]]
            else:

                item["author_person"] = list()
                item["author_organization"] = list()

        news_keywords = response.xpath('//meta[@name="news_keywords"]/@content').get()
        item["news_keywords"] = news_keywords.split(", ") if news_keywords else list()

        title = (
            response.xpath('//meta[@property="og:title"]/@content')
            .get()
            .split(" - WELT")[0]
        )
        description = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()

        body = dict()
        if response.xpath('//h3[@class="o-headline"]'):

            headlines = [
                h3.xpath("string()").get().strip()
                for h3 in response.xpath('//h3[@class="o-headline"]')
            ]

            text = [
                node.xpath("string()").get().strip()
                for node in response.xpath(
                    '//p[not(@*) and not(ancestor::div/@class="c-page-footer__section")] | //h3[@class="o-headline"]'
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
            '//li//div/h4/a[@name="morelikethis_a_free_"]/@href'
        ).getall()
        if recommendations:
            recommendations = ["welt.de" + rec for rec in recommendations]
            if len(recommendations) > 5:
                recommendations = recommendations[:5]
            item["recommendations"] = recommendations
        else:
            item["recommendations"] = list()

        item["response_body"] = response.body

        yield item
