import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re

# MongoDB connection
client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']
user_collection = db['users']
attendance_collection = db['attendance']
result_collection = db['result']

# Email setup
def send_email(subject, body, recipient_list):
    sender_email = "22z212@psgtech.ac.in"
    password = "cheran#212"

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

def check_timetable(session):
    try:
        time_table_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsTestTimetable.aspx")
        time_table_page_soup = BeautifulSoup(time_table_page_response.content, 'html.parser')
        script_tag = str(time_table_page_soup.find('script')).strip()
        expected_script_tag = "<script>alert('Test Time Table Not Yet Published')</script>"
        if expected_script_tag == script_tag or script_tag == None or "skm_highlightTopMenus" in script_tag:
            print("Test timetable not yet published.")
        else:
            print("Test timetable published.")
            return True  # Indicates timetable is published
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
                send_email("Result Update", f"The result has been published. Your CGPA is: {cgpa}", [recipient_email])
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
            send_email("Marks Update", "The marks data has changed.", [user['rollNo'] + "@psgtech.ac.in"])
        else:
            print(f"No new marks for {user['rollNo']}.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user {user['rollNo']}: {http_err}")
    except Exception as e:
        print(f"Error processing result data for {user['rollNo']}: {e}")

# Main Execution
first_user = user_collection.find_one()
attendance_changed = False
timetable_changed = False
seating_changed = False

if first_user and first_user['notifications']:
    session = requests.Session()
    
    # Check attendance for the first user
    current_attendance_data = get_attendance_data(session, first_user)
    if current_attendance_data:
        previous_data = list(attendance_collection.find({}, {'_id': 0}))
        previous_attendance_date = previous_data[0]['attendance_date'] if previous_data else None

        if current_attendance_data != previous_attendance_date:
            attendance_entry = {'attendance_date': current_attendance_data}
            attendance_collection.delete_many({})
            attendance_collection.insert_one(attendance_entry)
            attendance_changed = True

    # Check timetable and seating for the first user
    timetable_changed = check_timetable(session)
    print(timetable_changed)
    seating_changed = check_seating(session)

# If attendance changed, send emails to all users
if attendance_changed:
    users = user_collection.find()
    for user in users:
        if user['notifications']['attendance']:
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Attendance Update", "The attendance data has changed.", [recipient_email])
            print(f"Email sent regarding attendance update to {recipient_email}.")

# For all users, check results and calculate CGPA
users = user_collection.find()
for user in users:
    if user['notifications']['results']:
        print(user['rollNo'])
        result_data = get_result_data(user)
        if result_data:
            calculate_cgpa(result_data, user)
    if user['notifications']['marks']:
        mark_update(user)

if timetable_changed:
    users = user_collection.find()
    for user in users:
        if user['notifications']['timetable']:
            print(user['rollNo'])
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Timetable Update", "The test timetable has been published.", [recipient_email])
            print(f"Email sent regarding timetable update to {recipient_email}.")

if seating_changed:
    users = user_collection.find()
    for user in users:
        if user['notifications']['seatingArrangement']:
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Seating Update", "The seating allotment has been published.", [recipient_email])
            print(f"Email sent regarding seating update to {recipient_email}.")
