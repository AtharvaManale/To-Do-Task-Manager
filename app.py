from flask import Flask, render_template, redirect, request, session, flash
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask (__name__)
app.secret_key = os.getenv("key")

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT")),
    auth_plugin="mysql_native_password"
)


@app.route('/')
def signup():
    return render_template("signup.html")

@app.route('/sign', methods = ['post'])
def validate_info():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    mycursor = mydb.cursor()

    check_account_query = "SELECT * FROM login WHERE email=%s OR username=%s"
    mycursor.execute(check_account_query, (email, username))
    user = mycursor.fetchone()

    if user:
        flash("This Account Already Exist!")
        return redirect('/')
    else:
        hashed_password = generate_password_hash(password)

        create_account_query = "INSERT INTO login(email, username, password) VALUE(%s, %s, %s)"
        mycursor.execute(create_account_query, (email, username, hashed_password))
        mydb.commit()
        mycursor.close()

        flash("Account Was Created Successfully, Login To Continue", "info")
        return redirect('/l')
    
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
        favs = {row[0]: row[2] for row in results} #it creates dictionary eith task as key and fav as value
        mycursor.close()

        if not tasks:
            flash("No task present to work on...")
    
        return render_template("tasks.html", user = username, task = tasks, fav = favs)
    else:
        return redirect('/l')

@app.route('/add', methods = ['POST'])
def add():
    username = session['username']
    task = request.form['task']
    mycursor = mydb.cursor()

    select_tasks_query = "SELECT description, status, fav FROM tasks WHERE username=%s AND description=%s"
    mycursor.execute(select_tasks_query, (username, task))
    exist = mycursor.fetchone()
    
    if exist:
        flash("This task is already present")
        
    else:
        add_task_query = "INSERT INTO tasks (username, description) VALUES(%s, %s)"
        mycursor.execute(add_task_query, (username, task))
        mydb.commit()
    
    mycursor.close()
    return redirect('/task')

@app.route('/delete', methods = ['POST'])
def delete():
    username = session['username']
    t1 = request.form['t1']
    mycursor = mydb.cursor()

    delete_task_query = "DELETE FROM tasks WHERE username=%s AND description=%s"
    mycursor.execute(delete_task_query, (username, t1))
    mydb.commit()
    mycursor.close()

    return redirect('/task')

@app.route('/update_status', methods=['POST'])
def update_status():
    username = session['username']
    task = request.form['t1']
    status = request.form['status']
    mycursor = mydb.cursor()

    update_status_query = "UPDATE tasks SET status = %s WHERE username = %s AND description = %s"
    mycursor.execute(update_status_query, (status, username, task))
    mydb.commit()
    mycursor.close()

    return redirect('/task')

@app.route('/fav', methods = ['Post'])
def daily_task():
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
        flash("Here Your Go, Your Daily Tasks.")
        return render_template("daily.html", task = tasks, fav = favs, user = username)

@app.route('/remove', methods=['Post'])
def remove_dailytask():
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

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/l')

@app.route('/delete_account')
def delete_account():
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


if __name__ == '__main__':
    app.run(debug=True)