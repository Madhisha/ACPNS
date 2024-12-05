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

def login(user):
    session = requests.Session()
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
            'txtusercheck': user['rollNo'],  # This is the 10-digit mobile number as roll number
            'txtpwdcheck': user['password'],  # This is the password (usually mobile number)
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
    
def calculate_cgpa(data, user, table):
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
            print(f"CGPA for {user['rollNo']}: {cgpa}")
            previous_cgpa = user.get('cgpa', None)
            result_table = user.get('result_table', None)  # Use .get() to avoid KeyError

            # Update CGPA and send email only if result_table changes
            if result_table != table:
                user_collection.update_one(
                    {'rollNo': user['rollNo']},
                    {'$set': {'cgpa': cgpa, 'result_table': table}}
                )
                roll = user['rollNo'].lower()  # Ensure the roll number is valid
                recipient_email = roll + "@psgtech.ac.in"
                send_email(
                    recipient_email,
                    "Test Mail!!!!",
                    f"""
                    <html>
                        <body>
                            <p>Dear Student,</p>

                            <p>We are excited to inform you that your academic results have been published.</p>

                            {table}
                            <p>Your current semester Grade Point Average (GPA) is: <strong>{cgpa}</strong>.</p>

                            <p>Please log in to the eCampus portal for detailed information.</p>

                            <p>Should you require any assistance or have any queries, please do not hesitate to contact us for support.</p>

                            <p>Best regards,</p>
                            <p>Notifii Team</p>
                        </body>
                    </html>
                    """
                )
            else:
                print(f"No change in CGPA for {user['rollNo']}. No email sent.")
        else:
            print(f"No valid credit data for user {user['rollNo']}.")
    except Exception as e:
        print(f"Error calculating CGPA for user {user['rollNo']}: {e}")



batch_size = 100  # Define the size of each batch
total_users = user_collection.count_documents({})  # Get the total number of users
batch_num = 0

while batch_num * batch_size < total_users:
    # Fetch the next batch of users
    users = user_collection.find({}).skip(batch_num * batch_size).limit(batch_size)

    for user in users:
        if isinstance(user.get('notifications'), dict) and "24Z" not in user['rollNo']:
            session = login(user)
            result_data, table = get_result_data(session)
            if result_data:
                calculate_cgpa(result_data, user, table)
            # if user['notifications'].get('marks', False):
            #     mark_update(session, user)
            # if user['notifications'].get('seatingArrangement', False) and check_seating(session, user):
            #     roll = user['rollNo'].lower()
            #     recipient_email = roll + "@psgtech.ac.in"
            #     send_email(recipient_email, "Seating Update Notification", 
            #         f"""
            #         <html>
            #             <body>
            #                 <p>Dear Student,</p>
            #                 <p>We are pleased to inform you that the seating allotment has been published.</p>
            #                 <p>Please log in to the eCampus portal to view your seating arrangement.</p>
            #                 <p>If you have any questions or require further assistance, feel free to contact us.</p>
            #                 <p>Best regards,</p>
            #                 <p>Notifii Team</p>
            #             </body>
            #         </html>
            #         """
            #     )

    batch_num += 1  # Move to the next batch

# Schedule the job to run every day at a specific time
# schedule.every(1).minutes.do(scripts)

# # Keep the script running to execute scheduled jobs
# while True:
#     schedule.run_pending()
#     time.sleep(1)