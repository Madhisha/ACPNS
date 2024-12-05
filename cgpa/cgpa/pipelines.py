# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from email.mime.text import MIMEText
import smtplib

class EmailPipeline:
    def process_item(self, item, spider):
        recipient_email = f"{item['roll_no']}@psgtech.ac.in"
        body = f"""
        <html>
            <body>
                <p>Dear Student,</p>
                <p>Your current semester Grade Point Average (GPA) is: <strong>{item['cgpa']}</strong>.</p>
                {item['result_table']}
            </body>
        </html>
        """
        msg = MIMEText(body, 'html')
        msg['Subject'] = "Results Published"
        msg['From'] = "notifii.services@gmail.com"
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login("notifii.services@gmail.com", "evtz vwnw pwpq tanh")
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
        return item

