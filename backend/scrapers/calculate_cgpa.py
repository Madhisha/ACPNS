from db import user_collection
import re
from scrapers.send_mail import send_email

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