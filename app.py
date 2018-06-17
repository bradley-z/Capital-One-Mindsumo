from flask import Flask, render_template, request, session, redirect, g
from gpo import subscriptions_gpo, search_gpo, smartsearch_gpo, smartsort_gpo, \
                recommend_gpo, visualize_gpo, search_in_genre_gpo
import os
import copy

app = Flask(__name__)
# app.secret_key = os.urandom(24)
app.secret_key = 'x\xa5\xd9\xdc\xd3km\xa9\xa8\xb4`\xa9*\x9b\xb4\xce\x06\xf0J\x1f\xb2\x8d\xe4\x03'
app.debug = True

username = 'bradleyzhou'
password = '3qPB7~e>VR`/p?&S'
deviceid = 'legacy'

subs = subscriptions_gpo(username, password, deviceid)
default_subs = copy.deepcopy(subs)
searches = []
smartsearches = []
smart_sorted = []
podcast, recommendations = [], []
searches_in_genre = []

changed = False

@app.route('/')
def index():
    # global username, password, deviceid, subs
    # username = 'bradleyzhou'
    # password = '3qPB7~e>VR`/p?&S'
    # deviceid = 'legacy'
    # subs = subscriptions_gpo(username, password, deviceid)
    return render_template('home.html')

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'No'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    global username, password, deviceid, subs
    username = 'bradleyzhou'
    password = '3qPB7~e>VR`/p?&S'
    deviceid = 'legacy'

    subs = copy.deepcopy(default_subs) 
    return 'Drop'

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
    if 'user' in session:
        info = session['user'].split(' |delim| ')
        username = info[0]
        password = info[1]
        deviceid = info[2]
        global changed
        if not changed:
            global subs
            subs = subscriptions_gpo(username, password, deviceid)
            changed = True
    else:
        if not changed:
            global subs, default_subs
            subs = copy.deepcopy(default_subs)
            changed = True

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
        session.pop('user', None)
        global username, password, deviceid, subs, changed, default_subs
        un_temp = request.form['username']
        pw_temp = request.form['password']
        id_temp = request.form['deviceid']
        subs_temp = subscriptions_gpo(un_temp, pw_temp, id_temp)
        changed = False
        if subs_temp is not None:
            session['user'] = un_temp + " |delim| " + pw_temp + " |delim| " + id_temp
            subs = copy.deepcopy(subs_temp)
            changed = True
        # add a redirect here
        return redirect('/')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(threaded=False)
