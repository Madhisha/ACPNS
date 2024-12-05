import scrapy
from scrapy.http import FormRequest

class EcampusSpider(scrapy.Spider):
    name = 'ecampus'
    start_urls = ['https://ecampus.psgtech.ac.in/studzone/Login/ParentLogin']
    rollno = '22Z212'
    mob = '7667705550'
    email = '22z212@psgtech.ac.in'

    def parse(self, response):
        # Extract the form inputs dynamically
        form_data = {}
        for input_tag in response.xpath("//form//input"):
            name = input_tag.xpath("@name").get()
            value = input_tag.xpath("@value").get(default="")
            if name == "rollno":
                value = self.rollno
            elif name == "mob":
                value = self.mob
            if name:
                form_data[name] = value

        # Submit the login form
        yield FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.after_login
        )

    def after_login(self, response):
        # Check if login was successful
        if "Invalid credentials" in response.text:
            self.log("Login failed")
            return

        self.log("Login successful!")

        # Scrape attendance data
        attendance_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
        yield scrapy.Request(attendance_url, callback=self.parse_attendance)

    def parse_attendance(self, response):
        attendance_table = response.xpath("//table[@id='example']").get()
        if attendance_table:
            email_body = f"""
            <html>
                <body>
                    <p>Your attendance data has been updated:</p>
                    {attendance_table}
                    <p>Best regards,</p>
                    <p>Notifii Team</p>
                </body>
            </html>
            """
            self.send_email("Attendance Update", email_body)
        else:
            self.log("No attendance data available.")

        # Scrape timetable data
        timetable_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/TimeTable"
        yield scrapy.Request(timetable_url, callback=self.parse_timetable)

    def parse_timetable(self, response):
        timetable_tables = response.xpath("//table[@class='table table-bordered timetable-table']").getall()
        if timetable_tables:
            table_html = "".join(timetable_tables)
            email_body = f"""
            <html>
                <body>
                    <p>Your timetable has been updated:</p>
                    {table_html}
                    <p>Best regards,</p>
                    <p>Notifii Team</p>
                </body>
            </html>
            """
            self.send_email("Timetable Update", email_body)
        else:
            self.log("No timetable data available.")

    def send_email(self, subject, body):
        import smtplib
        from email.mime.text import MIMEText

        sender_email = "notifii.services@gmail.com"
        password = "evtz vwnw pwpq tanh"

        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = self.email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, self.email, msg.as_string())
                self.log(f"Email successfully sent: {subject}")
        except Exception as e:
            self.log(f"Error sending email: {e}")
