#app.py
from flask import Flask,jsonify, request, session, redirect, url_for, render_template, flash,Response, send_file
from datetime import datetime
import psycopg2 #pip install psycopg2 
import csv
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from geopy.distance import geodesic
from chat import get_response


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

@app.route('/western')
def western():
    return render_template('western.html')    

@app.route('/ba')
def ba():
    return render_template('ba.html')  


@app.route('/hp')
def hp():
    return render_template('hp.html')          


@app.route('/jaz')
def jaz():
    return render_template('jaz.html')  


@app.route('/tap')
def tap():
    return render_template('tap.html') 

@app.route('/cou')
def cou():
    return render_template('cou.html')

@app.route('/bal')
def bal():
    return render_template('bal.html')    

@app.route('/uni')
def uni():
    return render_template('uni.html')    

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')    
    
@app.route('/barath')
def barath():
    return render_template('barath.html') 

@app.route('/exam')
def exam():
    return render_template('exam.html')  

@app.route('/rule')
def rule():
    return render_template('rule.html')   
    
@app.route('/barth')
def barth():
    return render_template('barth.html')



 # Flask view function for 'search' endpoint
@app.route('/rating')
def rating():
    # Add your logic for the search functionality here
    return render_template('rating.html')


@app.route('/calendar')
def calendar():
    # Example: Fetching events from a database
    # Replace this with your actual database fetching logic
    cursor = conn.cursor()
    cursor.execute("SELECT title, date, time, location FROM events ORDER BY date DESC")
    events = cursor.fetchall()
    cursor.close()

    return render_template('calendar.html', events=events)


@app.route('/signup', methods=['POST'])
def signup():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']
    password = request.form['password']
    
    # Insert data into database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password,rolr) VALUES (%s, %s, %s)", (name, email, password,role))
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

            # Redirect to the stored target page after login
            return redirect(url_for('get_target_page'))
        else:
            return redirect(url_for('sign', error='Invalid email or password'))

    return render_template('sign.html')

# Your existing routes...

# Route to get the stored target page and redirect after login
@app.route('/get_target_page')
def get_target_page():
    target_page = session.pop('target_page', 'dashboard')  # Default to dashboard if no target_page is stored
    return redirect(url_for(target_page))

@app.route('/store_target_page', methods=['POST'])
def store_target_page():
    data = request.get_json()
    target_page = data.get('target_page')
    session['target_page'] = target_page
    return jsonify(success=True)


@app.route('/dashboard')
def dashboard():
    # Render dashboard template
    return render_template('dashboard.html')



@app.route('/myler')
def myler():
    user_id = session.get('id')

    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT subtopic_id, completed FROM users_progress WHERE user_id = %s", (user_id,))
    raw_progress_data = cursor.fetchall()

    # Process the data
    progress_data = []
    for record in raw_progress_data:
        subtopic_id, completed = record
        progress_record = {
            "subtopic_id": subtopic_id,
            "status": "Completed" if completed else "Not Completed"
        }
        progress_data.append(progress_record)

    cursor.close()
    # Close the connection if you're done with it

    return render_template('myler.html', progress_data=progress_data)

