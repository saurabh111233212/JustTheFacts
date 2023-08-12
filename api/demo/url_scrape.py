import trafilatura
import tldextract

# Code for extracting text and metadata associated with a URL


def get_domain(url):
    tld_parse = tldextract.extract(url)
    tld_domain = tld_parse.domain+'.'+tld_parse.suffix
    return tld_domain


def get_text(url, raw_html):
    raw = raw_html or trafilatura.fetch_url(url)
    text = trafilatura.extract(raw)
    return text


def get_html(url):
    raw = trafilatura.fetch_url(url)
    return raw


def get_text(html):
    text = trafilatura.extract(html)
    if text is None or text.strip() == "":
        text = "N/A"
    return text


def get_date(url, html):
    try:
        metadata = trafilatura.extract_metadata(html, default_url=url).as_dict()
        date = metadata['date']
    except TypeError:
        return ""
    return date


def get_author(url, html):
    try:
        metadata = trafilatura.extract_metadata(html, default_url=url).as_dict()
        author = metadata['author']
    except TypeError:
        return ""
    return author


def url_scrape(url, raw_html=None):
    raw_html = raw_html or get_html(url)
    res = {"domain": get_domain(url),
           "raw_text": get_text(raw_html),
           "raw_html": raw_html,
           "publish_date": get_date(url, raw_html),
           "author": get_author(url, raw_html)}
    return res

