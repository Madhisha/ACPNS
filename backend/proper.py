from time import sleep
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re
import bcrypt

# MongoDB connection
client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']
user_collection = db['users']
attendance_collection = db['attendance']
result_collection = db['result']

# Email setup
def send_email(subject, body, recipient_list):
    sender_email = "notifii.services@gmail.com"
    password = "evtz vwnw pwpq tanh"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_list)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_list, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

def get_attendance_data(session, user):
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'
    try:
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

        attendance_table = attendance_page_soup.find('table', {'id': 'PDGcourpercView'})
        headers = [header.text.strip() for header in attendance_table.find_all('tr')[0].find_all('td')]
        rows = attendance_table.find_all('tr', {'onmouseover': "javascript:prettyDG_changeBackColor(this, true);"})

        if rows:
            first_row = rows[0]
            cells = first_row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            date_index = headers.index('ATTENDANCE PERCENTAGE TO')
            attendance_data = row_data[date_index]

            return attendance_data
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return None

def check_timetable(user):
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
            print(f"Login failed for user.")
            return None
        
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
        if html_table == user.get('timetable', None):
            print("No change in timetable.")
            return False
        user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'timetable': html_table}})

        # Send email with the HTML table
        recipient_email = user['rollNo'] + "@psgtech.ac.in"  # Replace with the actual recipient's email
        subject = "Test Timetable Update Notification"
        body = f"""
        Dear Student,

        We are pleased to inform you that your test timetable has been published. Please find the details below:

        {html_table}

        Kindly log in to the eCampus portal for more information.

        If you have any questions or require further assistance, feel free to contact us.

        Best regards,
        Notifii Team
        """
        # Corrected function call
        send_email([recipient_email], subject, body)

    except Exception as e:
        print(f"Error checking test timetable: {e}")
        return None


def check_seating(session):
    try:
        seating_page = session.get("https://ecampus.psgtech.ac.in/studzone2/EpsWfSeating.aspx")
        seating_page_soup = BeautifulSoup(seating_page.content, 'html.parser')
        script_tag = str(seating_page_soup.find('script')).strip()
        expected_script_tag = "<script>alert(' Seating not Allotted  ')</script>"
        if script_tag == expected_script_tag or script_tag == None:
            print("Seating not yet allotted.")
        else:
            print("Seating allotted.")
            return True  # Indicates seating is allotted
    except Exception as e:
        print(f"Error checking seating allotment: {e}")
        return None

def get_result_data(user):
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'
    try:
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
    except Exception as e:
        print(f"Error processing result data: {e}")
        return None

def calculate_cgpa(data, user):
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
            previous_cgpa = user.get('cgpa', None)

            if previous_cgpa is None or cgpa != previous_cgpa:
                user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'cgpa': cgpa}})
                recipient_email = user['rollNo'] + "@psgtech.ac.in"
                send_email("Result Update Notification", 
                    f"Dear Student,\n\nWe are pleased to inform you that your results have been published. Your current CGPA is: {cgpa}. Please log in to the eCampus portal for detailed information.\n\nShould you require any assistance, feel free to reach us for support.\n\nBest regards,\nNotifii Team", 
                    [recipient_email])
            else:
                print(f"No change in CGPA for {user['rollNo']}. No email sent.")
        else:
            print(f"No valid credit data for user {user['rollNo']}.")
    except Exception as e:
        print(f"Error calculating CGPA for user {user['rollNo']}: {e}")
    
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
            send_email("Marks Update Notification", 
           "Dear Student,\n\nWe wish to inform you that your marks have been updated. Please log in to the eCampus portal to review the changes.\n\nIf you need any assistance, feel free to reach out to us for support.\n\nBest regards,\nNotifii Team", 
           [user['rollNo'] + "@psgtech.ac.in"])

        else:
            print(f"No new marks for {user['rollNo']}.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user {user['rollNo']}: {http_err}")
    except Exception as e:
        print(f"Error processing result data for {user['rollNo']}: {e}")

# Main Execution
first_user = user_collection.find_one()
attendance_changed = False

seating_changed = False

if first_user and first_user['notifications']:
    session = requests.Session()
    
    # Check attendance for the first user
    current_attendance_data = get_attendance_data(session, first_user)
    print(current_attendance_data)
    if current_attendance_data:
        previous_data = list(attendance_collection.find({}, {'_id': 0}))
        previous_attendance_date = previous_data[0]['attendance_date'] if previous_data else None

        if current_attendance_data != previous_attendance_date:
            attendance_entry = {'attendance_date': current_attendance_data}
            attendance_collection.delete_many({})
            attendance_collection.insert_one(attendance_entry)
            attendance_changed = True


# If attendance changed, send emails to all users
if attendance_changed:
    users = user_collection.find()
    for user in users:
        # Check if 'notifications' is a dictionary
        if isinstance(user.get('notifications'), dict):
            if user['notifications'].get('attendance', False):
                recipient_email = user['rollNo'] + "@psgtech.ac.in"
                send_email("Attendance Update Notification", 
        "Dear Student,\n\nPlease be informed that there has been an update to your attendance data. We kindly request you to log in to the eCampus portal to review the changes.\n\nIf you have any questions or require further assistance, feel free to contact us.\n\nBest regards,\nnotifii", 
        [recipient_email])
                print(f"Email sent regarding attendance update to {recipient_email}.")
            if user['notifications'].get('timetable', False):
                check_timetable(user)
        else:
            print(f"Skipping user {user['rollNo']}: 'notifications' is not properly structured.")

# For all users, check results and calculate CGPA
users = user_collection.find()
for user in users:
    if isinstance(user.get('notifications'), dict):
        if user['notifications'].get('results', False):
            print(user['rollNo'])
            result_data = get_result_data(user)
            if result_data:
                calculate_cgpa(result_data, user)
        if user['notifications'].get('marks', False):
            mark_update(user)
        if user['notifications'].get('test_timetable', False):
            check_timetable(user)
    else:
        print(f"Skipping user {user['rollNo']}: 'notifications' is not properly structured.")

for user in users:
    if isinstance(user.get('notifications'), dict):
        if user['notifications'].get('test_timetable', False):
            check_timetable(user)
if seating_changed:
    users = user_collection.find()
    for user in users:
        if isinstance(user.get('notifications'), dict):
            if user['notifications'].get('seatingArrangement', False):
                recipient_email = user['rollNo'] + "@psgtech.ac.in"
                send_email("Seating Update", "The seating allotment has been published.", [recipient_email])
                print(f"Email sent regarding seating update to {recipient_email}.")
        else:
            print(f"Skipping user {user['rollNo']}: 'notifications' is not properly structured.")
        
