import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re

# MongoDB connection
client = MongoClient("mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ecampus']  # Use your database name
collection = db['attendance']  # Use your collection name

# Email setup
def send_email(subject, body):
    sender_email = "22z212@psgtech.ac.in"
    receiver_email = ["22z235@psgtech.ac.in", "cheran411@gmail.com", "22z228@psgtech.ac.in"]
    password = "cheran#212"  # Consider using environment variables for security

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your SMTP server details
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# Function to get current attendance data
def get_attendance_data():
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
        'txtusercheck': '22z228',  # Replace with actual username
        'txtpwdcheck': 'hari123',  # Replace with actual password
        'abcd3': 'Login'
    }

    response = session.post(login_url, data=login_data)
    if "login failed" in response.text.lower():
        print("Login failed.")
        return None

    attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
    attendance_page_soup = BeautifulSoup(attendance_page_response.content, 'html.parser')

    #to check if attendance is in updating state
    attendance_update=attendance_page_soup.find('span',{'id':'Message'})
    # print(attendance_update.text)

    attendance_data = []
    if not attendance_update:
        attendance_table = attendance_page_soup.find('table', {'id': 'PDGcourpercView'})
        
        headers = [header.text for header in attendance_table.find_all('tr')[0].find_all('td')]
        rows = attendance_table.find_all('tr', {'onmouseover': "javascript:prettyDG_changeBackColor(this, true);"})
        
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            attendance_data.append(dict(zip(headers, row_data)))

    test_timetable_data(session) # Check for test timetable update
    seating_allotment_data(session) # Check for seating allotment update
    result_data(session) # Check for result update
    return attendance_data if attendance_data else None

def test_timetable_data(session):
    time_table_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsTestTimetable.aspx")
    time_table_page_soup = BeautifulSoup(time_table_page_response.content, 'html.parser')
    script_tag = str(time_table_page_soup.find('script')).strip()
    expected_script_tag = "<script>alert('Test Time Table Not Yet Published')</script>"
    if script_tag == expected_script_tag:
        print("Test timetable not yet published.")
    else:
        print("Test timetable published.")
        # Send an email notification
        send_email("Test Timetable Update", "The test timetable has been published.")
        print("Email sent regarding test timetable update.")
    return

def seating_allotment_data(session):

    seating_page=session.get("https://ecampus.psgtech.ac.in/studzone2/EpsWfSeating.aspx")
    seating_page_soup=BeautifulSoup(seating_page.content,'html.parser')
    script_tag=str(seating_page_soup.find('script')).strip()
    expected_script_tag="<script>alert(' Seating not Allotted  ')</script>"
    if script_tag==expected_script_tag:
        print("Seating not yet allotted.")
    else:
        print("Seating allotted.")
        # Send an email notification
        send_email("Seating Allotment Update", "The seating allotment has been published.")
        print("Email sent regarding seating allotment update.")
    return

def result_data(session):
    result_page=session.get("https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx")
    result_page_soup=BeautifulSoup(result_page.content,'html.parser')

    result_table=result_page_soup.find('table',{'id':'DgResult'})
    result_data = []
    titles=[title.text for title in result_table.find_all('tr')[0].find_all('td')]
    # result_data.append(titles)

    #to get the result data as a proper table

    # df=pd.DataFrame(columns=titles)
    # column_data=result_table.find_all('tr')
    # for row in column_data[1:]:
    #     row_data=row.find_all('td')
    #     data=[rd.text.strip() for rd in row_data]
    #     length=len(df)
    #     df.loc[length]=data
    # print(df)
    
    #to store the result data in mongodb
    # titles = [title.text.strip() for title in result_table.find_all('tr')[0].find_all('td')]

    rows = result_table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        result_data.append(dict(zip(titles, row_data)))

    
    collection=db['result']

    #to check if the result is new
    previous_data = list(collection.find({}, {'_id': 0}))
    if result_data == previous_data:
        print("No changes in result data.")
        return
    collection.delete_many({})
    collection.insert_many(result_data)

    cal_cgpa(result_data)

    # send_email("Result Update", "The result has been published.")


def cal_cgpa(data):
    tot_credit = 0
    for entry in data:
        credit = int(entry['Credit'])
        tot_credit += credit
        # Extract numeric grade using regex
        grade_match = re.search(r'\d+', entry['Grade/Remark'])
        if grade_match:
            grade = int(grade_match.group())
            entry['Credit_Grade_Product'] = credit * grade
        else:
            entry['Credit_Grade_Product'] = 0  # Default value if grade is not found

    tot_credit_grade_product = sum(entry['Credit_Grade_Product'] for entry in data)
    cgpa = tot_credit_grade_product / tot_credit
    print("CGPA:", cgpa)
    send_email("Result Update", f"The result has been published. CGPA: {cgpa}")
    
# Main logic
current_data = get_attendance_data()
if current_data:
    # Check for changes
    previous_data = list(collection.find({}, {'_id': 0}))

    if current_data != previous_data:  # Compare current and previous data
        # Store current data
        collection.delete_many({})  # Clear previous data
        collection.insert_many(current_data)
        
        # Send an email notification
        send_email("Attendance Update", "The attendance data has changed.")
        print("Email sent regarding attendance update.")
    else:
        print("No changes in attendance data.")
else:
    print("Attendance data not available.")
