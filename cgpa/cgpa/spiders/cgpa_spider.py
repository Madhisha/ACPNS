import scrapy
from bs4 import BeautifulSoup
from pymongo import MongoClient
from cgpa.items import CgpaItem
import re
import requests

class EcampusSpider(scrapy.Spider):
    name = "ecampus"
    allowed_domains = ["ecampus.psgtech.ac.in"]

    # MongoDB setup
    MONGO_URI = "mongodb+srv://22z212:TfVGyfVhyjG8hkNJ@cluster0.gbcugd2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(MONGO_URI, connectTimeoutMS=30000, socketTimeoutMS=30000)
    db = client['ecampus']
    user_collection = db['new_users']

    LOGIN_URL = "https://ecampus.psgtech.ac.in/studzone2/"
    RESULTS_URL = "https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_cookies = None

    def start_requests(self):
        # Fetch users from MongoDB
        users = self.user_collection.find()
        for user in users:
            self.logger.info(f"Logging in for user {user['rollNo']}...")
            
            # Perform login using requests
            session = requests.Session()
            response = session.get(self.LOGIN_URL)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract hidden fields
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
            viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

            login_data = {
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstate_generator,
                '__EVENTVALIDATION': event_validation,
                'txtusercheck': user['rollNo'],
                'txtpwdcheck': user['password'],
                'abcd3': 'Login'
            }
            
            login_response = session.post(self.LOGIN_URL, data=login_data)
            if "Parent" not in login_response.text:
                self.logger.error(f"Login failed for user {user['rollNo']}.")
                continue

            self.logger.info(f"Login successful for user {user['rollNo']}.")

            # Save cookies for Scrapy
            self.session_cookies = session.cookies.get_dict()
            yield scrapy.Request(
                url=self.RESULTS_URL,
                cookies=self.session_cookies,
                callback=self.parse_results,
                meta={'user': user}
            )

    import re

def parse_results(self, response):
    user = response.meta['user']
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the result data and final table HTML from the get_result_data function
    result_data, final_table = get_result_data(response.meta['session'])
    if result_data:
        self.logger.info(f"Result data fetched for {user['rollNo']}.")

        # Calculate CGPA using the result data
        calculate_cgpa(result_data, user, final_table)

        # If you need to yield or return any specific item after processing:
        yield CgpaItem(
            roll_no=user['rollNo'],
            result_table=final_table,
            cgpa=user.get('cgpa')  # Ensure 'cgpa' is set in the user data before yielding
        )
    else:
        self.logger.error(f"Failed to fetch result data for {user['rollNo']}.")

