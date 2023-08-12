import pandas as pd
import trafilatura
from urllib.parse import urlparse
import tldextract
from datetime import date


def get_domain(url):
    urllib_parse = urlparse(url)
    tld_parse = tldextract.extract(url)
    tld_domain = tld_parse.domain+'.'+tld_parse.suffix
    return tld_domain


def get_text(url):
    today = str(date.today())
    raw = trafilatura.fetch_url(url)
    text = trafilatura.extract(raw, output_format='xml', date_extraction_params={
        "extensive_search": True, "max_date": today
    }, url=url)
    return text


def scrape_articles(url_list):
    df = pd.DataFrame(url_list, columns=['url'])
    df['domain'] = df.url.apply(get_domain)
    df['text'] = df.url.progress_apply(get_text)

    return df


def test():
    url_list = """
    https://www.bbc.com/news/world-us-canada-66442370
    https://www.bbc.com/news/world-europe-66448987
    https://www.bbc.com/news/business-66435870
    https://www.bbc.com/news/business-66445496
    https://www.bbc.com/news/technology-66424770
    https://www.bbc.com/news/world-us-canada-66446697
    https://www.bbc.com/news/world-asia-india-66391485
    https://www.bbc.com/sport/football/66448957
    https://www.bbc.com/future/article/20230808-atomic-bomb-spike-carbon-radioactive-body-anthropocene
    https://www.bbc.com/travel/article/20230808-kazakhstan-a-road-trip-through-the-nations-immense-landscapes
    https://www.cnn.com/2023/08/09/politics/dianne-feinstein-hospitalized-after-fall/index.html
    https://www.cnn.com/2023/08/09/entertainment/billy-porter-strike-selling-home/index.html
    https://www.cnn.com/2022/08/10/health/waking-up-tired-reasons-solutions-wellness/index.html
    https://www.cnn.com/2023/08/09/health/biles-mental-health-break-wellness/index.html
    https://www.cnn.com/2023/08/09/politics/ron-desantis-monique-worrell-orlando-attorney/index.html
    https://www.cnn.com/2023/08/09/health/covid-variant-eg5/index.html
    https://www.cnn.com/2023/08/09/us/montgomery-boat-dock-fight-what-we-know/index.html
    https://www.cnn.com/2023/08/09/opinions/child-care-funding-warren-smith/index.html
    https://www.cnn.com/2023/08/07/opinions/womens-world-cup-morocco-nigeria-south-africa-jamaica-aziz/index.html
    https://www.cnn.com/travel/airport-tarmac-phone-rules/index.html
    https://www.nytimes.com/2023/08/09/us/ohio-voters-issue-1-constitution.html
    https://www.nytimes.com/2023/08/08/dining/restaurant-four-day-workweek.html
    https://www.nytimes.com/2023/08/08/well/live/covid-summer-surge.html
    https://www.nytimes.com/2023/08/08/us/politics/trump-indictment-fake-electors-memo.html
    https://www.nytimes.com/2023/08/09/business/china-economy-inflation.html
    https://www.nytimes.com/2023/08/09/arts/design/restitution-nepal-indonesia-democratic-republic-of-congo-cameroon.html
    https://www.nytimes.com/2023/08/09/us/desantis-orlando-prosecutor.html
    https://www.nytimes.com/2023/08/09/world/europe/russia-attack-romania-danube.html
    https://www.nytimes.com/2023/08/09/us/kansas-wheat-harvest-drought.html
    https://www.nytimes.com/2023/08/09/nyregion/kai-cenat-union-square.html
    https://www.washingtonpost.com/education/2023/08/09/florida-schools-drop-ap-psychology-class/
    https://www.washingtonpost.com/lifestyle/2023/08/09/unique-harris-case/
    https://www.washingtonpost.com/politics/2023/08/09/will-more-states-try-make-it-harder-pass-ballot-measures/
    https://www.washingtonpost.com/business/2023/08/08/credit-card-debt-1-trillion-high-earners/
    https://www.washingtonpost.com/travel/2023/08/08/cheaper-airfare-domestic-holiday-flights/
    https://www.washingtonpost.com/history/2023/08/09/mlk-dream-speech-smithsonian-museum/
    https://www.washingtonpost.com/weather/2023/08/09/hawaii-wildfires-maui-lahaina-dora/
    https://www.washingtonpost.com/nation/2023/08/09/mega-millions-jackpot-winner-billion/
    https://www.washingtonpost.com/politics/2023/08/08/vivek-ramaswamy-signs-rnc-pledge/
    https://www.washingtonpost.com/world/2023/08/09/australia-poisonous-mushroom-lunch-police/
    https://www.reuters.com/world/china/chinas-consumer-prices-swing-into-decline-deflation-risks-build-2023-08-09/
    https://www.reuters.com/business/wework-raises-going-concern-doubt-shares-tank-2023-08-08/
    https://www.reuters.com/business/retail-consumer/kellogg-forecasts-annual-sales-up-136-bln-snacks-business-ahead-split-2023-08-09/
    https://www.reuters.com/markets/europe/why-germanys-property-sector-is-dumps-2023-08-09/
    https://www.reuters.com/technology/us-reports-big-interest-52-billion-semiconductor-chips-funding-2023-08-09/
    https://www.reuters.com/markets/deals/amazon-talks-become-anchor-investor-arm-ahead-ipo-sources-2023-08-08/
    https://www.reuters.com/world/us/100-day-strike-hollywood-writers-frustrated-talks-languish-2023-08-09/
    https://www.reuters.com/technology/roblox-misses-quarterly-bookings-estimates-lower-spending-2023-08-09/
    https://www.reuters.com/world/us/lingering-inflation-worries-keep-biden-approval-stagnant-40-reutersipsos-2023-08-09/
    https://www.reuters.com/investigates/special-report/usa-politics-violence/
    """.strip().split('\n')

    return scrape_articles(url_list)

