import requests

api = "http://just-the-facts.apps.allenai.org/api/"


def change_topic_name(old_topic, new_topic):
    r = requests.get(api + "get-topic", params={'topic': old_topic}).json()
    urls = r['urls']
    print(urls)
    urls_csv = ",".join(urls)

    print("Adding new topic:", new_topic)
    requests.get(api + "update-topic", params={'topic': new_topic, 'urls': urls_csv})

    r_new = requests.get(api + "get-topic", params={'topic': new_topic}).json()
    print(r_new)
    if r_new['urls'] == urls:
        # erasing old topic
        print("Erasing old topic:", old_topic)
        requests.get(api + "update-topic", params={'topic': old_topic, 'urls': ''})


def add_topic(topic, urls):
    urls_csv = ",".join(urls)
    print("Adding new topic:", topic)
    requests.get(api + "update-topic", params={'topic': topic, 'urls': urls_csv})


if __name__ == "__main__":
    #change_topic_name("Ohio Vote on Abortion Rights", "Ohio Vote on Constitutional Amendment")
    #change_topic_name("LK-99 superconductor", "LK-99 Superconductor")
    #change_topic_name("Hawaii wild fires", "Hawaii Wild Fires")
    #change_topic_name("DeSantis suspends prosecutor", "DeSantis Suspends Prosecutor")
    #change_topic_name("Trump Search Warrant", "Trump Twitter Search Warrant", )
    #change_topic_name("Hawaii Wild Fires", "Hawaii Wild Fires - Aug 9, 2023")
    change_topic_name("Biden's Loan Forgiveness", "Biden's Student Loan Forgiveness")
    # Hawaii Wild Fires Aug 11
    hawaii_wild_fires_urls = ["https://www.nbcnews.com/news/us-news/live-blog/maui-fires-live-updates-lahaina-rcna99396",
                              "https://www.theguardian.com/us-news/live/2023/aug/11/hawaii-wildfires-maui-lahainia-search-survivors-evacuation",
                              "https://abcnews.go.com/US/maui-evacuees-after-losing-homes-hawaii-wildfires/story?id=102195773",
                              "https://www.bbc.com/news/live/world-66461158"]
    #add_topic("Hawaii Wild Fires - Aug 11, 2023", hawaii_wild_fires_urls)


    assassination_urls = ["https://www.npr.org/2023/08/11/1193402600/ecuador-assassination-villavicencio-presidential-candidate-elections",
                          "https://www.cbsnews.com/news/ecuador-assassination-presidential-candidate-fernando-villavicencio-quito/",
                          "https://www.cnn.com/videos/world/2023/08/11/exp-ecuador-state-of-emergency.cnn",
                          "https://www.reuters.com/world/americas/ecuadorean-candidate-villavicencio-killed-campaign-event-local-media-2023-08-10/"]
    #add_topic("Assassination of Fernando Villavicencio", assassination_urls)