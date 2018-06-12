from flask import Flask, render_template, request
from gpo import subscriptions_gpo, search_gpo, smartsearch_gpo

app = Flask(__name__)
app.debug = True

subs = subscriptions_gpo()
searches = []
smartsearches = []

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
        text = request.form['genre']
        count = request.form['count']
        searches = smartsearch_gpo(text, int(count))
        return render_template('smartsearch.html', searches = searches)

@app.route('/smartsort')
def smartsort():
    return render_template('smartsort.html')

if __name__ == '__main__':
    app.run()