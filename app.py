from flask import Flask, render_template
from flask import Markup
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from flask import flash
import sqlite3
MyApp = Flask(__name__)
MyApp.secret_key = "jjk44jK942K83kive9Xei73OO"

@MyApp.route("/")
def splash():
	return render_template('home.html', style=url_for('static', filename='style.css'))

@MyApp.route("/route2")
def route2():
	return render_template('route2.html', style=url_for('static', filename='style.css'))

@MyApp.route("/route3")
def route3():
	return render_template('route3.html', style=url_for('static', filename='style.css'))

@MyApp.route("/route4")
def route4():
	return render_template('route4.html', style=url_for('static', filename='style.css'))

@MyApp.route("/account")
def account():
	if 'login' not in session:
		flash('Login Needed')
		return redirect('/login')
      
	return render_template('account.html', style=url_for('static', filename='style.css'), user='Calvin')

@MyApp.route("/login")
def login():
	return render_template('login.html', style=url_for('static', filename='style.css'))

@MyApp.route("/request", methods=['POST'])
def submit():
         # calvin
        username = request.form['user']
         # pass
        password = request.form['pass']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''select * from users where username = ? and password = ?;''', (username, password))
        user = cur.fetchone();
        conn.close()
        if user is None:
               flash('Username or Password unsuccessful')
        else:
                session['login'] = user[0]
                flash('Successful Login')

	return redirect('login')

@MyApp.route("/logout")
def logout():
	if 'login' in session:
		session.pop('login', None)
        return redirect('/')

if __name__ == "__main__":
        MyApp.run()
