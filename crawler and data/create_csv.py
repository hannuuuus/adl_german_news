import json
import csv
import os

json_folder_path = r'C:\github\news\news\german-news\data\all\krone\json'


csv_output_file = 'krone.csv'

with open(csv_output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)


    writer.writerow(['news_outlet', 'provenance', 'query_keywords', 'creation_date',
                     'last_modified', 'crawl_date', 'author_person', 'author_organization',
                     'news_keywords', 'content_title', 'content_description', 'content_body'])


    for json_filename in os.listdir(json_folder_path):
        if json_filename.endswith('.json'):
            json_file_path = os.path.join(json_folder_path, json_filename)


            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)


                writer.writerow([
                    data.get("news_outlet", ""),
                    data.get("provenance", ""),
                    ', '.join(data.get("query_keywords", [])),
                    data.get("creation_date", ""),
                    data.get("last_modified", ""),
                    data.get("crawl_date", ""),
                    ', '.join(data.get("author_person", [])),
                    ', '.join(data.get("author_organization", [])),
                    ', '.join(data.get("news_keywords", [])),
                    data.get("content", {}).get("title", ""),
                    data.get("content", {}).get("description", ""),
                    ' '.join(data.get("content", {}).get("body", {}).get("", []))
                ])

print(f"Alle JSON-Dateien wurden erfolgreich in {csv_output_file} gespeichert.")