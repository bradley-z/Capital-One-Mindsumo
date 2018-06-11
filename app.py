from flask import Flask, render_template
from gpo import subscriptions

app = Flask(__name__)
# app.debug = True

subs = subscriptions()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

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