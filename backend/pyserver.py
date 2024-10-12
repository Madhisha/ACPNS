from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re


app = Flask(__name__)
CORS(app, supports_credentials=True)  

MONGO_URI = 'mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'  # Replace with your MongoDB Cloud URI
DB_NAME = 'ecampus'  # Replace with your database name
USERS_COLLECTION = 'users'  # Collection name

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]
session = requests.Session()


def login_to_ecampus(user, pwd):
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'

    try:
        # Perform login
        response = session.get(login_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        login_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'txtusercheck': user,  # Replace with actual username
            'txtpwdcheck': pwd,  # Replace with actual password
            'abcd3': 'Login'
        }

        response = session.post(login_url, data=login_data)
        
        # Check if login was successful by attempting to fetch the attendance page
        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
        if 'ASP.NET Ajax client-side framework failed to load.' in attendance_page_response.text:
            return False
        else:
            return True

    except requests.exceptions.HTTPError as http_err:
        return False
    except Exception as err:
        return False
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    rollNo = data.get('rollNo')
    password = data.get('password')

    try:
        # Check if the user already exists in the database
        existing_user = users_collection.find_one({"rollNo": rollNo})
        if existing_user:
            return jsonify({"message": "User already registered."}), 409

        # Attempt to login to eCampus with provided credentials
        login_successful = login_to_ecampus(rollNo, password)
        if not login_successful:
            return jsonify({"message": "Login failed. Invalid credentials."}), 401

        # If login successful, save the user to the database
        new_user = {
            "rollNo": rollNo,
            "password": password,
            "notifications": {
                "attendance": False,
                "marks": False,
                "timetable": False,
                "seatingArrangement": False,
                "results": False
            },
            "cgpa": None
        }

        # Fetch results and update the user data
        result = get_result_data(session)
        new_user['cgpa'] = calculate_cgpa(result)
        new_user['marks'] = mark_update(session)

        # Save new user data to MongoDB
        users_collection.insert_one(new_user)
        send_email("Registration Successful", "You have successfully registered for eCampus notifications.", f"{rollNo}@psgtech.ac.in")
        return jsonify({"message": "Registration successful!"}), 200

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({"message": "Server error. Please try again later."}), 500

# Email setup
def send_email(subject, body, recipient):
    sender_email = "22zz212@psgtech.ac.in"
    password = "evtz vwnw pwpq tanh"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


def get_result_data(session):
    result_page = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx")
    result_page_soup = BeautifulSoup(result_page.content, 'html.parser')

    result_table = result_page_soup.find('table', {'id': 'DgResult'})
    result_data = []
    titles = [title.text for title in result_table.find_all('tr')[0].find_all('td')]

    rows = result_table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        result_data.append(dict(zip(titles, row_data)))

    return result_data


def calculate_cgpa(data):
    try:
        tot_credit = 0
        credit_grade_product = 0
        for entry in data:
            credit = int(entry['Credit'])
            tot_credit += credit
            # Extract numeric grade using regex
            grade_match = re.search(r'\d+', entry['Grade/Remark'])
            if grade_match:
                grade = int(grade_match.group())
                credit_grade_product += credit * grade

        if tot_credit > 0:
            cgpa = credit_grade_product / tot_credit
            print(f"CGPA : {cgpa}")
            return cgpa
        else:
            print(f"No valid credit data for user.")
    except Exception as e:
        print(f"Error calculating CGPA for user: {e}")
    
def extract_table_data_as_string(table):
    """Extract data from the table and return it as a concatenated string for comparison."""
    table_data = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        if cells:
            # Concatenate all cell values in the row to form a string
            row_data = " ".join(cell.text.strip() for cell in cells)
            table_data.append(row_data)
    # Return the concatenated string for the whole table
    return " | ".join(table_data)

def mark_update(session):
    
    marks_page_url = "https://ecampus.psgtech.ac.in/studzone2/CAMarks_View.aspx"
    marks_page = session.get(marks_page_url)
    marks_page.raise_for_status()

    marks_page_soup = BeautifulSoup(marks_page.content, 'html.parser')

    # Step 5: Iterate over all tables on the page
    regex_pattern = re.compile(r'^8')  # Regular expression for IDs starting with '8'
    all_tables = marks_page_soup.find_all('table', id=regex_pattern)  # Find all tables
    all_tables_data_string = ""  # String to store concatenated data from all tables

    for table in all_tables:
        # Extract and append data from each table
        table_data_string = extract_table_data_as_string(table)
        all_tables_data_string += table_data_string + " || "  # Delimiter for each table

    # Step 6: Check for changes in marks
    return all_tables_data_string

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    rollNo = data.get('rollNo')
    password = data.get('password')

    try:
        user = users_collection.find_one({"rollNo": rollNo, "password": password})

        if user:
            # Convert ObjectId to string for JSON serialization
            user['_id'] = str(user['_id'])
            return jsonify(user)  # Return the user object

        return jsonify({"message": "Invalid credentials. Please try again."}), 401

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({"message": "Server error. Please try again later."}), 500


# Profile fetching route
@app.route('/profile', methods=['GET'])
def profile():
    rollNo = request.args.get('rollNo')

    try:
        user = users_collection.find_one({"rollNo": rollNo})

        if user:
            # Convert ObjectId to string for JSON serialization
            user['_id'] = str(user['_id'])
            return jsonify(user)

        return jsonify({"message": "User not found."}), 404

    except Exception as e:
        print(f"Error fetching profile: {str(e)}")
        return jsonify({"message": "Server error. Please try again later."}), 500


# Update notification preferences
@app.route('/notifications', methods=['POST'])
def update_notifications():
    data = request.get_json()
    rollNo = data.get('rollNo')
    notifications = data.get('notifications')

    try:
        result = users_collection.update_one({"rollNo": rollNo}, {"$set": {"notifications": notifications}})

        # Check how many documents were matched and updated
        if result.matched_count > 0:
            return jsonify({"message": "Notification preference updated successfully!"})
        else:
            return jsonify({"message": "User not found."}), 404

    except Exception as e:
        print(f"Error updating notifications: {str(e)}")
        return jsonify({"message": "Server error. Please try again later."}), 500

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Setup your email server settings
    smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
    smtp_port = 587  # Usually 587 for TLS
    smtp_user = '22zz212@psgtech.ac.in'  # Replace with your email
    smtp_password = 'evtz vwnw pwpq tanh'  # Replace with your email password

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = '22z235@psgtech.ac.in'
    msg['Subject'] = f'Message from {name}'

    # Email body
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Use TLS
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)