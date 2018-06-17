# Capital One Software Engineering Summit Summer 2018
Submission for the second round of the Capital One Software Engineering Summit. The challenge can be found [here](https://www.mindsumo.com/contests/podcast-engine).

The final project can be found [here](https://bradleyzhou-capital-one.herokuapp.com/).

## List of Frameworks and APIs used
* [Flask](http://flask.pocoo.org/) for backend
* [Bootstrap](https://getbootstrap.com/) for frontend
* [mygpoclient](http://mygpoclient.readthedocs.io/en/latest/) to access gPodder API
* [Requests](http://docs.python-requests.org/en/master/) to issue GET requests to other HTML pages
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to parse such GET requests
* [thesauropod](http://www.thesauropod.us/) to recommend podcasts
* [Word Cloud](https://github.com/amueller/word_cloud) to generate frequency visualizations

## Overview of each feature
*Note: Clicking each podcast will redirect you to the podcast website. By default, subscriptions and recommendations are based off of a test account I created that is subscribed to the top 25 podcasts. You can login with your own gPodder credentials and see your own subscriptions and recommendations.*
### Required features
#### Search
* Input a search term and displays all results. Implemented using mygpoclient library.

#### Subscriptions
* Displays subscriptions. Can login to view a different user's subscriptions. Implemented using mygpoclient library.

#### Smart Search (Search by Genre)
* Input a genre and displays all podcasts that fall in that genre. Can input a number *n* to view the top *n* results, sorted. If *n* is 0, then all results will be displayed, unsorted. Implemented using mygpoclient library.

#### Smart Sort  
* Assumes that the podcast you should listen to first is the one that would take you the least amount of times to catch up to. First calculated average episode release interval for each subscription and used that data in conjunction with episodes released and an input of how many podcasts one will listen to per day to calculate the time to catch up to each subscription and saves the data in a JSON. Generates a table and then sorts by days to catch up, ascending. Assumes the user is subscribed to top 25 podcasts, but function can be ran again to generate JSON for another user.

### Extra features
#### Login
* Login using gPodder credentials (username, password, and device id) to view your own subscriptions and get personalized recommendations. Upon successful login, subsequent visits to /subscriptions and /recommendations will now use subscription data from the new account until logout or another account is logged in; logging out will clear the cookie. Implemented using Flask sessions.

#### Recommendations
* Randomly selects a podcast in subscriptions and returns three recommendations and how similar they are to the first podcast. There is an API for recommendations called "suggestions," but it seemed to be broken; no suggestions were being given. However, another website (found [here](http://www.thesauropod.us/)) offers suggestions. An API does not exist, so I utilized a series of clever GET requests to extract the recommendations. Implemented using requests and Beautiful Soup.
* *Note: Due to the nature of the implementation, recommendations can take several seconds to load.*

#### Smart Search Extended (Search Within Genre)
* Input a search term and a genre and returns only podcasts that fit both criteria. Implemented using mygpoclient library.

#### Data Visualization
* Aggregated all the words from subscription titles and descriptions and created a frequency analysis of the data. Implemented using an API found [here](https://github.com/amueller/word_cloud). Data is generated from the top 25 podcast list, but can be ran again to generate an analysis for subscriptions or another set of podcasts, too.

## Challenges
* Some image urls defined in the podcast object are broken
* Subscriber counts seem to be perpetually frozen; unlike in the API example, every podcast had the same value for subscribers as subscribers last week. Naturally, this makes writing a function to display the podcasts that have gained the most subscribers in a given period of time relatively redundant in this context.
* Suggestions from API are broken.
* For some reason, a bunch of podcasts just randomly stopped updating around the same time (mid-February 2018). This skews the episode count data slightly, but the differential should be minimal due to its relative recency.
* Certain data, such as episode count, isn't available through the API and as a result, I had to access it some other way, such as through GET requests.
