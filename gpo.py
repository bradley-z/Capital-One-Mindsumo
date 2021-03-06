from mygpoclient import simple, public
from bs4 import BeautifulSoup
from datetime import datetime
from wordcloud import WordCloud
import requests
import json
import urllib
import random


REC_MAX = 3


def search_gpo(search_term):
    client = public.PublicClient()

    search_results = client.search_podcasts(search_term)
    return search_results

def subscriptions_gpo(username='bradleyzhou', password='3qPB7~e>VR`/p?&S', deviceid='legacy'):
    client = simple.SimpleClient(username, password)
    public_client = public.PublicClient()

    try:
        subscription_urls = client.get_subscriptions(deviceid)
    except:
        return None
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
    if count == 0:
        return search_results
    search_results = sorted(search_results, key=lambda k: k['subscribers'], reverse=True)
    search_results = search_results[0:count]

    return search_results

# ----------------------------------------------------------------------------- #
#                       Helper functions for smart sort                         #
# ----------------------------------------------------------------------------- #

# reformats date for easier usage
def normalize_date(date):
    date = date.replace("Jan.", "01")
    date = date.replace("Feb.", "02")
    date = date.replace("March", "03")
    date = date.replace("April", "04")
    date = date.replace("May", "05")
    date = date.replace("June", "06")
    date = date.replace("July", "07")
    date = date.replace("Aug.", "08")
    date = date.replace("Sept.", "09")
    date = date.replace("Oct.", "10")
    date = date.replace("Nov.", "11")
    date = date.replace("Dec.", "12")
    date = date.replace(",", "")
    return date

def days_difference(d1, d2):
    return abs((d1 - d2).days)

# given list of dates, calculate average difference in days
def calculate_average_days(dates):
    count = 0
    total_days = 0
    for i in range(len(dates) - 1):
        total_days += days_difference(dates[i], dates[i + 1])
        count += 1

    return total_days * 1.0 / count

# calculates how long it takes for each podcast to release a new episode
def get_average_release_time_per_subscription():
    subscriptions = subscriptions_gpo()

    averages = []

    for subscription in subscriptions:
        url = subscription["mygpo_link"]
        req = requests.get(url)
        html_text = req.text.encode("ascii", "ignore")
        soup = BeautifulSoup(html_text, "html.parser")

        dates = []
        for line in soup.find_all("span", {"class": "released"}):
            dates.append(normalize_date(line.text.encode("ascii", "ignore")[4:-3]))
        removed_duplicates = list(set(dates))
        removed_duplicates.sort(key = dates.index)
        dates = [] 
        for date in removed_duplicates:
            dates.append(datetime.strptime(date, "%m %d %Y"))

        '''
        disregard the first date for now because in some cases, it's some random post
        that was posted a long time after the podcast ended. if the first date isn't
        out of range, then recalculate the average now considering the first date
        '''
        average = calculate_average_days(dates[1:])

        # refactor in first date
        first_dif = days_difference(dates[0], dates[1])
        if first_dif <= (4 * average):
            total = average * (len(dates) - 1) + first_dif
            average = total / len(dates)
        
        averages.append(average)

    return averages

# takes the information about subs and turns it int JSON format
def create_json():
    client = public.PublicClient()
    subscriptions = subscriptions_gpo()
    titles = [ subscription["title"] for subscription in subscriptions ]
    '''
    episode counts added manually since this data isn't available through api, i
    can't even get it through GET request to the webpage since the webpage is
    only available if i login
    '''
    episode_counts = [ 408, 773, 407, 527, 5049, 501, 2406, 1878, 482, 1147, \
                        2123, 6314, 793, 2507, 3152, 478, 473, 2377, 470, 138, \
                        680, 504, 1511, 351, 1031 ]
    '''
    for some reason, a bunch of podcasts on gPodder abruptly end at around
    mid-february 2018 even though they are still ongoing. therefore, i manually
    searched each podcast to see which ones were still ongoing
    '''
    continuing = [ True for i in range(25) ]
    continuing[0] = False
    continuing[18] = False
    continuing[24] = False
    averages = get_average_release_time_per_subscription()

    dictionaries = []
    keys = ["title", "episode_count", "releases_per_day", "continuing", "days_to_finish"]
    for i in range(len(subscriptions)):
        values = [titles[i], episode_counts[i], 1.0 / averages[i], continuing[i], 0]
        dictionary = dict(zip(keys,values))
        dictionaries.append(dictionary)

    with open("data/subscription_data.json", "w") as fout:
        json.dump(dictionaries, fout)

# ----------------------------------------------------------------------------- #

