from flask import Flask, render_template
import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")
@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")
@app.route("/list")
def list():
    return render_template("list.html")


@app.route('/signup-process', methods=['POST'])
def signup_process():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['fname']
        last_name = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['number']
        address = request.form['address']

        # Insert the data into the SQLite database
        conn = sqlite3.connect('petadoption.sqlite')
        c = conn.cursor()
        c.execute('''
            INSERT INTO userDetails (fname, lname, username, email, password, cellno, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, username, email, password, phone_number, address))

        conn.commit()
        conn.close()

        return render_template('homepage.html')

@app.route('/signin-process', methods=['POST'])
def signin_process():
    if request.method == 'POST':
        # Get the entered username and password
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Query the database to check if the user exists and the password is correct
        conn = sqlite3.connect('petadoption.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM userDetails WHERE username=? AND password=?', (entered_username, entered_password))
        user = c.fetchone()  # Fetch the first matching user

        conn.close()

        if user:
            # User exists, and the password is correct
            return render_template('homepage.html')
        else:
            # User not found or incorrect password
            error_message = "Invalid username or password. Please try again."
            return render_template('sign-in.html', error=error_message)

    return render_template('sign-in.html', error=None)


if __name__ == '__main__':
    app.run(debug=True)
