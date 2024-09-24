from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)  

MONGO_URI = 'mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'  # Replace with your MongoDB Cloud URI
DB_NAME = 'ecampus'  # Replace with your database name
USERS_COLLECTION = 'users'  # Collection name

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]


def login_to_ecampus(user, pwd):
    session = requests.Session()
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


# Register route
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
            "notifications": False,
            "cgpa": None,
            "marks": []
        }
        users_collection.insert_one(new_user)

        return jsonify({"message": "Registration successful!"}), 200

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({"message": "Server error. Please try again later."}), 500


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



if __name__ == "__main__":
    app.run(debug=True, port=5000)
