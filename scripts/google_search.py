import argparse
from datetime import datetime
import json
import os
import sys
from datetime import datetime, timedelta
from googlesearch import search
import time

website_list = 'nytimes.com reuters.com apnews.com'.split()
print(website_list)

topic_list_old = [
    'Ron Desantis Florida prosecutor',
    'Iran prisoner swap deal',
    'Ecuador presidential candidate',
    'Ohio election',
    'Kim Jong Un North Korea',
    'NOAA hurricane season',
    'US Inflation consumer price index',
    'Russia Explosion',
    'Wild Mushrooms',
    'OpenAI GPTBot'
]

topic_list = ['Hawaii Wild Fires']


def load_jsonl(file_name):
    with open(file_name, 'r') as file:
        return [json.loads(line.strip()) for line in file]


def save_jsonl(file_name, data):
    with open(file_name, 'w') as file:
        for d in data:
            file.write(json.dumps(d))
            file.write("\n")


def google_search(out_file):
    # Get today's date
    today = datetime.today()

    # Calculate the date from one week ago
    one_week_ago = today - timedelta(days=1)

    # Format the dates
    start_date = one_week_ago.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    url_topic_list = []
    for topic in topic_list:
        for website in website_list:
            query = f"{topic} site:{website}"
            print(f"Searching for '{query}'")
            try:
                urls = search(f'{topic} site:{website} after:{start_date} before:{end_date}', stop=10)
                for url in urls:
                    url_topic_list.append({'url': url, 'topic': topic})
                time.sleep(1)
            except Exception as e:
                print(e)
                continue

    save_jsonl(out_file, url_topic_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_file", type=str, default='just_facts_urls_recent_v2.jsonl', help="Output file")
    args = parser.parse_args()
    google_search(args.out_file)

