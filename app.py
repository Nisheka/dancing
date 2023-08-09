#app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "NewDB"
DB_USER = "postgres"
DB_PASS = "Tharu*99"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 

app = Flask(__name__)
app.static_folder = 'static'  # Set static folder as 'static' directory in your Flask application

# Routes
@app.route('/')
def home():
    return render_template('home.html')
    # app.py
@app.route('/sign')
def sign():
    return render_template('sign.html')

# Flask view function for 'search' endpoint
@app.route('/search')
def search():
    # Add your logic for the search functionality here
    return render_template('search.html')

 # Flask view function for 'search' endpoint
@app.route('/rating')
def rating():
    # Add your logic for the search functionality here
    return render_template('rating.html')
   


@app.route('/signup', methods=['POST'])
def signup():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    # Insert data into database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('home'))

@app.route('/signin', methods=['POST'])
def signin():
    # Get form data
    email = request.form['email']
    password = request.form['password']
    
    # Query database for user with given email and password
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        # Redirect to dashboard page for logged in user
        return redirect(url_for('dashboard'))
    else:
        # Redirect back to home page with error message
        return redirect(url_for('home', error='Invalid email or password'))

@app.route('/dashboard')
def dashboard():
    # Render dashboard template
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
