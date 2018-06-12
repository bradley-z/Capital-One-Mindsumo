from mygpoclient import simple, public
from bs4 import BeautifulSoup
from datetime import datetime
import requests

username = 'bradleyzhou'
password = '3qPB7~e>VR`/p?&S'
deviceid = 'legacy'


def search_gpo(search_term):
    client = public.PublicClient()

    search_results = client.search_podcasts(search_term)
    return search_results

def subscriptions_gpo():
    client = simple.SimpleClient(username, password)
    public_client = public.PublicClient()

    subscription_urls = client.get_subscriptions(deviceid)
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

# ----------------------------------------------------------------------------- #

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

def calculate_average_days(dates):
    count = 0
    total_days = 0
    for i in range(len(dates) - 1):
        total_days += days_difference(dates[i], dates[i + 1])
        count += 1

    return total_days * 1.0 / count

# ----------------------------------------------------------------------------- #

def smartsort_gpo():
    client = public.PublicClient()
    subscriptions = subscriptions_gpo()

    # change this to for subscription in subscriptions
    url = subscriptions[10]["mygpo_link"]
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

    # print title
    # print html_text
    # find all the instances of <span class="released">
    # delete the first one if it's greater > year?
    # remove duplicates
    # also check if current date >= 4x average


# smartsearch_gpo("tech", 10)
smartsort_gpo()