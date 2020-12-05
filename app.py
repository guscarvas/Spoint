from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)


@app.route('/',methods=['GET'])  # Root of your web platform
def home():
    return '<h1>Hello World!</h1>'


books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


if __name__ == '__main__':
    app.run()
