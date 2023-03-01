from pickle import TRUE
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

    return render_template('home/index.html', msg = msg)
    
@app.route('/mensalplanner/login', methods = ['POST', 'GET'])
def login():
    msg = ''
    l   = ['username', 'password']

    if ut.verifyRequestList('POST', l, request.form):
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

    return render_template('accounts/register.html', msg = msg)

@app.route('/mensalplanner/update_task', methods = ['POST', 'GET'])
def update_task():
    l = ['task_id', 'task_name', 'task_desc']

    if ut.verifyRequestList('POST', l, request.form):
        task_id   = request.form['task_id']
        task_name = request.form['task_name']
        task_desc = request.form['task_desc']
        
        database.update_task(mysql.connection, task_id, task_name, task_desc)
    return redirect(url_for('home'))

@app.route('/mensalplanner/remove_task', methods = ['POST', 'GET'])
def remove_task():
    task_id = request.args.get('jsdata')
    
    database.remove_task(mysql.connection, task_id)
    return redirect(url_for('login'))

@app.route('/mensalplanner/view_task')
def view_task():
     task_id = request.args.get('jsdata')
     task_details = database.get_task_from_id(mysql.connection, task_id)
     return render_template('home/view_task.html', task_details = task_details)

@app.route('/mensalplanner/new_task')
def new_task():
    user_id = request.args.get('user')
    
    return render_template('home/new_task.html', day = datetime.now().day, user_id = user_id, month = datetime.now().month, year = datetime.now().year)

@app.route('/mensalplanner/insert_newTask', methods = ['POST', 'GET'])
def insert_newTask():
    l = ['user_id', 'task_name', 'task_desc', 'task_date', 'task_value', 'task_debcred']
    
    for i in request.form.items():
        print(i)

    if ut.verifyRequestList('POST', l, request.form): 
        user_id    = request.form['user_id']
        task_name  = request.form['task_name']
        task_desc  = request.form['task_desc']
        task_year, task_month, task_day = request.form['task_date'].split('-')
        task_value = request.form['task_value']
        task_debcred = request.form['task_debcred']
        label_id = '1'
        
        # task_id, task_name, task_description, task_day, task_month, task_year, task_value, task_credit_debit, user, label        
        database.insert_into_table(mysql.connection, 'task', task_name = task_name, task_desc = task_desc, task_day = task_day, task_month = task_month, task_year = task_year, task_value = task_value, task_debcred = task_debcred, user_id = user_id, label_id = label_id)
    
    return redirect(url_for('home'))

@app.route('/mensalplanner/home')
def home():
    account = session

    # user is logged
    if 'loggedin' in account:
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        month_str = datetime.now().strftime('%B')

        # get tasks of user on now month
        tasks = database.get_task_from_user(mysql.connection, account['id'], month = datetime.now().month, year = datetime.now().year)

        # get days of month
        days_month = ut.get_days_of_date()

        # get tasks of days
        day_and_tasks = ut.get_days_and_task(days_month, tasks)

        return render_template('home/home.html', account = account, tasks = tasks, days_month = days_month, week_days = week_days, day_and_tasks = day_and_tasks, month = month_str)

    return redirect(url_for('login'))

@app.route('/mensalplanner/profile')
def profile():
    if 'loggedin' in session:
        u_id, name, password, email = database.verify_login(mysql.connection, session['username'], session['password'])
        account = {'user_id' : u_id, 'username' : name, 'password' : password, 'email' : email}

        return render_template('accounts/profile.html', account = account)
    return redirect(url_for('login'))


@app.route('/mensalplanner/logout')
def logout():
    session.clear()
    return home()

@app.route('/')
def hello_world():
    return render_template('home/index.html')

def start_server():
    app.run(host='localhost', port=80)

def view_page():
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("PyWebView & Flask", "http://localhost/mensalplanner/index", width=1240)
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
        
    
    

