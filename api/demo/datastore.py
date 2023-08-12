import json
import numpy as np
import os
import re

# Handling of various data structures, persisting to files, querying
# This code is a mess, should be consolidated into a class

SKIFF_DIR = "/skiff_files/apps/just-the-facts/data"
SCRAPE_FILE = os.path.join(SKIFF_DIR, "scrape.json")
FACT_FILE = os.path.join(SKIFF_DIR, "fact.json")
TOPIC_FILE = os.path.join(SKIFF_DIR, "topic.json")
SOURCE_EMBED_FILE = os.path.join(SKIFF_DIR, "source_embed.npz")
FACT_EMBED_FILE = os.path.join(SKIFF_DIR, "fact_embed.npz")

LAST_LOADED = None   # TODO: Track when files were loaded, to merge when other replica has updated


def load_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


def save_json(file_name, data):
    with open(file_name, 'w') as file:
        return json.dump(data, file)


def load_all_data():
    SCRAPE_DATA = {}
    FACT_DATA = {}
    TOPIC_DATA = {}
    SOURCE_EMBED_DATA = {}
    FACT_EMBED_DATA = {}
    print("Loading cached data...")
    if os.path.exists(SCRAPE_FILE):
        SCRAPE_DATA = load_json(SCRAPE_FILE)
        print(f"Loaded {len(SCRAPE_DATA)} entries from {SCRAPE_FILE}")
    if os.path.exists(FACT_FILE):
        FACT_DATA = load_json(FACT_FILE)
        print(f"Loaded {len(FACT_DATA)} entries from {FACT_FILE}")
    if os.path.exists(TOPIC_FILE):
        TOPIC_DATA = load_json(TOPIC_FILE)
        print(f"Loaded {len(TOPIC_DATA)} entries from {TOPIC_FILE}")
    if os.path.exists(SOURCE_EMBED_FILE):
        SOURCE_EMBED_DATA = dict(np.load(SOURCE_EMBED_FILE))
        print(f"Loaded {len(SOURCE_EMBED_DATA)} entries from {SOURCE_EMBED_FILE}")
    if os.path.exists(FACT_EMBED_FILE):
        FACT_EMBED_DATA = dict(np.load(FACT_EMBED_FILE))
        print(f"Loaded {len(FACT_EMBED_DATA)} entries from {FACT_EMBED_FILE}")
    return SCRAPE_DATA, FACT_DATA, TOPIC_DATA, SOURCE_EMBED_DATA, FACT_EMBED_DATA


def get_patch_file(file_name):
    patch_name =  re.sub("(\\.(json|npz))", "-patch\\1", file_name)
    if patch_name == file_name:
        return "NOMATCH"   # in case something goes wrong
    return patch_name

def save_all_data(SCRAPE_DATA, FACT_DATA, TOPIC_DATA, SOURCE_EMBED_DATA, FACT_EMBED_DATA):
    if not os.path.exists(SKIFF_DIR):
        return
    # Check if patches should be added in
    patch_file = get_patch_file(SCRAPE_FILE)
    if os.path.exists(patch_file):
        patch = load_json(patch_file)
        SCRAPE_DATA.update(patch)
        print(f"Patched {len(patch)} entries from {patch_file}")
        os.remove(patch_file)
    patch_file = get_patch_file(FACT_FILE)
    if os.path.exists(patch_file):
        patch = load_json(patch_file)
        FACT_DATA.update(patch)
        print(f"Patched {len(patch)} entries from {patch_file}")
        os.remove(patch_file)
    patch_file = get_patch_file(SOURCE_EMBED_FILE)
    if os.path.exists(patch_file):
        patch = dict(np.load(patch_file))
        SOURCE_EMBED_DATA.update(patch)
        print(f"Patched {len(patch)} entries from {patch_file}")
        os.remove(patch_file)
    patch_file = get_patch_file(FACT_EMBED_FILE)
    if os.path.exists(patch_file):
        patch = dict(np.load(patch_file))
        FACT_EMBED_DATA.update(patch)
        print(f"Patched {len(patch)} entries from {patch_file}")
        os.remove(patch_file)

    # TODO: Check file dates for out of date
    if SCRAPE_DATA:
        save_json(SCRAPE_FILE, SCRAPE_DATA)
    if FACT_DATA:
        save_json(FACT_FILE, FACT_DATA)
    if TOPIC_DATA:
        save_json(TOPIC_FILE, TOPIC_DATA)
    if FACT_EMBED_DATA:
        np.savez(FACT_EMBED_FILE, **FACT_EMBED_DATA)
    if SOURCE_EMBED_DATA:
        np.savez(SOURCE_EMBED_FILE, **SOURCE_EMBED_DATA)


def save_topic_data(TOPIC_DATA):
    if not os.path.exists(SKIFF_DIR):
        return
    if TOPIC_DATA:
        save_json(TOPIC_FILE, TOPIC_DATA)



