from database import user_collection
from scrapers.calculate_cgpa import calculate_cgpa
from scrapers.check_seating import check_seating
from scrapers.login import login
from scrapers.mark_update import mark_update
from scrapers.send_mail import send_email
from scrapers.get_attendance import get_attendance_data
from scrapers.get_result_data import get_result_data
from scrapers.check_timetable import check_timetable
import time

while True:
    batch_size = 100  # Define the size of each batch
    total_users = user_collection.count_documents({})  # Get the total number of users
    batch_num = 0

    while batch_num * batch_size < total_users:
        # Fetch the next batch of users
        users = user_collection.find({}).skip(batch_num * batch_size).limit(batch_size)
        times = time.strftime("%H:%M:%S", time.localtime())
        send_email("notifii.services@gmail.com", f"Running now at time {times}", 'body')
        for user in users:
            if isinstance(user.get('notifications'), dict) and "24Z" in user['rollNo']:
                session = login(user)
                if user['notifications'].get('attendance', False):
                    get_attendance_data(session, user)
                if user['notifications'].get('timetable', False):
                    check_timetable(session, user)
                if user['notifications'].get('results', False):
                    result_data,table = get_result_data(session)
                    if result_data:
                        calculate_cgpa(result_data, user, table)
                if user['notifications'].get('marks', False):
                    mark_update(session, user)
                if user['notifications'].get('seatingArrangement', False) and check_seating(session, user):
                    roll = user['rollNo'].lower()
                    recipient_email = roll + "@psgtech.ac.in"
                    send_email(recipient_email, "Seating Update Notification", 
                        f"""
                        <html>
                            <body>
                                <p>Dear Student,</p>
                                <p>We are pleased to inform you that the seating allotment has been published.</p>
                                <p>Please log in to the eCampus portal to view your seating arrangement.</p>
                                <p>If you have any questions or require further assistance, feel free to contact us.</p>
                                <p>Best regards,</p>
                                <p>Notifii Team</p>
                            </body>
                        </html>
                        """
                    )

        batch_num += 1  # Move to the next batch

