from flask import Flask, render_template, request,jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import stripe

stripe.api_key = "sk_test_51O9e3JSFzk0D6VrYz2cSozO1Jfmq79bEhR8REPUGD28vbfg0HfnJ4krNnPyNYij2RVXc2gCKShWRbuv8a4bgs6z6004iVVF4T4"  # Test mode
app = Flask(__name__, static_url_path='/static')
app.secret_key = '7388bb75420f83b9b0f0a8b5377dc9cb'

def insert_user_data(data):
    
        try:
            # Configure database connection
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }

            # Connect to the database
            connection = mysql.connector.connect(**db_config)

            # Create a cursor object
            cursor = connection.cursor()

            # Insert data into the table
            insert_query = "INSERT INTO users (full_name, phone, email, password, college_id, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, data)
            
            # Commit the changes and close the cursor and connection
            connection.commit()
            cursor.close()
            connection.close()
            
            return True

        except mysql.connector.Error as e:
            print("Error:", e)
            return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        college_id = request.form['college_id']
        gender = request.form['gender']
        
        hashed_password = generate_password_hash(password)
        
        data = (full_name, phone, email, hashed_password, college_id, gender)
        
        if insert_user_data(data):
            return "User data inserted successfully."
        else:
            return "Failed to insert user data."

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Connect to the database
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            # Fetch the user's hashed password from the database based on the provided email
            select_query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            
            if result:
                hashed_password = result[0]
                if check_password_hash(hashed_password, password):
                    session['email'] = email
                    cursor.close()
                    connection.close()
                    return redirect(url_for('dashboard'))
                else:
                    cursor.close()
                    connection.close()
                    return "Invalid credentials"
            else:
                cursor.close()
                connection.close()
                return "User not found"
        
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return "Database error"

    return render_template('index.html')



@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # Fetch user data from the database based on the email in the session
        email = session['email']

        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_data:
                full_name, phone, college_id, gender = user_data
                return render_template('dashboard.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
            else:
                return "User data not found."

        except mysql.connector.Error as e:
            print("Error:", e)
            return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'email' in session:
        if request.method == 'POST':
            full_name = request.form['full_name']
            phone = request.form['phone']
            college_id = request.form['college_id']
            email = session['email']

            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                update_query = "UPDATE users SET full_name = %s, phone = %s, college_id = %s WHERE email = %s"
                cursor.execute(update_query, (full_name, phone, college_id, email))
                connection.commit()

                cursor.close()
                connection.close()

                return redirect(url_for('dashboard'))

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to update user data."

        else:
            email = session['email']
            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
                cursor.execute(select_query, (email,))
                user_data = cursor.fetchone()

                cursor.close()
                connection.close()

                if user_data:
                    full_name, phone, college_id, gender = user_data
                    return render_template('edit_profile.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
                else:
                    return "User data not found."

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
   
    session.clear()
    return redirect(url_for('index')) 

@app.route('/property_list2')
def property_list2():
    return render_template('property_list2.html')

@app.route('/property_list1')
def property_list1():
    return render_template('property_list1.html')

@app.route('/property_list3')
def property_list3():
    return render_template('property_list3.html')

@app.route('/property_list4')
def property_list4():
    return render_template('property_list4.html')

@app.route('/property_list5')
def property_list5():
    return render_template('property_list5.html')

@app.route('/index_after_login')
def index_after_login():
    return render_template('index_after_login.html')

@app.route('/property_list1_after_login')
def property_list1_after_login():
    return render_template('property_list1_after_login.html')


@app.route('/property_list2_after_login')
def property_list2_after_login():
    return render_template('property_list2_after_login.html')

@app.route('/property_list3_after_login')
def property_list3_after_login():
    return render_template('property_list3_after_login.html')

@app.route('/property_list4_after_login')
def property_list4_after_login():
    return render_template('property_list4_after_login.html')

@app.route('/property_list5_after_login')
def property_list5_after_login():
    return render_template('property_list5_after_login.html')


@app.route('/juice1')
def juice1():
    return render_template('juice1.html')

@app.route('/juice2')
def juice2():
    return render_template('juice2.html')

@app.route('/juice3')
def juice3():
    return render_template('juice3.html')

@app.route('/juice4')
def juice4():
    return render_template('juice4.html')

@app.route('/juice5')
def juice5():
    return render_template('juice5.html')

@app.route('/juice6')
def juice6():
    return render_template('juice6.html')

@app.route('/juice7')
def juice7():
    return render_template('juice7.html')

@app.route('/juice8')
def juice8():
    return render_template('juice8.html')

@app.route('/juice9')
def juice9():
    return render_template('juice9.html')

@app.route('/juice10')
def juice10():
    return render_template('juice10.html')

@app.route('/juice11')
def juice11():
    return render_template('juice11.html')

@app.route('/juice12')
def juice12():
    return render_template('juice12.html')

@app.route('/juice13')
def juice13():
    return render_template('juice13.html')

@app.route('/juice14')
def juice14():
    return render_template('juice14.html')

@app.route('/juice15')
def juice15():
    return render_template('juice15.html')

@app.route('/juice16')
def juice16():
    return render_template('juice16.html')

@app.route('/juice17')
def juice17():
    return render_template('juice17.html')

@app.route('/juice18')
def juice18():
    return render_template('juice18.html')

@app.route('/juice19')
def juice19():
    return render_template('juice19.html')

@app.route('/juice20')
def juice20():
    return render_template('juice20.html')



# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'canteen'  # Replace with your MySQL database name
}

@app.route('/create-rating', methods=['POST'])
def create_rating():
    try:
        email = request.json['email']  # Assuming the email is sent in the JSON request body
        rating_item = "Coconut"  # Hardcoding the rating item for this example
        rating_value = request.json['rating_value']  # Assuming the rating_value is sent in the JSON request body

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve the user ID based on the email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()

        if user_id is None:
            return jsonify({"error": "User not found"}), 404

        # Check if the rating item exists; if not, create it
        cursor.execute("SELECT id FROM ratings WHERE rating_item = %s", (rating_item,))
        rating_id = cursor.fetchone()

        if rating_id is None:
            cursor.execute("INSERT INTO ratings (rating_item) VALUES (%s)", (rating_item,))
            conn.commit()
            rating_id = cursor.lastrowid

        # Check if the user has already rated this item
        cursor.execute("SELECT id FROM user_ratings WHERE user_id = %s AND rating_id = %s", (user_id[0], rating_id))
        existing_rating = cursor.fetchone()

        if existing_rating is None:
            # Insert the rating into the 'user_ratings' table
            insert_query = "INSERT INTO user_ratings (user_id, rating_id, rating_value) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_id[0], rating_id, rating_value))
        else:
            return jsonify({"error": "Rating already given and cannot be changed"}), 400

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Rating created successfully"})

    except mysql.connector.Error as db_error:
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/like', methods=['POST'])
def like_property():
    try:
        email = request.json['email']  # Assuming the email is sent in the JSON request body

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve the user ID based on the email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()

        if user_id is None:
            return jsonify({"error": "User not found"}), 404

        # Implement your logic to handle liking the Coconut property here
        # You can update a 'likes' field in your properties table or create a new 'likes' table

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Property liked successfully"})

    except mysql.connector.Error as db_error:
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/order', methods=['GET', 'POST'])
def order():
    # Handle order submission logic here, such as processing the order form data
    # For now, we'll simply render an order submission template
    return render_template('order.html')


if __name__ == '__main__':
    app.run(debug=True)



