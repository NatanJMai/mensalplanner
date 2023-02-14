from flask           import Flask, render_template, request, session
from mysql.connector import Error
from flask_mysqldb   import MySQL
from os              import urandom


import database.db_functions as database
import flask_test as ftest
import tests
import webview
import sys
import threading

app = Flask(__name__)
app = ftest.run(app)
app.secret_key = urandom(24)
mysql = MySQL(app)


@app.route('/index')
def python_login():    
    return render_template('index.html')
    
@app.route('/login', methods = ['POST', 'GET'])
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
            
            return render_template('home.html')
        else:
            msg = "LOGIN NOT WORKING"
            home()
    
    return render_template('index.html')        

@app.route('/register', methods = ['POST', 'GET'])
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
            return render_template('index.html')
        
        database.insert_into_table(mysql.connection, 'user', username = username, password = password, email = email)
        msg = "SUCESSO ON CRATE"
        return render_template('home.html')

    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('home.html')





@app.route('/')
def hello_world():
    return render_template('index.html')

def start_server():
    app.run(host='localhost', port=80)

def view_page():
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("PyWebView & Flask", "http://localhost/index")
    webview.start()
    #sys.exit()
    return


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
                tests.test_insert()
            elif choose == 3:
                tests.show_all()
            else:
                return




if __name__ == "__main__":    
    view_page()
        
    
    

