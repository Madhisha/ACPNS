from flask import jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re


client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']
user_collection = db['new_users']
attendance_collection = db['attendance']
result_collection = db['result']
session = requests.Session()

def send_email(recipient_email, subject, body):
    sender_email = "notifii.services@gmail.com"
    password = "evtz vwnw pwpq tanh"

    # Create the MIMEText message object with HTML content
    msg = MIMEText(body, 'html')  # 'html' specifies the format

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_attendance_data(session):
    try:
        # Fetch the attendance page
        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
        soup = BeautifulSoup(attendance_page_response.content, 'html.parser')

        # Find the attendance table
        table = soup.find('table', id='PDGcourpercView')
        if table is None:
            print("Attendance table not found.")
            return

        # Construct the HTML table
        html_table = "<table border='1' cellpadding='5' cellspacing='0'>"
        
        # Extract table headers
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        html_table += "<tr>"
        for header in headers:
            html_table += f"<th>{header}</th>"
        html_table += "</tr>"

        # Extract table rows, skipping the first row (header)
        for row in table.find_all('tr'):
            columns = [col.get_text(strip=True) for col in row.find_all('td')]
            html_table += "<tr>"
            for col in columns:
                html_table += f"<td>{col}</td>"
            html_table += "</tr>"
        
        html_table += "</table>"

        return html_table        
    except requests.RequestException as e:
        print(f"Error fetching the attendance data: {e}")
        return None

    except Exception as e:
        print(f"Error processing attendance data: {e}")
        return None

def login_as_parent(rollNo, password):
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'

    try:
        # Step 1: Access the initial login page
        response = session.get(login_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the necessary form data (__VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION)
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        # Step 2: Simulate the selection of the "Parent" radio button (rdolst_3) with a POST request
        parent_radio_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'rdolst': 'P',  # Selecting "Parent"
            '__EVENTTARGET': 'rdolst$3',  # Trigger the postback for the "Parent" option
            '__EVENTARGUMENT': ''  # Keep this blank as per POST-back behavior
        }

        # Send POST request to select "Parent" option
        post_response = session.post(login_url, data=parent_radio_data)

        # Check if we reached the parent login page
        if 'Parent' not in post_response.text:
            raise ValueError("Failed to reach the parent login page.")

        # Parse the response again to get updated form data
        soup = BeautifulSoup(post_response.content, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        # Step 3: Perform the login as Parent
        login_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'txtusercheck': rollNo,  # This is the 10-digit mobile number as roll number
            'txtpwdcheck': password,  # This is the password (usually mobile number)
            'abcd3': 'Login'
        }

        # Send login request
        response = session.post(login_url, data=login_data)

        # Step 4: Check if login was successful and access the attendance page
        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfStudMenu.aspx")
        if 'ASP.NET Ajax client-side framework failed to load.' in attendance_page_response.text:
            return False
        else:
            return session
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except ValueError as val_err:
        return f"Value error: {val_err}"
    except Exception as err:
        return f"An error occurred: {err}"

def check_timetable(session):
    try:
        # Step 4: Fetch timetable page and parse
        time_table_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsTestTimetable.aspx")
        time_table_page_soup = BeautifulSoup(time_table_page_response.content, 'html.parser')
        
        # Step 5: Find and extract the table data
        table = time_table_page_soup.find('table', {'id': 'DgResult'})
        if table is None:
            print("Test timetable not found.")
            return
        
        # Construct the HTML table
        html_table = "<table border='1' cellpadding='5' cellspacing='0'>"
        
        # Extract table headers
        headers = [header.text.strip() for header in table.find_all('tr')[0].find_all('td')]
        html_table += "<tr>"
        for header in headers:
            html_table += f"<th>{header}</th>"
        html_table += "</tr>"

        # Extract table rows
        for row in table.find_all('tr')[1:]:
            columns = [col.text.strip() for col in row.find_all('td')]
            html_table += "<tr>"
            for col in columns:
                html_table += f"<td>{col}</td>"
            html_table += "</tr>"
        
        html_table += "</table>"
        return html_table

    except Exception as e:
        print(f"Error checking test timetable: {e}")
        return None
