from bs4 import BeautifulSoup
from scrapers.send_mail import send_email
from database import user_collection

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
        roll = user['rollNo'].lower()  # Ensure the roll number is valid
        recipient_email = roll + "@psgtech.ac.in"  # Construct the recipient's email
        subject = "Test Timetable Update Notification"
        body = f"""
        <html>
            <body>
                <p>Dear Student,</p>

                <p>We are pleased to inform you that your test timetable has been published. Please find the details below:</p>

                {html_table}

                <p>Kindly log in to the eCampus portal for more information.</p>

                <p>If you have any questions or require further assistance, feel free to contact us.</p>
                <p>You can modify your notification preferences in the Notifii web application.<br>
                <a href="https://notifii.vercel.app">Notifii Web Application</a></p>

                <p>Best regards,<br>
                Notifii Team</p>
            </body>
        </html>
        """


        # Send email
        send_email(recipient_email, subject, body)


    except Exception as e:
        print(f"Error checking test timetable: {e}")
        return None
