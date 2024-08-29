# login.py
import sys
import requests
from bs4 import BeautifulSoup

def login_to_ecampus(user, pwd):
    session = requests.Session()
    login_url = 'https://ecampus.psgtech.ac.in/studzone2/'

    try:
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
            'txtusercheck': user,  # Replace with actual username
            'txtpwdcheck': pwd,  # Replace with actual password
            'abcd3': 'Login'
        }

        response = session.post(login_url, data=login_data)
         
        attendance_page_response = session.get("https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx")
        if 'ASP.NET Ajax client-side framework failed to load.' in attendance_page_response.text:
            return "Login failed."
        else:
            return "Login successful!"
        # if ">Welcome to Students Zone!</marquee>" in response.text:
        #     return "Login successful!"
        # else:
        #     return "Login failed."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

if __name__ == "__main__":
    user = sys.argv[1]
    pwd = sys.argv[2]
    print(login_to_ecampus(user, pwd))
