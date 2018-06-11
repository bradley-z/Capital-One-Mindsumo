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

def smartsearch_gpo(search_tag, count):
    client = public.PublicClient()

    search_results = client.get_podcasts_of_a_tag(search_tag, count)
    search_results = [ vars(podcast) for podcast in search_results ]

    search_results = sorted(search_results, key=lambda k: k['subscribers'], reverse=True) 
    
    return search_results

# smartsearch_gpo("tech", 10)