from flask import Flask, render_template, request
from gpo import subscriptions_gpo, search_gpo

app = Flask(__name__)
app.debug = True

subs = subscriptions_gpo()
searches = []

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html', searches = searches)

@app.route('/search', methods=['POST'])
def search_post():
    text = request.form['text']
    # processed_text = text.upper()
    searches = search_gpo(text)
    # print text
    return render_template('search.html', searches = searches)

@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html', subscriptions = subs)

@app.route('/smartsearch')
def smartsearch():
    return render_template('smartsearch.html')

@app.route('/smartsort')
def smartsort():
    return render_template('smartsort.html')

if __name__ == '__main__':
    app.run()