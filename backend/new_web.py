import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

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


def login_to_ecampus(rollno, mob):
    """
    Logs in to the eCampus website using the provided roll number and mobile number.
    :param rollno: str, Roll number to use for login
    :param mob: str, Mobile number (password) to use for login
    :return: session object if login successful, else (False, error message)
    """
    # URL of the login page
    url = "https://ecampus.psgtech.ac.in/studzone/Login/ParentLogin"
    session = requests.Session()

    # Get the login page content
    response = session.get(url)
    if not response.ok:
        return False, f"Failed to fetch login page. HTTP Status Code: {response.status_code}"

    # Parse the HTML
    login_soup = BeautifulSoup(response.content, "html.parser")

    # Find the form element
    form = login_soup.find("form", {"class": "form__content"})  # Adjust class if necessary

    if not form:
        return False, "Login form not found on the page!"

    # Extract all form inputs
    inputs = form.find_all("input")
    payload = {}
    
    for input_tag in inputs:
        input_name = input_tag.get("name")
        input_value = input_tag.get("value", "")
        
        # Fill in the form with your credentials
        if input_name == "rollno":
            input_value = rollno  # Use the provided roll number
        elif input_name == "mob":
            input_value = mob  # Use the provided mobile number (password)
            
        # Add to payload
        if input_name:  # Ignore inputs without a name attribute
            payload[input_name] = input_value

    # Handle hidden inputs (e.g., verification tokens)
    hidden_inputs = form.find_all("input", {"type": "hidden"})
    for hidden_input in hidden_inputs:
        hidden_name = hidden_input.get("name")
        hidden_value = hidden_input.get("value", "")
        if hidden_name:
            payload[hidden_name] = hidden_value

    # Extract the form action URL
    action = form.get("action")
    login_url = requests.compat.urljoin(url, action)

    # Submit the form
    login_response = session.post(login_url, data=payload)
    
    # Check the login response
    if login_response.ok:
        return session  # Login successful
    else:
        return False, f"Login failed. HTTP Status Code: {login_response.status_code}"

def mark_update(session):
    try:
        # Step 4: Access the marks page
        marks_page_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CAMarksView"
        marks_page = session.get(marks_page_url)
        marks_page.raise_for_status()

        marks_page_soup = BeautifulSoup(marks_page.content, 'html.parser')

        # Find all tables
        all_tables = marks_page_soup.find_all('table', class_="table table-bordered table-striped")
        all_tables_html = ""  # String to store concatenated HTML for all tables

        for table in all_tables:
            # Add inline CSS styles to the table
            styled_table = str(table).replace(
                '<table',
                '<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;"'
            ).replace(
                '<th',
                '<th style="background-color: #5b2a6e; color: white; padding: 8px; text-align: left;"'
            ).replace(
                '<td',
                '<td style="border: 1px solid #ddd; padding: 8px;"'
            )
            # Append the styled table's HTML
            all_tables_html += styled_table + "<br>"

        # Step 6: Check for changes in marks (if necessary)

        recipient_email = '22z212@psgtech.ac.in'
        send_email(
            recipient_email,
            "Marks Update Notification",
            f"""
            <html>
                <body>
                    <p>Dear Student,</p>
                    <p>We wish to inform you that your marks have been updated. Please see the details below:</p>
                    {all_tables_html} 
                    <p>Please log in to the eCampus portal to review the changes in detail.</p>
                    <p>If you need any assistance, feel free to reach out to us for support.</p>
                    <p>Best regards,</p>
                    <p>Notifii Team</p>
                </body>
            </html>
            """
        )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user")
    except Exception as e:
        print(f"Error processing result data: {e}")


def class_Timetable(session):
    try:
        # Step 4: Access the timetable page
        timetable_page_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/TimeTable"
        timetable_page = session.get(timetable_page_url)
        timetable_soup = BeautifulSoup(timetable_page.content, 'html.parser')
        all_tables = timetable_soup.find_all('table', class_="table table-bordered timetable-table")
        
        # Initialize the string to accumulate styled tables
        table_html = ""
        
        for table_tag in all_tables:
            # Convert the Tag object to a string before processing
            table_str = str(table_tag)
            
            # Add inline CSS styles to the table
            styled_table = table_str.replace(
                '<table',
                '<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;"'
            ).replace(
                '<th',
                '<th style="background-color: #5b2a6e; color: white; padding: 8px; text-align: left;"'
            ).replace(
                '<td',
                '<td style="border: 1px solid #ddd; padding: 8px;"'
            )
            
            # Append the styled table's HTML
            table_html += styled_table + "<br>"
        
        send_email(
            "22z212@psgtech.ac.in",
            "Timetable Update Notification",
            f"""
            <html>
                <body>
                    <p>Dear Student,</p>
                    <p>We wish to inform you that your timetable has been updated. Please see the details below:</p>
                    {table_html}
                    <p>Please log in to the eCampus portal to review the changes in detail.</p>
                    <p>If you need any assistance, feel free to reach out to us for support.</p>
                    <p>Best regards,</p>
                    <p>Notifii Team</p>
                </body>
            </html>
            """
        )
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for user: {http_err}")


# Login details
rollno = "22Z212"  # Replace with actual roll number
mob = "7667705550"  # Replace with actual mobile number (password)

# Login to the portal
session = login_to_ecampus(rollno, mob)
if isinstance(session, requests.Session):
    print("Login successful!")
    
    # Fetch attendance data
    response = session.get("https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage")
    attendance_soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the attendance table
    attendance_table = attendance_soup.find('table', id="example")
    if attendance_table:
        table_html = str(attendance_table)  # Extract the raw HTML of the table
    else:
        table_html = "<p>No attendance data available.</p>"

    # Prepare the email body
    body = f"""
        <html>
            <body>
                <p>We hope this email finds you well.</p>
                <p>Please note that your attendance data has been updated. The latest details are provided below:</p>
                {table_html}
                <p>Kindly review the updated attendance on the portal.</p>
                <p>You can modify your notification preferences in the Notifii web application.<br>
                <a href="https://notifii.vercel.app">Notifii Web Application</a></p>
                <p>Best regards,</p>
                <p>Notifii Team</p>
            </body>
        </html>
    """

    # Send email
    recipient_email = f"{rollno.lower()}@psgtech.ac.in"
    send_email(recipient_email, "Attendance Update", body)
    print("Attendance update email sent!")
else:
    print(f"Login failed: {session}")

# mark_update(session)
class_Timetable(session)