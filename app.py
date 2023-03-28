from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import io
import base64
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Exist_User(db.Model):
    __tablename__ = 'exist_user'
    login = db.Column(db.String(255), nullable=False, primary_key=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Exist_User %r>' % self.login


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<History %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_customer = request.form['login']
        password = request.form['password']

        user = db.session.query(Exist_User).filter_by(login=login_customer).all()
        if len(user) != 0:
            user = user[0]
            if password == user.password:
                return redirect(f'/customer/{login_customer}/{password}')
            else:
                return redirect('/error')
        else:
            return redirect('/error')
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        login_customer = request.form['login']
        password = request.form['password']

        user = Exist_User(login=login_customer, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(f'/login')
        except:
            return redirect('/error')
    else:
        return render_template('register.html')


@app.route('/customer/<login>/<password>', methods=['POST', 'GET'])
def customer(login, password):
    user = db.session.query(Exist_User).filter_by(login=login).all()
    if len(user) != 0:
        user = user[0]
        if password == user.password:
            if request.method == 'POST':
                login_customer = request.form['login']
                password = request.form['password']
            else:
                data = db.session.query(History).filter_by(login=f'{login}/{password}').order_by(History.date).all()
                power = sum([i.value for i in data])
                price = 5
                cost = power*price
                plt.plot(range(len(data)), [i.value for i in data])
                img = io.BytesIO()
                plt.savefig(img, format='png')
                plot_url = base64.b64encode(img.getvalue()).decode()
                return render_template('customer.html', power=power, cost=cost, plot_url=plot_url)
        else:
            return redirect('/error')
    else:
        return redirect('/error')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


@app.route('/op', methods=['POST', 'GET'])
def op():
    return render_template('admin.html')


@app.route('/error', methods=['POST', 'GET'])
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
