import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re

client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']
user_collection = db['users']
attendance_collection = db['attendance']
result_collection = db['result']
# Assuming session and user_collection are initialized globally
session = requests.Session()

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

def mark_update(user):
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'
    
    try:
        # Step 1: Get login page
        response = session.get(login_url)
        response.raise_for_status()

        # Step 2: Parse login page and extract necessary form values
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        # Step 3: Prepare login data and perform login
        login_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'txtusercheck': user['rollNo'],
            'txtpwdcheck': user['password'],
            'abcd3': 'Login'
        }

        login_response = session.post(login_url, data=login_data)
        login_response.raise_for_status()

        if "login failed" in login_response.text.lower():
            print(f"Login failed for user {user['rollNo']}.")
            return None

        # Step 4: Access the marks page
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
        stored_marks_string = user.get('marks_string', '')  # Get stored string, default to empty if not found

        if stored_marks_string != all_tables_data_string:
            # If marks are different, update MongoDB with new data
            user_collection.update_one(
                {'rollNo': user['rollNo']},
                {
                    '$set': {
                        'marks_string': all_tables_data_string,  # Store the concatenated string for future comparisons
                    }
                }
            )
            print(f"Updated marks for {user['rollNo']}.")
        else:
            print(f"No new marks for {user['rollNo']}.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user {user['rollNo']}: {http_err}")
    except Exception as e:
        print(f"Error processing result data for {user['rollNo']}: {e}")

# Fetch all users from the collection and update their marks
def update_all_users():
    try:
        users = user_collection.find()
        for user in users:
            mark_update(user)
    except Exception as e:
        print(f"Error updating marks for all users: {e}")

# Call the function to update marks for all users
update_all_users()
