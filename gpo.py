from mygpoclient import simple, public

def search(search_term):
    client = public.PublicClient()

    search_results = client.search_podcasts(search_term)
    # for result in search_results:
    #     print result.url
    #     print '-'*50

def subscriptions():
    client = simple.SimpleClient('bradleyzhou','3qPB7~e>VR`/p?&S')
    search_client = public.PublicClient()

    subscription_urls = client.get_subscriptions('legacy')
    subscription_podcast_objects = []
    for url in subscription_urls:
        subscription_podcast_objects.append((search_client.search_podcasts(url))[0])


subscriptions()
