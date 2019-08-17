from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CoffeeFeedback(db.Model):
    __tablename__ = 'coffe_feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    coffee = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, coffee, rating, comments):
        self.customer = customer
        self.coffee = coffee
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        coffee = request.form['coffee']
        rating = request.form['rating']
        comments = request.form['comments']

        if customer == '' or coffee == '':
            return render_template('index.html', message='Please enter required fields!')
        if db.session.query(CoffeeFeedback).filter(CoffeeFeedback.customer == customer).count() == 0:
            data = CoffeeFeedback(customer, coffee, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, coffee, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!')


if __name__ == '__main__':
    app.run()