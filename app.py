from flask import Flask, render_template, redirect, request, session, flash
import mysql.connector
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import re
import random
import time

load_dotenv()

app = Flask (__name__)

app.config['MAIL_SERVER'] = os.getenv("Email_SERVER")
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("Email_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("Email_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("Email_USERNAME")
app.secret_key = os.getenv("key")

mail = Mail(app)
csrf = CSRFProtect(app)


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT")),
    auth_plugin="mysql_native_password"
)

ALLOWED_PATTERN = re.compile(r"^[a-zA-Z0-9\s.'-]{1,200}$")

@app.route('/')
def signup():
    return render_template("signup.html")

@app.route('/sign', methods = ['post'])
def validate_info():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    session['email'] = email
    session['username'] = username
    session['password'] = hashed_password
    mycursor = mydb.cursor()

    check_account_query = "SELECT * FROM login WHERE email=%s OR username=%s"
    mycursor.execute(check_account_query, (email, username))
    user = mycursor.fetchone()

    if not ALLOWED_PATTERN.match(username):
        flash("Invalid Username description. Please avoid using special characters.")
        return redirect('/')

    if len(password) < 8 or len(password) > 12:
        flash("Password must be between 8 and 12 characters long.")
        return redirect('/')

    if user:
        flash("This Account Already Exist!")
        return redirect('/')
    else:
        mydb.commit()
        mycursor.close()

        return redirect('/signup/verification')

@app.route('/signup/verification', methods = ['Get', 'Post'])
def otp_generator():
    otp = str(random.randint(100000, 999999))
    session['otp'] = generate_password_hash(otp)
    session['otp_time'] = time.time()

    msg = Message(
        subject="Account Verification",
        recipients=[session['email']],
        body=f"Hey {session['username']}! This is One Time Password to verify your account {otp}"
    )
    try:
        mail.send(msg)
    except Exception as e:
        print("Mail send failed:", e)
        flash("Could not send confirmation email. Enter valid mail address", "warning")

    return render_template("otp.html", email = session['email'])

@app.route('/verification', methods = ['Post'])
def verify():
    d1 = request.form['d1']
    d2 = request.form['d2']
    d3 = request.form['d3']
    d4 = request.form['d4']
    d5 = request.form['d5']
    d6 = request.form['d6']
    
    list_in = [d1, d2, d3, d4, d5, d6]
    user_input = "".join(list_in)

    if time.time() - session['otp_time'] > 300:
        session.pop('otp', None)
        session.pop('otp_time', None)

        flash("OTP expired, please click on resend.")
        return render_template("otp.html", email = session['email'])

    elif not check_password_hash(session['otp'], user_input):
        flash("Enter Correct OTP!")
        return render_template("otp.html")

    msg = Message(
            subject="Confirmation from TO-DO!",
            recipients = [session['email']],
            body= f'Hey {session["username"]}! Thanks For Signing Up with TO-DO. Enjoy the experience of the app.'
        )
    try:
        mail.send(msg)
    except Exception as e:
        print("Mail send failed:", e)
        flash("Could not send confirmation email. Enter valid mail address", "warning")
    mycursor = mydb.cursor()
    create_account_query = "INSERT INTO login(email, username, password) VALUES(%s, %s, %s)"
    mycursor.execute(create_account_query, (session["email"], session["username"], session['password']))
    mydb.commit()
    mycursor.close()

    session.pop("email", None)
    session.pop("username", None)
    session.pop("password", None)
    session.pop("otp", None)
    session.pop("otp_time", None)

    flash("Account Was Created Successfully, Login To Continue", "info")
    return redirect('/l')

@app.route('/back')
def back():
    session.pop("email", None)
    session.pop("username", None)
    session.pop("password", None)
    session.pop("otp", None)
    session.pop("otp_time", None)

    flash("Sign Up with Valid Email")
    return redirect('/')

@app.route('/l')
def login():
    return render_template("login.html")

@app.route('/login', methods = ['post'])
def validate_login():
    username = request.form['username']
    password = request.form['password']
    mycursor = mydb.cursor()

    verify_account_query = "SELECT * FROM login WHERE username=%s"
    mycursor.execute(verify_account_query, (username,))
    user = mycursor.fetchone()
    mycursor.close()

    if not ALLOWED_PATTERN.match(username):
        flash("Invalid credentials description. Please avoid using special characters.")
        return redirect('/l')

    if user and check_password_hash(user[2], password):
        session['username'] = username
        return redirect('/home')
    else:
        flash("Incorrect Credentilas, Try again")
        return redirect('/l')

@app.route('/home')
def home():
    if "username" in session:
        username = session['username']
        return render_template("home.html", user = username)
    else:
        return redirect('/l')

@app.route('/task')
def tasks():
    if "username" in session:
        username = session['username']
        mycursor = mydb.cursor()

        show_tasks_query = "SELECT description, status, fav FROM tasks WHERE username=%s"
        mycursor.execute(show_tasks_query, (username,))
        results = mycursor.fetchall() 
        tasks = [(r[0], r[1]) for r in results]# it creates a list of tuples as tasks
        favs = {r1[0]: r1[2] for r1 in results}# it creates dictionary with task as key and fav as value
        mycursor.close()

        if not tasks:
            flash("No task present to work on...")
    
        return render_template("tasks.html", user = username, task = tasks, fav = favs)
    else:
        flask("First Login To Access Features.")
        return redirect('/l')