def register(rollNo, password):

    try:
        # Check if the user already exists in the database
        existing_user = user_collection.find_one({"rollNo": rollNo})
        if existing_user:
            # return jsonify({"message": "User already registered."}), 409
            print(f"User {rollNo} already registered.")
            return

        # Attempt to login to eCampus with provided credentials
        session = login_as_parent(rollNo, password)
        if not session:
            # return jsonify({"message": "Login failed. Invalid credentials."}), 401
            print(f"Login failed for user {rollNo}. Invalid credentials.")
            return

        # If login successful, save the user to the database
        new_user = {
            "rollNo": rollNo,
            "password": password,
            "notifications": {
                "attendance": True,
                "marks": True,
                "timetable": True,
                "seatingArrangement": True,
                "results": False,
            },
            "cgpa": None,
            "timetable": None,
            
        }

        # Fetch results and update the user data
        result, table = get_result_data(session)
        new_user['cgpa'] = calculate_cgpa(result)
        new_user['marks'] = mark_update(session)
        new_user['timetable'] = check_timetable(session)
        new_user['result_table'] = table
        new_user['attendance'] = get_attendance_data(session)

        # Save new user data to MongoDB
        user_collection.insert_one(new_user)
        subject = "Introducing NOTIFII: Stay Updated with Real-Time College Notifications"
        body = f"""
        <html>
        <body>
            <p>Dear Student,</p>
            <p>We are excited to announce the launch of <strong>NOTIFII</strong>, our new Automated College Portal Notification System. With NOTIFII, you’ll always stay informed about important academic updates directly to your email, so you never miss out on crucial information.</p>
            <p>Here’s what NOTIFII will do for you:</p>
            <ul>
            <li><strong>Real-Time Notifications:</strong> Receive instant notifications for critical updates, including:
                <ul>
                <li>Exam schedules</li>
                <li>Timetable releases</li>
                <li>Grade releases, along with your CGPA calculation</li>
                <li>Continuous Assessment (CA) marks</li>
                <li>Attendance status</li>
                <li>Seating arrangements</li>
                </ul>
            </li>
            <p> By default result notification is disabled. If you want to enable it, please update your preferences in your profile.</p>
            <li><strong>Automated Monitoring:</strong> NOTIFII automatically checks the college portal for any new updates, eliminating the need for manual checking, so you can focus on your academics.</li>
            <li><strong>Customizable Preferences:</strong> You can tailor which notifications you want to receive and easily manage your preferences through a user-friendly interface.</li>
            <li><strong>Efficient Communication:</strong> NOTIFII ensures timely and accurate updates on important academic events, helping you stay organized and prepared.</li>
            </ul>
            <p>To begin receiving notifications, please ensure that you have registered and updated your preferences through your profile.</p>
            <p>We hope that NOTIFII enhances your academic experience by providing timely updates and streamlining communication.</p>
            <p>Best regards,<br>Notifii team, PSG Tech</p>
            <p><a href="https://notifii.vercel.app">notifii website</a></p>
            <p>If you have any queries, feel free to contact us at <a href="mailto:22z212@psgtech.ac.in">22z212@psgtech.ac.in</a>.</p>
        </body>
        </html>
        """
        send_email(subject, body, f"{rollNo}@psgtech.ac.in")

        print(f"User {rollNo} registered successfully.")    

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        # return jsonify({"message": "Server error. Please try again later."}), 500
        print(f"Server error. Please try again later.")

# Email setup
def send_email(subject, body, recipient):
    sender_email = "notifii.services@gmail.com"
    password = "evtz vwnw pwpq tanh"

    msg = MIMEText(body, 'html')
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
    try:
        result_page = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx")
        result_page_soup = BeautifulSoup(result_page.content, 'html.parser')

        result_table = result_page_soup.find('table', {'id': 'DgResult'})
        result_data = []
        titles = [title.text for title in result_table.find_all('tr')[0].find_all('td')]

        final_table = str(result_table)


        rows = result_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            result_data.append(dict(zip(titles, row_data)))

        return result_data, final_table
    except Exception as e:
        print(f"Error processing result data: {e}")
        return None
    
def calculate_cgpa(data):
    try:
        tot_credit = 0
        credit_grade_product = 0

        # Calculate total credits and grade-credit product
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
            return cgpa
        else:
            print(f"No valid credit data for user.")
    except Exception as e:
        print(f"Error calculating CGPA for user: {e}")

    

def mark_update(session):
    try:
        # Step 4: Access the marks page
        marks_page_url = "https://ecampus.psgtech.ac.in/studzone2/CAMarks_View.aspx"
        marks_page = session.get(marks_page_url)
        marks_page.raise_for_status()

        marks_page_soup = BeautifulSoup(marks_page.content, 'html.parser')

        # Step 5: Iterate over all tables on the page
        regex_pattern = re.compile(r'^8')  # Regular expression for IDs starting with '8'
        all_tables = marks_page_soup.find_all('table', id=regex_pattern)  # Find all tables
        all_tables_html = ""  # String to store concatenated HTML for all tables

        for table in all_tables:
            # Append each table's HTML representation to the combined HTML string
            all_tables_html += str(table) + "<br>"  # Adding a line break between tables for readability

        # Step 6: Check for changes in marks
        return all_tables_html

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user")
    except Exception as e:
        print(f"Error processing result data for : {e}")


# Usage
data = [
    ("22Z304","9500915353")
]


for rollNo, password in data:
    register(rollNo, password)
    