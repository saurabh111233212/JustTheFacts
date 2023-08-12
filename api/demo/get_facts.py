from datetime import datetime

from .url_scrape import url_scrape
from .generate_facts_gpt import align_facts, generate_facts_gpt, get_embedding
from .datastore import load_all_data, save_all_data, save_topic_data

EXTRACTOR_VERSION = 0


SCRAPE_DATA, FACT_DATA, TOPIC_DATA, SOURCE_EMBED_DATA, FACT_EMBED_DATA = load_all_data()

def make_key(*keys):
    return "--".join(keys)

def get_facts_db(url, method, reset_cache=False):
    if reset_cache:
        return None
    return FACT_DATA.get(make_key(url, method))

def add_facts_db(url, method, facts):
    FACT_DATA[make_key(url, method)] = facts

def get_scrape_db(url, reset_cache=False):
    if reset_cache:
        return None
    return SCRAPE_DATA.get(url)

def add_scrape_db(url, scrape):
    SCRAPE_DATA[url] = scrape



# Extract text URL, run LLM to generate facts and other metadata
def generate_facts(url, raw_html=None, method=None, add_embeddings=True, reset_cache=False):
    db_changed = False
    scrape = get_scrape_db(url, reset_cache)
    if scrape is None:
        scrape = url_scrape(url, raw_html)
        add_scrape_db(url, scrape)
        db_changed = True

    res = get_facts_db(url, method, reset_cache)
    if res is None:
        facts = generate_facts_gpt(url, scrape, method=method)
        res = {
            "url": url,
            "metadata": scrape,
            "extraction_timestamp": str(datetime.now()),
            "extractor_version": EXTRACTOR_VERSION,
            "extractor_method": method,
            "facts": facts
        }

        add_facts_db(url, method, res)
        db_changed = True
    embed_data = {}
    if add_embeddings:
        facts = res['facts']
        embeddings = []
        todo = []
        for fact in facts:
            fact_text = fact['text']
            if reset_cache or make_key(url, fact_text) in FACT_EMBED_DATA:
                embeddings.append(FACT_EMBED_DATA[make_key(url, fact_text)])
            else:
                embeddings.append(None)
                todo.append(fact_text)
        if len(todo) > 0:
            embeddings_new = get_embedding(todo)
            idx_new = 0
            for idx in range(len(facts)):
                if embeddings[idx] is not None:
                    continue
                db_changed = True
                embedding_new = embeddings_new[idx_new]
                embeddings[idx] = embedding_new
                FACT_EMBED_DATA[make_key(url, facts[idx]['text'])] = embedding_new
                idx_new += 1

        embed_data['fact_embeddings'] = embeddings
        if reset_cache or url in SOURCE_EMBED_DATA:
            source_embedding = SOURCE_EMBED_DATA[url]
        else:
            source_embedding = get_embedding(scrape['raw_text'])[0]
            SOURCE_EMBED_DATA[url] = source_embedding
            db_changed = True
        embed_data['embedding'] = source_embedding


    if db_changed:
        save_all_data(SCRAPE_DATA, FACT_DATA, TOPIC_DATA, SOURCE_EMBED_DATA, FACT_EMBED_DATA)

    return res, embed_data


def normalize_url(url_raw):
    # Remove trailing slashes
    url = url_raw.strip().strip('/')
    return url


def get_facts(url_raw, raw_html=None, method=None, add_embeddings=False, reset_cache=False):
    url = normalize_url(url_raw)
    res, embed_data = generate_facts(url, raw_html=raw_html, method=method,
                                     add_embeddings=add_embeddings, reset_cache=reset_cache)
    return res


def compare_facts(urls_raw, topic, method="dummy", match_threshold=0.9, allow_multiple_per_source=True):
    all_docs = []
    all_embeddings = []
    urls = []
    if topic is not None and topic in TOPIC_DATA:
        urls += TOPIC_DATA[topic]['urls']
    if urls_raw is not None:
        urls += urls_raw
    for url_raw in urls:
        url = normalize_url(url_raw)
        doc, embed_data = generate_facts(url, method=method, add_embeddings=True)
        all_docs.append(doc)
        all_embeddings.append(embed_data['fact_embeddings'])
    res = align_facts(all_docs, all_embeddings,
                      match_threshold=match_threshold,
                      allow_multiple_per_source=allow_multiple_per_source)
    return res


def get_topic(topic):
    if topic not in TOPIC_DATA:
        return []
    return TOPIC_DATA[topic]


def update_topic(topic, urls):
    if len(urls) == 0:
        if topic in TOPIC_DATA:
            del TOPIC_DATA[topic]
    else:
        TOPIC_DATA[topic] = {"urls": urls}
    save_topic_data(TOPIC_DATA)


def topics_from_url(url_raw):
    found_topics = []
    url = normalize_url(url_raw)
    for topic in TOPIC_DATA:
        if url in TOPIC_DATA[topic]['urls']:
            found_topics.append(topic)
    return found_topics


def list_topics():
    return TOPIC_DATA