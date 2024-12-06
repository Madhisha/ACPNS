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
    
