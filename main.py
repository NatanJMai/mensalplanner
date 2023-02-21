from flask           import Flask, render_template, request, session, redirect, url_for
from mysql.connector import Error
from flask_mysqldb   import MySQL
from os              import urandom
from datetime        import datetime

import database.db_functions as database
import flask_test as ftest
import tests
import webview
import sys
import threading
import util.util as ut


app = Flask(__name__)
app = ftest.run(app)
app.secret_key = urandom(24)
mysql = MySQL(app)

@app.route('/mensalplanner/index')
def index(**kwargs):    
    msg = ''
    if 'msg' in kwargs:
        msg = kwargs['msg']

    return render_template('index.html', msg = msg)
    
@app.route('/mensalplanner/login', methods = ['POST', 'GET'])
def login():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account  = database.verify_login(mysql.connection, username, password)

        # if account != null
        if account:
            u_id, name, password, email = account

            session['id']    = u_id
            session['email'] = email
            session['loggedin'] = True
            session['username'] = name
            session['password'] = password

            return home()
        else:
            msg = "User not found!"    
    return index(msg = msg)
            

@app.route('/mensalplanner/register', methods = ['POST', 'GET'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        result   = database.insert_into_table(mysql.connection, 'user', username = username, password = password, email = email)    

        # if result = true, there is already an user.
        if not result:
            msg = "User already created!"
            return index(msg = msg)
        
        database.insert_into_table(mysql.connection, 'user', username = username, password = password, email = email)
        return login()

    return render_template('register.html', msg = msg)

@app.route('/mensalplanner/update_task', methods = ['POST', 'GET'])
def update_task():
    if request.method == 'POST' and 'task_id' in request.form and 'task_name' in request.form and 'task_desc' in request.form:
        task_id   = request.form['task_id']
        task_name = request.form['task_name']
        task_desc = request.form['task_desc']
        
        database.update_task(mysql.connection, task_id, task_name, task_desc)
        #print(f"ID: '{task_id}' NAME '{task_name}' e DESC '{task_desc}'")
    return home()

@app.route('/mensalplanner/remove_task', methods = ['POST', 'GET'])
def remove_task():
    task_id = request.args.get('jsdata')
    
    database.remove_task(mysql.connection, task_id)
    return home()

@app.route('/mensalplanner/view_task')
def view_task():
     task_id = request.args.get('jsdata')
     task_details = database.get_task_from_id(mysql.connection, task_id)
     return render_template('view_task.html', task_details = task_details)


@app.route('/mensalplanner/home')
def home():
    account = session

    # user is logged
    if 'loggedin' in account:
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # get tasks of user on now month
        tasks = database.get_task_from_user(mysql.connection, account['id'], month = datetime.now().month, year = datetime.now().year)
        
        # get days of month
        days_month = ut.get_days_of_date()

        # get tasks of days
        day_and_tasks = ut.get_days_and_task(days_month, tasks)

        return render_template('home.html', account = account, tasks = tasks, days_month = days_month, week_days = week_days, day_and_tasks = day_and_tasks)

    return redirect(url_for('login'))

@app.route('/mensalplanner/profile')
def profile():
    if 'loggedin' in session:
        u_id, name, password, email = database.verify_login(mysql.connection, session['username'], session['password'])
        account = {'user_id' : u_id, 'username' : name, 'password' : password, 'email' : email}

        return render_template('profile.html', account = account)
    return home()


@app.route('/mensalplanner/logout')
def logout():
    session.clear()
    return home()

@app.route('/')
def hello_world():
    return render_template('index.html')

def start_server():
    app.run(host='localhost', port=80)

def view_page():
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("PyWebView & Flask", "http://localhost/mensalplanner/index", width = 1200)
    webview.start()
    sys.exit()


def main():
    while(1):
        try:
            choose = int(input('''------- CHOOSE ------\n0. SHOW PAGE\n1. START DATABASES\n2. TEST INSERT RECORDS\n3. SHOW RECORDS\nOTHER. EXIT'''))
        except:
            print("Please type a correct option.")
        else:
            if choose == 0:
                view_page()
            elif choose == 1:
                database.start_database()
            elif choose == 2:
                tests.test_insert(int(input("DAY")))
            elif choose == 3:
                tests.show_all()
            else:
                return




if __name__ == "__main__":    
    view_page()
    #main()
        
    
    

