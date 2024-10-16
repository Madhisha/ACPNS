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

def get_attendance_data():
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'
    try:
        session = requests.Session()
        response = session.get(login_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        login_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'txtusercheck': '22z212',
            'txtpwdcheck': 'cheran#212',
            'abcd3': 'Login'
        }

        response = session.post(login_url, data=login_data)
        if "login failed" in response.text.lower():
            # print(f"Login failed for user {user['rollNo']}.")
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
            seating = check_seating(session)

            return attendance_data, seating
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return None

def login(user):
    session = requests.Session()
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'

    try:
        session = requests.Session()
        login_url = 'https://ecampus.psgtech.ac.in/studzone2/'

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
            'txtusercheck': user['rollNo'],  # Replace with actual username
            'txtpwdcheck': user['password'],  # Replace with actual password
            'abcd3': 'Login'
        }

        response = session.post(login_url, data=login_data)

        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
        if 'ASP.NET Ajax client-side framework failed to load.' in attendance_page_response.text:
            return None
        else:
            return session
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

    
def check_timetable(session, user):
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

def get_result_data(session):
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
                    f"Dear Student,\n\nWe are pleased to inform you that your academic results have been published. Your current Cumulative Grade Point Average (CGPA) is: {cgpa}. Please log in to the eCampus portal for detailed information.\n\nShould you require any assistance or have any queries, please do not hesitate to contact us for support.\n\nBest regards,\nNotifii Team", 
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

def mark_update(session, user):
    
    try:
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


users = user_collection.find()
previous_data = list(attendance_collection.find({}, {'_id': 0}))
current_data, seating_arrangement = get_attendance_data()
previous_data = previous_data[0]['attendance_date'] if previous_data else None
print(current_data, previous_data)
if current_data != previous_data and current_data != None:
    attendance_collection.update_one({}, {'$set': {'attendance_date': current_data}})
    attendance_change = True
else:
    attendance_change = False

for user in users:
    if isinstance(user.get('notifications'), dict):
        if user['notifications'].get('attendance', False) and attendance_change:
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email("Attendance Update Notification", 
    "Dear Student,\n\nPlease be informed that there has been an update to your attendance data. We kindly request you to log in to the eCampus portal to review the changes.\n\nIf you have any questions or require further assistance, feel free to contact us.\n\nBest regards,\nnotifii", 
    [recipient_email])
            print(f"Email sent regarding attendance update to {recipient_email}.")
        session = login(user)
        if user['notifications'].get('timetable', False):
            check_timetable(session, user)
        if user['notifications'].get('results', False):
            print(user['rollNo'])
            result_data = get_result_data(session)
            if result_data:
                calculate_cgpa(result_data, user)
        if user['notifications'].get('marks', False):
            mark_update(session, user)
        if user['notifications'].get('seatingArrangement', False) and seating_arrangement:
            recipient_email = user['rollNo'] + "@psgtech.ac.in"
            send_email(
                "Seating Update Notification",
                "Dear Student,\n\nWe are pleased to inform you that the seating allotment has been published. Please log in to the eCampus portal to view your seating arrangement.\n\nIf you have any questions or require further assistance, feel free to contact us.\n\nBest regards,\nNotifii Team",
                [recipient_email]
            )