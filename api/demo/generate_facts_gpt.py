import openai
import re
import time

import faiss
import numpy as np

def ask_question_about_article(article_text_raw, question, model="gpt-4"):
    article_text = article_text_raw[:7000]  # Max tokens is 8192 total
    prompt_messages = [
    { "role": "system",
      "content": "You are a fact checker."  # The system description tells GPT what persona it should take on
    },
    { "role": "user",
     "content": f"Here is a newspaper article:\n\n{article_text}\n\n{question}"
    }
    ]

    response = None
    retries = 4
    while response is None and retries > 0:
        retries -= 1
        try:
            response = openai.ChatCompletion.create(model=model, messages=prompt_messages)
        except Exception as e:
            response = None
            print("GPT error. Retrying in 10 seconds...")
            print(e)
            time.sleep(10)
    if response is None:
        return ""
    return response["choices"][0]["message"]["content"]

PROMPT_GET_FACTS_V1 = "Please extract a list of simple, declarative sentences that enumerate just the core facts from the article."

def extract_statements(text):
    """ Extract statements from a numbered list, skipping any lines that don't start with a number"""
    pattern = r'^\s*\d+\.\s*(.*)\s*$'
    lines = text.split('\n')

    statements = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            statements.append(match.group(1))
    return statements


def get_embedding(text_or_list, model="text-embedding-ada-002"):
    texts = text_or_list
    if isinstance(texts, str):
        texts = [texts]
    texts = [text.replace("\n", " ")[:8000] for text in texts]

    full = openai.Embedding.create(input=texts, model=model)
    responses = [x['embedding'] for x in full['data']]
    return responses


def generate_facts_gpt(url, scrape, method=None, add_embeddings=True):
    text = scrape['raw_text']
    if method is None:
        # Dummy function for extracting facts
        fact_strings = [x.strip() for x in text.split(".")[:4]]
    elif method == "gpt-4":
        text = scrape['raw_text']
        response = ask_question_about_article(text, PROMPT_GET_FACTS_V1, "gpt-4")
        fact_strings = extract_statements(response)
    else:
        fact_strings = []

    facts = [{"text": fact} for fact in fact_strings]

    return facts


# Simple greedy algorithm for collecting similar facts across sources based on embedding similarity
# Docs input order matters
def align_facts(docs, fact_embeddings, match_threshold=0.9, allow_multiple_per_source=True):
    all_facts = []
    all_embeddings = []
    todo = []
    for doc, fact_embedding in zip(docs, fact_embeddings):
        url = doc['url']
        facts = doc['facts']
        for fact, embed in zip(facts, fact_embedding):
            fact_text = fact['text']
            all_facts.append((url, fact_text))
            all_embeddings.append(embed)
        assert len(todo) == 0
    all_embeddings = np.array(all_embeddings, dtype=np.float32)
    index = faiss.IndexFlatIP(1536)
    index.add(all_embeddings)
    fact_sets = []
    seen_facts = set()
    match_dist, match_idx = index.search(all_embeddings, len(all_embeddings))
    for idx in range(len(all_facts)):
        (url, fact) = all_facts[idx]
        if (url, fact) in seen_facts:
            continue
        seen_urls = set([url])
        new_set = [(url, fact, 1)]
        seen_facts.add((url, fact))
        for m_d, m_idx in zip(match_dist[idx], match_idx[idx]):
            m_url, m_fact = all_facts[m_idx]
            if (m_url, m_fact) in seen_facts or m_d < match_threshold:
                continue
            if not allow_multiple_per_source and m_url in seen_urls:
                continue
            new_set.append((m_url, m_fact, m_d.item()))
            seen_urls.add(m_url)
            seen_facts.add((m_url, m_fact))
        fact_sets.append(new_set)
    fact_sets = [[{"url":x[0], "fact":x[1], "score":x[2]} for x in fact_set] for fact_set in fact_sets]
    return fact_sets
