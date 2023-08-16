#app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "newdb"
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

@app.route('/Local')
def Local():
    return render_template('Local.html')
    # app.py
@app.route('/homee')
def homee():
    return render_template('homee.html')
    
@app.route('/kandy')
def kandy():
    return render_template('Kandy.html')

@app.route('/lowc')
def lowc():
    return render_template('lowc.html')

@app.route('/saba')
def saba():
    return render_template('saba.html')
    
@app.route('/dev')
def dev():
    return render_template('dev.html')
    
@app.route('/fol')
def fol():
    return render_template('fol.html')

@app.route('/dar')
def dar():
    return render_template('dar.html')

@app.route('/uni')
def uni():
    return render_template('uni.html')    

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')    

@app.route('/coustume')
def coustume():
    return render_template('coustume.html') 

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


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

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


@app.route('/degrees', methods=['GET', 'POST'])
def degrees_page():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM universities")
    universities = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        university_id = int(request.form['university'])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM universities WHERE id = %s", (university_id,))
        selected_university = cursor.fetchone()

        cursor.execute("SELECT * FROM degrees WHERE university_id = %s", (university_id,))
        degrees = cursor.fetchall()
        cursor.close()
        
        return render_template('degrees.html', universities=universities, selected_university=selected_university, degrees=degrees)
    
    return render_template('degrees.html', universities=universities)

if __name__ == '__main__':
    app.run(debug=True)
