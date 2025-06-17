from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="783848",
        database="login_demo"
    )
    cursor = db.cursor()
    print("Database connection successful!")
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash("Please log in to access the home page.", "info")
        return redirect('/login')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        result = cursor.fetchone()

        if result:
            session['username'] = uname
            flash(f"Welcome back, {uname}!", "success")
            return redirect('/')
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (uname,))
        if cursor.fetchone():
            flash("Username already exists. Please choose a different one.", "warning")
            return redirect('/register')
        else:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, pwd))
                db.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect('/login')
            except mysql.connector.Error as err:
                db.rollback()
                flash(f"An error occurred during registration: {err}", "error")
                return redirect('/register')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)