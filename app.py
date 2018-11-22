from flask import Flask, render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from flask import flash
import sqlite3
MyApp = Flask(__name__)
MyApp.secret_key = "jjk44jK942K83kive9Xei73OO"

def logged():
        loggedIn = None
        if 'login' in session:
                loggedIn = 1
	return loggedIn

@MyApp.route("/")
def splash():
	return render_template('home.html', logged=logged())

@MyApp.route("/route2")
def route2():
	return render_template('route2.html', logged=logged())

@MyApp.route("/route3")
def route3():
	return render_template('route3.html', logged=logged())

@MyApp.route("/route4")
def route4():
	return render_template('route4.html', logged=logged())

@MyApp.route("/account")
def account():
	if 'login' not in session:
		flash('Login Needed')
		return redirect('/login')
      
	return render_template('account.html', user=session['login'], logged=logged())

@MyApp.route("/login")
def login():
	return render_template('login.html', logged=logged())

@MyApp.route("/createaccount")
def createaccount():
        return render_template('create.html', logged=logged())


@MyApp.route("/request", methods=['POST'])
def submit():
	 # calvin
        username = request.form['user']
         # pass
        password = request.form['pass']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''select * from users where username = ? and password = ?;''', (username, password))
        user = cur.fetchone()
        conn.close()
        if user is None:
               flash('Username or Password unsuccessful')
        else:
                session['login'] = user[0]
                flash('Successful Login')

	return redirect('login')

@MyApp.route("/create", methods=['POST'])
def create():
        username = request.form.get('user', type=str)
        password = request.form.get('pass', type=str)
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute('''select COUNT(*) from users where username = ?;''', (username,))
        user = curs.fetchone()
	if user[0] == 0:
		curs.execute('''insert into users values('admin','pass');''')
               	flash('Account Created')
		conn.commit()
		conn.close()
        	#return render_template('test.html', infos=username+password)
		return redirect('login')
        else:
                flash('Account not created')

	conn.close()
        return redirect('createaccount')


@MyApp.route("/logout")
def logout():
	if 'login' in session:
		session.pop('login', None)
        return redirect('/')

if __name__ == "__main__":
        MyApp.run()