def smartsort_gpo(podcasts_per_day):
    with open("data/subscription_data.json") as f:
        podcasts = json.load(f)
    for podcast in podcasts:
        '''
        rearrangement of the following equation:
        (episodes per day) * (num days) = (episodes released) + ((releases per day) * (num days))
        if the podcast is completed, then (episodes per day) * (num days) = (episodes released)
        '''
        if podcast["continuing"]:
            days_to_catch_up = podcast["episode_count"] * 1.0 / (podcasts_per_day - podcast["releases_per_day"])
        else:
            days_to_catch_up = podcast["episode_count"] * 1.0 / podcasts_per_day
        podcast["days_to_finish"] = days_to_catch_up
    
    # sort the list by having lowest days to finish first
    podcasts = sorted(podcasts, key=lambda k: k['days_to_finish'])
    
    return podcasts

# ----------------------------------------------------------------------------- #
#                    Helper functions for recommendations                       #
# ----------------------------------------------------------------------------- #

# creates first url
def create_url(podcast):
    base_url = "http://www.thesauropod.us/check_input?podcast_name="
    title = podcast["title"]
    # replace all special characters with encodings
    url = base_url + urllib.quote_plus(title)
    return url

# gets all hrefs on the first webpage to find the link to the second
def get_links(url):
    req = requests.get(url)
    html_text = req.text.encode("ascii", "ignore")
    soup = BeautifulSoup(html_text, "html.parser")

    links = soup.find_all('a', href=True)
    # extract just the links
    links = [ link["href"] for link in links ]
    return links

# searches the title and returns title if it exists, else return None
def get_object(title):
    client = public.PublicClient()

    search_results = client.search_podcasts(title)
    if len(search_results) == 0:
        return None
    else:
        count = 0
        for result in search_results:
            count += 1
            if result.title == title:
                return result
            if count > 25:
                return None
    return None

# extracts recommendation titles and similarities from second url
def get_final_recommendations(podcast, url, subscriptions):
    # passing in list of subscriptions so as not to recommend something subscribed to
    subscription_titles = [ subscription["title"] for subscription in subscriptions ]

    req = requests.get(url)
    html_text = req.text.encode("ascii", "ignore")
    soup = BeautifulSoup(html_text, "html.parser")
    recs = soup.find_all('tr', id=True)

    final_recommendations = []
    final_similarities = []

    rec_count = 0
    while(len(final_recommendations) < REC_MAX):
        rec = recs[rec_count]
        rec_count += 1

        similarity = float(rec.find("input")["value"])
        similarity = round(similarity * 100, 2)

        title_line = rec.find_all('td')[2]
        title = title_line.text

        # don't want to include recommendations already subscribed to
        if title in subscription_titles:
            continue
        else:
            # this is the limiting function, could improve speed by finding different way to do this
            podcast_object = get_object(title)

            # just make sure no repeats or subscriptions, since get_object CAN return something different
            if podcast_object is None or podcast_object.title == podcast["title"] \
                            or podcast_object.title in subscription_titles or \
                                        podcast_object in final_recommendations:
                continue
            else:
                final_recommendations.append(podcast_object)
                final_similarities.append(similarity)

    return final_recommendations, final_similarities


# ---------------------------------------------------------------------------- #

def recommend_gpo(subscriptions):
    links = []
    podcast = None
    # there are 4 hrefs on the page if the podcast exists in the database
    while len(links) != 4:
        podcast_index = random.randint(0, len(subscriptions) - 1)
        podcast = subscriptions[podcast_index]
        url_one = create_url(podcast)
        links = get_links(url_one)
    # the link wanted is always the last href
    url_two = "http://www.thesauropod.us" + links[len(links) - 1]

    final_recs = []
    recs, similarities = get_final_recommendations(podcast, url_two, subscriptions)
    for i in range(len(recs)):
        final_recs.append((recs[i], similarities[i]))

    # returns single podcast as a list to be easier for flask
    return [podcast], final_recs
'''
returns top 100 podcasts in dictionary form
this can be used as an alternate set of data for functionalities such as data visualization, recommendations, or smart sort
'''
def get_top():
    client = public.PublicClient()
    tops = client.get_toplist(100)
    tops = [ vars(podcast) for podcast in tops ]
    return tops

# generates png image of word frequencies of subscriptions
def visualize_gpo(subscriptions):
    descriptions = ""
    for subscription in subscriptions:
        descriptions = descriptions + subscription["title"] + " "
        descriptions = descriptions + subscription["description"] + " "
    wc = WordCloud(width=1200, height=800).generate(descriptions)
    image = wc.to_image()
    image.save("static/frequencies.png", "PNG")

def search_in_genre_gpo(genre, search_term):
    genre_searches = smartsearch_gpo(genre, 0)
    term_searches = search_gpo(search_term)
    term_searches = [ vars(podcast) for podcast in term_searches ]
    matches = []
    for podcast in genre_searches:
        if podcast in term_searches:
            matches.append(podcast)
    return matches
