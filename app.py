from flask import Flask, render_template, request
from gpo import subscriptions_gpo, search_gpo, smartsearch_gpo, smartsort_gpo, recommend_gpo, visualize_gpo

app = Flask(__name__)
app.debug = True

subs = subscriptions_gpo()
searches = []
smartsearches = []
podcasts = []
podcast, recommendations = [], []

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
        searches_post = smartsearch_gpo(genre, int(count))
        return render_template('smartsearch.html', searches = searches_post)

@app.route('/smartsort')
def smartsort():
    return render_template('smartsort.html')

@app.route('/smartsort', methods=['POST', 'GET'])
def smartsort_post():
    if request.method == 'POST':
        count = request.form['count']
        podcasts = smartsort_gpo(int(count))
        return render_template('smartsort.html', podcasts = podcasts)

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
    # return 

    # return render_template('visualization.html', word_freqs=freqs, max_freq=max_freq)

if __name__ == '__main__':
    app.run(threaded=True)
