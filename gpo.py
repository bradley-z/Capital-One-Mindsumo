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

    # format search tag better
    search_tag = search_tag.replace(" & ", "-")
    search_tag = search_tag.replace("&", "-")
    search_tag = search_tag.replace(" ", "-")

    '''
    get_podcasts_of_a_tag doens't really retrieve podcasts sorted by subscribers.
    this retrieves the max number of podcasts in the search, converts the objects
    to dictionaries, sorts them, then only takes the first count podcasts and
    returns them
    '''
    search_results = client.get_podcasts_of_a_tag(search_tag, 100)
    search_results = [ vars(podcast) for podcast in search_results ]
    search_results = sorted(search_results, key=lambda k: k['subscribers'], reverse=True)
    search_results = search_results[0:count]

    return search_results

smartsearch_gpo("tech", 10)