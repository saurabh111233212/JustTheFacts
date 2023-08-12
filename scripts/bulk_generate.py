import argparse
from datetime import datetime
import json
import os
import sys

## Sample usage:
##  OPENAI_API_KEY=sk-... python bulk_generate.py --url_file just_facts_urls_v1.jsonl --out_file output.jsonl

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'api'))

from demo.get_facts import get_facts

def load_jsonl(file_name):
    with open(file_name, 'r') as file:
        return [json.loads(line.strip()) for line in file]


def save_jsonl(file_name, data):
    with open(file_name, 'w') as file:
        for d in data:
            file.write(json.dumps(d))
            file.write("\n")


def generate_fact_data(url_file, out_file, add_embeddings=False, skip=0):
    urls = load_jsonl(url_file)[skip:]
    print(f"Processing {len(urls)} urls...")
    all_res = []
    for url in urls:
        print(f"  {datetime.now()} [{len(all_res)}] {url['url']}")
        res = get_facts(url['url'], raw_html=url.get('raw_html'), method="gpt-4", add_embeddings=add_embeddings)
        all_res.append(res)
        save_jsonl(out_file, all_res)
    print(f"{datetime.now()} Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url_file", type=str, required=True, help="JSONL file with URLs")
    parser.add_argument("--out_file", type=str, required=True, help="Output file")
    #parser.add_argument("--prompt", default="V1", help="Which GPT-4 prompt to use")
    parser.add_argument("--add_embeddings", action="store_true", help="Compute embeddings for facts and text")
    parser.add_argument("--skip", type=int, default=0, help="Skip first urls")
    args = parser.parse_args()
    generate_fact_data(args.url_file, args.out_file,
                       add_embeddings=args.add_embeddings,
                       skip=args.skip)
