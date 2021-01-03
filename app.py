from enum import unique
from flask import Flask, request, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY = 'topsecretkey',
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def index():
    return "Hello, World again! and Hi!"

@app.route("/new/")
def query_string(greeting = 'hello!'):
    query_val = request.args.get("greeting", greeting)
    return "<h1> The greeting is: {} </h1>".format(query_val)

@app.route('/user')
@app.route('/user/<username>')
def no_query_string(username='Gagan'):
    return '<h1> Hello, there! - {} </h1>'.format(username.title())

# STRINGS (default datatype of query strings in the URLs)
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> Here is the String: ' + name + '</h1>'

# NUMBERS
@app.route('/number/<int:num>')
def working_with_numbers(num):
    return '<h1> Here is the number: ' + str(num) + '</h1>'

# NUMBERS
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1> The sum is: {} </h1>'.format(num1 + num2)

# FLOATS
@app.route('/multiply/<float:num1>/<float:num2>')
def multiply_two_numbers(num1, num2):
    return '<h1> The product is: {} </h1>'.format(num1 * num2)

@app.route('/temp')
def using_template():
    return render_template('hello.html')

@app.route('/watch')
def top_movies():
    movie_list = [
        'Neon Demon',
        'Ann with an E',
        'Taken',
        'Inception',
        'Person of Interest'
    ]
    return render_template('movies.html', movies = movie_list, name = 'Harry')

@app.route('/tables')
def movies_table():
    movies_dict = {
        'Neon Demon': 2.30,
        'Ann with an E': 6,
        'Taken': 1.3,
        'Inception': 3.2,
        'Person of Interest': 4.5
    }
    return render_template('table_data.html', movies=movies_dict, name='Sally')

@app.route('/filters')
def filter_data():
    movies_dict = {
        'neon Demon': 2.30,
        'ann with an e': 6,
        'taken': 1.3,
        'inception': 3.2,
        'person of Interest': 4.5
    }
    return render_template('filter_data.html', movies = movies_dict, name = None, film = 'Umbrella Academy')

@app.route('/macros')
def using_macros():
    movies_dict = {
        'neon Demon': 2.30,
        'ann with an e': 6,
        'taken': 1.3,
        'inception': 3.2,
        'person of Interest': 4.5
    }
    return render_template('using_macros.html', movies = movies_dict)

@app.route('/session')
def session_data():
    if 'name' not in session:
        session['name'] = 'Gagan'
    return render_template('session.html', session=session, name=session['name'])

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique = True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default = datetime.utcnow())
    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)