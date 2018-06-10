from mygpoclient import simple, public

def search(search_term):
    client = public.PublicClient()

    search_results = client.search_podcasts(search_term)

def subscriptions():
    client = simple.SimpleClient('bradleyzhou','3qPB7~e>VR`/p?&S')
