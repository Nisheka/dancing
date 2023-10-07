#app.py
from flask import Flask,jsonify, request, session, redirect, url_for, render_template, flash
from datetime import datetime
import psycopg2 #pip install psycopg2 
import csv



app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "NewDB"
DB_USER = "postgres"
DB_PASS = "Tharu*99"

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    print("Connected to the database successfully!")
except psycopg2.OperationalError as e:
    print("Error:", e)


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


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['id'] = user[0]  # Store user ID in session
            role = user[4]  # Get the user role from the database
            session['name'] = user[1] 
            

            if role == 'event_manager':

                return redirect(url_for('event'))  # Redirect to event manager dashboard

            elif role == 'admin':
                # Redirect to admin dashboard
                # Add admin dashboard route here
                pass
            elif role == 'artist':
                # Redirect to artist dashboard
                # Add artist dashboard route here
                pass
            else:
                return redirect(url_for('dashboard'))  # Redirect to user dashboard
        else:
            return redirect(url_for('sign', error='Invalid email or password'))

    return render_template('sign.html')

@app.route('/signout')
def signout():
    session.pop('id', None)  # Remove user ID from session
    return redirect(url_for('event'))




@app.route('/dashboard')
def dashboard():
    # Render dashboard template
    return render_template('dashboard.html')
    
@app.route('/event', methods=['GET', 'POST'])
def event():
    if 'id' not in session:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        # Get event details from the form
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        break_time = request.form['break_time']
        sessions = request.form['sessions']
        lead = request.form['lead']

        # Insert event details into the events table
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (event_date, start_time, end_time, break_time, sessions, lead) VALUES (%s, %s, %s, %s, %s, %s)",
                       (event_date, start_time, end_time, break_time, sessions, lead))
        conn.commit()
        cursor.close()

        return redirect(url_for('calendar'))

    return render_template('event.html')



@app.route('/get_events')
def get_events():
    # Fetch event data from the database and return it as JSON
    start = datetime.fromisoformat(request.args.get('start'))
    end = datetime.fromisoformat(request.args.get('end'))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_date BETWEEN %s AND %s", (start.date(), end.date()))
    events = cursor.fetchall()
    cursor.close()

    event_list = []
    for event in events:
        event_list.append({
            'lead': event[6],  # Assuming 'lead' is the 7th column in your events table
            'start': event[2].isoformat(),  # Assuming 'event_date' is the 3rd column
            'end': event[3].isoformat()     # Assuming 'end_time' is the 4th column
        })

    return jsonify({'events': event_list})

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



@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'id' in session:
        id = session['id']
        email = session.get('email', None)
        cursor = conn.cursor()
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            # Update user details in the database
            cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
            conn.commit()
            flash('User details updated successfully', 'success')
        
        # Fetch user details from the database
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        
        return render_template('account.html', user=user)
    else:
        return redirect(url_for('signin'))




@app.route('/update_user', methods=['POST'])
def update_user():
    if 'id' in session:
        user_id = session['id']
        name = request.form['name']
        email = request.form['email']
        
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        cursor.close()

        # Redirect to my_account page after updating
        return redirect(url_for('account'))
    
    # Redirect to login if user not logged in or other error occurs
    return redirect(url_for('signin'))

    
    # Redirect to login if user not logged in or other error occurs
    return redirect(url_for('signin'))

# ----------- Second Flask Application Routes -----------
# Define a function to recommend dance style based on user input
def recommend_dance_style(user_input):
    # Load dance style data from a CSV file (replace 'dance_styles.csv' with your CSV file)
    dance_styles = []
    with open('dance_style.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dance_styles.append(row)

    # Define a function to calculate a match score between user input and dance styles
    def calculate_match_score(dance_style, user_input):
        # Initialize match score to 0
        match_score = 0

        # Check if required keys are present in dance_style and user_input dictionaries
        if 'age_min' in dance_style and 'age_max' in dance_style and 'age' in user_input:
            if int(dance_style.get('age_min', 0)) <= int(user_input['age']) <= int(dance_style.get('age_max', float('inf'))):
                match_score += 1

        # Check if 'Previous Dance Experience' is present in dance_style and user_input dictionaries
        if 'Previous Dance Experience' in dance_style and 'experience' in user_input:
            if dance_style['Previous Dance Experience'].lower() == user_input['experience'].lower():
                match_score += 1

        # Check if 'Goals' is present in dance_style and user_input dictionaries
        if 'Goals' in dance_style and 'goals' in user_input:
            if dance_style['Goals'].lower() == user_input['goals'].lower():
                match_score += 1

        return match_score

    # Calculate match scores for each dance style
    match_scores = {}
    for style in dance_styles:
        match_scores[style.get('Recommended Dance Style', 'Unknown')] = calculate_match_score(style, user_input)

    # Get the dance style with the highest match score
    recommended_style = max(match_scores, key=match_scores.get)

    return recommended_style

@app.route('/dance-recommendation', methods=['GET', 'POST'])
def dance_recommendation():
    recommended_style = None
    user_input = {}  # Define an empty dictionary for user input

    if request.method == 'POST':
        user_input = {
            'age': request.form['age'],
            'experience': request.form['experience'],
            'inspiration': request.form['inspiration'],
            'goals': request.form['goals'],
            'styles': request.form['styles'],
            'explore': request.form['explore'],
            'limitations': request.form['limitations'],
            'interest': request.form['interest'],
            'artist': request.form['artist'],
            'flexibility_coordination': request.form['flexibility'],
            'solo_partner_group': request.form['solo_partner_group'],
            'music_genre': request.form['music_genre']
            # Add more input fields as needed
        }

        # Call the recommend_dance_style function
        recommended_style = recommend_dance_style(user_input)

    return render_template('index.html', recommended_style=recommended_style)

if __name__ == '__main__':
    app.run(debug=True)


