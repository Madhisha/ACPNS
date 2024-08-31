import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re
import os

# MongoDB connection
client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']  # Use your database name
user_collection = db['users']  # Use your collection name for users
attendance_collection = db['attendance']
result_collection = db['result']

# Email setup
def send_email(subject, body, recipient_list):
    sender_email = "22z212@psgtech.ac.in"
    password = "cheran#212"  # Use environment variable for security

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_list)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your SMTP server details
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_list, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to get current attendance data
def get_attendance_data(user):
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
            'txtusercheck': user['rollNo'],
            'txtpwdcheck': user['password'],
            'abcd3': 'Login'
        }

        response = session.post(login_url, data=login_data)
        if "login failed" in response.text.lower():
            print(f"Login failed for user {user['rollNo']}.")
            return None

        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
        attendance_page_soup = BeautifulSoup(attendance_page_response.content, 'html.parser')

        # Check if attendance is in updating state
        attendance_update = attendance_page_soup.find('span', {'id': 'Message'})

        attendance_data = []
        if not attendance_update:
            attendance_table = attendance_page_soup.find('table', {'id': 'PDGcourpercView'})
            
            headers = [header.text for header in attendance_table.find_all('tr')[0].find_all('td')]
            rows = attendance_table.find_all('tr', {'onmouseover': "javascript:prettyDG_changeBackColor(this, true);"})
            
            for row in rows:
                cells = row.find_all('td')
                row_data = [cell.text.strip() for cell in cells]
                attendance_data.append(dict(zip(headers, row_data)))
        
        test_timetable_data(session)
        seating_allotment_data(session)
        result_data(session,user)
        return attendance_data if attendance_data else None

    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return None

def test_timetable_data(session):
    try:
        time_table_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsTestTimetable.aspx")
        time_table_page_soup = BeautifulSoup(time_table_page_response.content, 'html.parser')
        script_tag = str(time_table_page_soup.find('script')).strip()
        expected_script_tag = "<script>alert('Test Time Table Not Yet Published')</script>"
        if script_tag == expected_script_tag:
            print("Test timetable not yet published.")
        else:
            print("Test timetable published.")
            # Send an email notification
            users = user_collection.find()
            recipient_emails = [user['rollNo'] + "@psgtech.ac.in" for user in users]
            send_email("Test Timetable Update", "The test timetable has been published.", recipient_emails)
    except Exception as e:
        print(f"Error checking test timetable: {e}")

def seating_allotment_data(session):
    try:
        seating_page = session.get("https://ecampus.psgtech.ac.in/studzone2/EpsWfSeating.aspx")
        seating_page_soup = BeautifulSoup(seating_page.content, 'html.parser')
        script_tag = str(seating_page_soup.find('script')).strip()
        expected_script_tag = "<script>alert(' Seating not Allotted  ')</script>"
        if script_tag == expected_script_tag:
            print("Seating not yet allotted.")
        else:
            print("Seating allotted.")
            # Send an email notification
            users = user_collection.find()
            recipient_emails = [user['rollNo'] + "@psgtech.ac.in" for user in users]
            send_email("Seating Allotment Update", "The seating allotment has been published.", recipient_emails)
    except Exception as e:
        print(f"Error checking seating allotment: {e}")

def result_data(session,user):
    try:
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

        # Check if result is new
        previous_data = list(result_collection.find({}, {'_id': 0}))
        if result_data == previous_data:
            print("No changes in result data.")
            return
        result_collection.delete_many({})
        result_collection.insert_many(result_data)

        cal_cgpa(result_data,user)
    except Exception as e:
        print(f"Error processing result data: {e}")

def cal_cgpa(data, user):
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
            print(f"CGPA for {user['rollNo']}: {cgpa}")
            # Update CGPA for the specific user
            user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'cgpa': cgpa}})
            # Send an email notification to the user
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Result Update", f"The result has been published. Your CGPA is: {cgpa}", [recipient_email])
        else:
            print(f"No valid credit data for user {user['rollNo']}.")
    except Exception as e:
        print(f"Error calculating CGPA for user {user['rollNo']}: {e}")

# Main logic
users = user_collection.find()
for user in users:
    current_attendance_data = get_attendance_data(user)
    if current_attendance_data:
        # Check for changes
        previous_data = list(attendance_collection.find({}, {'_id': 0}))

        if current_attendance_data != previous_data:  # Compare current and previous data
            # Store current data
            attendance_collection.delete_many({})  # Clear previous data
            attendance_collection.insert_many(current_attendance_data)
            
            # Send an email notification to the user
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Attendance Update", "The attendance data has changed.", [recipient_email])
            print(f"Email sent regarding attendance update to {recipient_email}.")
        else:
            print(f"No changes in attendance data for user {user['rollNo']}.")
    else:
        print(f"Attendance data not available for user {user['rollNo']}.")
