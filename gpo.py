from mygpoclient import simple, public


def search_gpo(search_term):
    client = public.PublicClient()

    search_results = client.search_podcasts(search_term)
    return search_results

def subscriptions_gpo():
    client = simple.SimpleClient('bradleyzhou','3qPB7~e>VR`/p?&S')
    public_client = public.PublicClient()

    subscription_urls = client.get_subscriptions('legacy')
    subscription_podcast_objects = []
    for url in subscription_urls:
        podcast = public_client.get_podcast_data(url)
        # vars converts podcast object into dictionary
        subscription_podcast_objects.append(vars(podcast))
    return subscription_podcast_objects

# subscriptions()