@app.route('/add', methods = ['POST'])
def add():
    if "username" in session:
        username = session['username']
        task = request.form['task']
        mycursor = mydb.cursor()

        select_tasks_query = "SELECT description, status, fav FROM tasks WHERE username=%s AND description=%s"
        mycursor.execute(select_tasks_query, (username, task))
        exist = mycursor.fetchone()

        if not ALLOWED_PATTERN.match(task):
            flash("Invalid task description. Please avoid using special characters.")
            return redirect('/task')
        
        if exist:
            flash("This task is already present")
            
        else:
            add_task_query = "INSERT INTO tasks (username, description) VALUES(%s, %s)"
            mycursor.execute(add_task_query, (username, task))
            mydb.commit()
        
        mycursor.close()
        return redirect('/task')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')


@app.route('/delete', methods = ['POST'])
def delete_():
    if "username" in session:
        username = session['username']
        t1 = request.form['t1']
        mycursor = mydb.cursor()

        delete_task_query = "DELETE FROM tasks WHERE username=%s AND description=%s"
        mycursor.execute(delete_task_query, (username, t1))
        mydb.commit()
        mycursor.close()

        return redirect('/task')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/update_status', methods=['POST'])
def update_status():
    if "username" in session:
        username = session['username']
        task = request.form['t1']
        status = request.form['status']
        mycursor = mydb.cursor()

        update_status_query = "UPDATE tasks SET status = %s WHERE username = %s AND description = %s"
        mycursor.execute(update_status_query, (status, username, task))
        mydb.commit()
        mycursor.close()

        return redirect('/task')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/update_status', methods=['POST'])
def update_status_():
    if "username" in session:
        username = session['username']
        task = request.form['t1']
        status = request.form['status']
        mycursor = mydb.cursor()

        update_status_query = "UPDATE tasks SET status = %s WHERE username = %s AND description = %s"
        mycursor.execute(update_status_query, (status, username, task))
        mydb.commit()
        mycursor.close()

        return redirect('/task')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/fav', methods = ['Post'])
def daily_task():
    if "username" in session:
        username = session['username']
        task = request.form['t1']
        mycursor = mydb.cursor()

        add_dailytasks_query = "SELECT fav FROM tasks WHERE username=%s AND description=%s"
        mycursor.execute(add_dailytasks_query, (username, task))
        current = mycursor.fetchone()

        if current:
            new_fav = 0 if current[0] == 1 else 1
            update_dailytasks_query = "UPDATE tasks SET fav=%s WHERE username=%s AND description=%s"
            mycursor.execute(update_dailytasks_query, (new_fav, username, task))
            mydb.commit()

        mycursor.close()
        return redirect('/task')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/show')
def show_daily():
    if "username" in session:
        username = session['username']
        mycursor = mydb.cursor()
        
        show_dailytasks_query = "SELECT description, status, fav FROM tasks WHERE username =%s AND fav = 1"
        mycursor.execute(show_dailytasks_query, (username,))
        results = mycursor.fetchall()
        tasks = [(r[0], r[1]) for r in results]
        favs = {row[0]: row[2] for row in results}

        if not results:
            flash("No daily tasks present to work on...")

        mycursor.close()
        if results:
            flash("Here You Go, Your Daily Tasks.")
        return render_template("daily.html", task = tasks, fav = favs, user = username)
    else:
        flask("First Login To Access Features.")
        return redirect('/l')

@app.route('/update_status_new', methods=['POST', 'PUT'], endpoint='update_status_new_ep')
def update_status_new():
    if "username" in session:
        username = session['username']
        task = request.form['t1']
        status = request.form['status']
        mycursor = mydb.cursor()

        update_status_query = "UPDATE tasks SET status = %s WHERE username = %s AND description = %s"
        mycursor.execute(update_status_query, (status, username, task))
        mydb.commit()
        mycursor.close()

        return redirect('/show')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/delete_new', methods = ['POST'])
def delete_new():
    if "username" in session:
        username = session['username']
        t1 = request.form['t1']
        mycursor = mydb.cursor()

        delete_task_query = "DELETE FROM tasks WHERE username=%s AND description=%s"
        mycursor.execute(delete_task_query, (username, t1))
        mydb.commit()
        mycursor.close()

        return redirect('/show')
    else:
        flask("First Login To Access Features.", "info")
        return redirect('/l')

@app.route('/remove', methods=['Post'])
def remove_dailytask():
    if "username" in session:
        username = session['username']
        task = request.form['t1']
        mycursor = mydb.cursor()

        access_dailytasks_query = "SELECT fav FROM tasks WHERE username=%s AND description=%s"
        mycursor.execute(access_dailytasks_query, (username, task))
        current = mycursor.fetchone()

        if current:
            new_fav = 0 
            remove_dailytask_query = "UPDATE tasks SET fav = %s WHERE username = %s AND description = %s"
            mycursor.execute(remove_dailytask_query, (new_fav, username, task))
            mydb.commit()

        mycursor.close()
        return redirect('/show')
    else:
        flask("First Login To Access Features.")
        return redirect('/l')

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/l')

@app.route('/deleteaccount', methods = ['Post'])
def delete_account():
    if "username" in session:
        username = session['username']
        mycursor = mydb.cursor()

        delete_account_query = "DELETE FROM login WHERE username=%s"
        mycursor.execute(delete_account_query, (username,))
        mydb.commit()

        delete_alltasks_query = "DELETE FROM tasks WHERE username=%s"
        mycursor.execute(delete_alltasks_query, (username,))
        mydb.commit()
        
        mycursor.close()
        session.pop("username", None)
        
        flash("Account Was Deleted Successfully, SignUp To Create New", "info")
        return redirect('/')
    else:
        flash("First Login To Access Features.","info")
        return redirect('/l')

if __name__ == '__main__':
    app.run(debug=True)