# Inside app.py
@app.route('/mark_complete/<int:subtopic_id>', methods=['GET'])
def mark_complete(subtopic_id):
 
    # Mark subtopic as completed for the current user
    if 'id' in session:
        user_id = session.get['id']
        print("User ID:", user_id)  # Debugging
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users_progress (user_id, subtopic_id, completed) VALUES (%s, %s, %s)",
                           (user_id, subtopic_id, True))
            conn.commit()
            print("Insert successful")  # Debugging
        except Exception as e:
            print("Error inserting into users_progress:", e)  # Debugging
            conn.rollback()  # Rollback in case of an error
        finally:
            cursor.close()
    return redirect(request.referrer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with conn.cursor() as cursor:
            try:
                # Modified SQL query to check the role
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s AND role = 'event_manager'", (email, password))
                user = cursor.fetchone()

                if user:
                    # User is an event manager, proceed to the event manager dashboard
                    return redirect(url_for('event'))
                else:
                    # User is not an event manager or login details are incorrect
                    return render_template('login.html', error='Invalid email/password or not authorized as an event manager.')

            except psycopg2.Error as e:
                conn.rollback()  # Rollback the transaction on error
                print("Database error: ", e)  # Log the database error for debugging
                return render_template('login.html', error='A database error occurred. Please try again.')
    
    # If it's a GET request, just render the sign-in template
    return render_template('login.html')


@app.route('/gets_target_page')
def gets_target_page():
    targets_page = session.pop('targets_page', 'calendar')  # Default to dashboard if no target_page is stored
    return redirect(url_for(targets_page))


@app.route('/stores_target_page', methods=['POST'])
def stores_target_page():
    data = request.get_json()
    targets_page = data.get('targets_page')
    session['targets_page'] = targets_page
    return jsonify(success=True)


@app.route('/signout')
def signout():
    session.pop('id', None)  # Remove user ID from session
    return redirect(url_for('calender'))



@app.route('/event', methods=['GET', 'POST'])
def event():
    
    if request.method == 'POST':
        try:
            event_title = request.form['title']
            event_date = request.form['date']
            event_description = request.form['description']
            event_time = request.form['time']  # Retrieve time
            event_location = request.form['location']  # Retrieve location
        
            

            cursor = conn.cursor()
            cursor.execute("INSERT INTO events (title, date, description, time , location) VALUES (%s, %s, %s, %s, %s)", 
                           (event_title, event_date,event_description,event_time, event_location,))
            conn.commit()
            cursor.close()
            return redirect(url_for('calendar', message='Event created successfully!'))
        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            cursor.close()
            print("An error occurred: ", e)
            return redirect(url_for('event', error='An error occurred while creating the event.'))

    return render_template('event.html')


@app.route('/events')
def show_events():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE date = %s ", (start.date()))
    events = cursor.fetchall()
    cursor.close()
    return render_template('home.html', events=events)



@app.route('/get_events')
def get_events():
    # Fetch event data from the database and return it as JSON
    start = datetime.fromisoformat(request.args.get('start'))


    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE date = %s ", (start.date()))
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


@app.route('/modules')
def modules():
    # Fetch main modules from the database
   
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modules")
    modules = cursor.fetchall()
    cursor.close()

    return render_template('modules.html', modules=modules)

# Update the '/module/<int:module_id>' route in your app.py file
@app.route('/module/<int:module_id>')
def module(module_id):
    # Fetch subtopics and videos for the selected module
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            st.id, 
            st.title AS subtopic_title, 
            st.description, 
            st.video_id, 
            st.duration, 
            v.title AS video_title
        FROM subtopics st 
        LEFT JOIN videos v ON st.video_id = v.video_id
        WHERE st.module_id = %s
    """, (module_id,))
    data = cursor.fetchall()



    # Fetch module title for the selected module
    cursor.execute("SELECT id, title FROM modules WHERE id = %s", (module_id,))
    module_title = cursor.fetchone()[0]

    cursor.close()
    return render_template('module.html', data=data, module_title=module_title)






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

@app.route('/search')
def search():
    category = request.args.get('category')

    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT id,name,category, description, price, image FROM locations WHERE category = %s", (category,))
    else:
        cursor.execute("SELECT id,name,category, description, price, image FROM locations")

    # Fetch results as tuples
    locations_data = cursor.fetchall()
    cursor.close()

    # Convert each tuple to a dictionary
    locations = []
    for location_data in locations_data:
        location_dict = {
            'id': location_data[0],
            'name': location_data[1],
            'category': location_data[2],
            'description': location_data[3],
            'price': location_data[4],
            'image': location_data[5]  # Add the 'image' field
            # Add other fields as needed
        }
        locations.append(location_dict)

    return render_template('search.html', locations=locations)
def get_all_locations():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM locations;')
        locations = cursor.fetchall()
        cursor.close()  # Close the cursor, but keep the connection open
        return locations

    except psycopg2.Error as e:
        print("Error fetching locations from the database:", e)
        return []

    finally:
        # Close the cursor (if it was opened) and connection
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/update_location', methods=['GET'])
def update_location():
    global current_latitude, current_longitude

    # Receive latitude and longitude from the POST request's form data
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Store the received values in the global variables
    current_latitude = latitude
    current_longitude = longitude
    current_location = (current_latitude, current_longitude)

    # Calculate distances and format the result
    nearest_locations_with_distance = []

    # Retrieve all locations from the database
    locations = get_all_locations()

    for location in locations:
        location_coords = (location[2], location[3])  # Assuming latitude is at index 2 and longitude at index 3
        distance = geodesic(current_location, location_coords).kilometers

        nearest_locations_with_distance.append({
            'id': location[0],
            'name': location[1],
            'latitude': location[2],
            'longitude': location[3],
            'category': location[4],
            'price': location[5],
            'description': location[6],
            'image': location[7],
            'distance': distance
        })

    return render_template('filtered.html', locations=nearest_locations_with_distance)
    
@app.route('/coustume')
def coustume():
        try:
    

        # Create a cursor
          cursor = conn.cursor()

        # Execute SQL query to fetch all active products
          cursor.execute("SELECT * FROM product WHERE active=True")

        # Fetch all rows
          products = cursor.fetchall()

          return render_template('coustume.html', products=products)

        except psycopg2.Error as e:
          print("Error fetching products from the database:", e)

        finally:
        # Close the cursor (if it was opened) and connection
         if 'cursor' in locals():
            cursor.close()
        conn.close()


@app.route('/item')
def item():
    # Get the 'id' parameter from the request
    product_id = request.args.get('id')

    # Query the database to get the product with the specified id
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, rating,image,description FROM product WHERE id = %s", (product_id,))
    product_data = cursor.fetchone()
    cursor.close()

    # Check if the product exists
    if product_data:
        # If the product exists, create a dictionary with the product data
        product = {
            'id': product_data[0],
            'name': product_data[1],
            'price': product_data[2],
            'rating': product_data[3],
            'image': product_data[4],
            'description': product_data[5]
           
            
        }

        # Render the item.html template with the product data
        return render_template('item.html', product=product)
    else:
        # If the product doesn't exist, return a 404 error
        return "Product not found", 404


@app.route('/view/id=1')
def view():
    # Get the 'id' parameter from the request
    loc_id = 2

    # Query the database to get the product with the specified id
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, description, image FROM locations WHERE id = %s", (loc_id,))
    loc_data = cursor.fetchone()
    cursor.close()

    # Check if the product exists
    if loc_data:
        # If the product exists, create a dictionary with the product data
        location = {
            'id': loc_data[0],
            'name': loc_data[1],
            'category': loc_data[2],
            'price': loc_data[3],
            'description': loc_data[4],
            'image': loc_data[5]
            # Add other fields as needed
        }

        # Render the view.html template with the product data
        return render_template('view.html', location=location)
    else:
        # If the product doesn't exist, return a 404 error
        return "Product not found", 404


@app.route("/predict", methods=["POST"])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)


