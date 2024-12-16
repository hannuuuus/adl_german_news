# adl_german_news
This repository contains my Applied Deep Learning Project that collects data from German speaking news outlets
Please find detailed information in the file assignment2.pdf.

The structure of this repository is as follows:

the files in crawler and data:
- create.csv is to turn the scraped json into csv
- german_fake_news_data.csv is the finished product, the dataset
- requirements.txt are the dependencies\
the other 2 files are for the scrapy project, that are automatically created

-  crawler and data\data\scrapy_raw_data\
Contains the raw json and html files that the scrapers produce. Divided by news outlet.
As of the beginning of December 2024 all crawlers work on the websites.

- \crawler and data\data\scrapy_csv_xlsx_data\
The csv and xlsx of these json files. I labelled these files this way manually.

- \crawler and data\data\data_ready_for_analysis\
The csv divided on whether they are labelled and news outlet. This structure made it easy to load them into the data analysis pipelines.


- \crawler and data\data\fully_labelled_data\
The two final files where all data is labelled (manually and not).

in src\preprocess data:

- pipelines_eda: are data analysis for each csv of manually labelled data
- labelling_approaches: is where you can find what I tried to automatically label the rest of the data. The final approach I used is multiclass_labelling.py
- adl_algorithm: is where I tried a simple DL algorithm on my data to show how to work with it

Now to the data itself:
news_outlet: A string of the name of the news outlet.\
provenance: a url of the article\
query_keywords: keywords from a list i created that the crawler would scrape the page, so these were actually found in the article and triggered the scraping\
creation_date: of the article\
last_modified: date of the article\
crawl_date: crawl date\
author_person: author\
author_organization: authr orgnisation\
news_keywords: if given, the article itself would sometimes contain this section, so these keywords are from the author\
title: title\
description: if given, the short version of the article, that is usually found in the first paragraph\
body: the actual article
fake news: label of either 0/1
extreme bias: label of either 0/1
clickbait: label of either 0/1
credible: label of either 0/1
body_len: length of the body
