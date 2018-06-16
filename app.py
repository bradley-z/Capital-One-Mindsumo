from flask import Flask, render_template, request
from gpo import subscriptions_gpo, search_gpo, smartsearch_gpo, smartsort_gpo, \
                recommend_gpo, visualize_gpo, search_in_genre_gpo

app = Flask(__name__)
# app.debug = True

username = 'bradleyzhou'
password = '3qPB7~e>VR`/p?&S'
deviceid = 'legacy'

subs = subscriptions_gpo(username, password, deviceid)
searches = []
smartsearches = []
smart_sorted = []
podcast, recommendations = [], []
searches_in_genre = []


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html', searches = searches)

@app.route('/search', methods=['POST', 'GET'])
def search_post():
    if request.method == 'POST':
        text = request.form['text']
        searches = search_gpo(text)
        return render_template('search.html', searches = searches)

@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html', subscriptions = subs)

@app.route('/smartsearch')
def smartsearch():
    return render_template('smartsearch.html', searches = smartsearches)

@app.route('/smartsearch', methods=['POST', 'GET'])
def smartsearch_post():
    if request.method == 'POST':
        genre = request.form['genre']
        count = request.form['count']
        smartsearches = smartsearch_gpo(genre, int(count))
        return render_template('smartsearch.html', searches = smartsearches)

@app.route('/search-in-genre')
def search_in_genre():
    return render_template('search_in_genre.html', searches = searches_in_genre)

@app.route('/search-in-genre', methods = ['POST', 'GET'])
def search_in_genre_post():
    if request.method == 'POST':
        genre = request.form['genre']
        search_term = request.form['term']
        searches_in_genre = search_in_genre_gpo(genre, search_term)
        return render_template('search_in_genre.html', searches = searches_in_genre)


@app.route('/smartsort')
def smartsort():
    return render_template('smartsort.html')

@app.route('/smartsort', methods=['POST', 'GET'])
def smartsort_post():
    if request.method == 'POST':
        count = request.form['count']
        smart_sorted = smartsort_gpo(int(count))
        return render_template('smartsort.html', podcasts = smart_sorted)

@app.route('/recommendations')
def recommend():
    return render_template('recommendations.html', podcasts = podcast, \
                recommendations = recommendations)

@app.route('/recommendations', methods=['POST', 'GET'])
def recommend_post():
    if request.method == 'POST':
        podcast, recommendations = recommend_gpo(subs)
        return render_template('recommendations.html', podcasts = podcast, \
                    recommendations = recommendations)

@app.route('/visualization', methods=['GET'])
def visualization():
    # visualize_gpo(subs)
    return render_template('visualization.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        deviceid = request.form['deviceid']
        global subs
        subs = subscriptions_gpo(username, password, deviceid)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(threaded=True)
