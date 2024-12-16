# adl_german_news
This repository contains my Applied Deep Learning Project that collects data from German speaking news outlets\

(forgive me for the naming, I did not think it through and dont want to change all paths in the code)\
The structure of this repository is as follows:\

the files in crawler and data:\
- create.csv is to turn the scraped json into csv\
- german_fake_news_data.csv is the finished product, the dataset\
- requirements.txt are the dependencies\
the other 2 files are for the scrapy project, that are automatically created\\

- \crawler and data\news_crawler: contains all code for the webcrawlers\
In the folder spiders there are spiders for the certain news outlets.\
Some of them crawl but don't scrape. I think this is due to the robots.txt file, that the crawler obeys.\
As of the beginning of December 2024 all crawlers work on the websites.\

- \crawler and data\data\all\
This is where the html and json the webscrapers produce, are saved.\

- \crawler and data\clean_data\
This is where I saved these raw data files as csv.\
and further as .xlsx (as i read through the news in this format, it is easier for me to just add columns and mark each news article like that)\

- in src\preprocess data:\\

- pipelines_eda: are data analysis for each csv of manually labelled data\
- labelling_approaches: is where you can find what I tried to automatically label the rest of the data\
- fully_labelled_data: is where I saved the manually labelled data file and the automatically labelled one\
- data_ready_for_analysis: is where i stored the csv that are divided by unlabelled/labelled and per news outlet\
- adl_algorithm: is where I tried a simple DL algorithm on my data to show how to work with it\

Now to the data itself:\
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
