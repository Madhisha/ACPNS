from bs4 import BeautifulSoup
from db import user_collection

def check_seating(session, user):
    try:
        # Get seating page content
        seating_page = session.get("https://ecampus.psgtech.ac.in/studzone2/EpsWfSeating.aspx")
        seating_page_soup = BeautifulSoup(seating_page.content, 'html.parser')
        script_tag = str(seating_page_soup.find('script')).strip()
        expected_script_tag = "<script>alert(' Seating not Allotted  ')</script>"

        # Initialize seating field if it doesn't exist
        if 'seating' not in user:
            user['seating'] = 'not_allotted'
            user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'seating': 'not_allotted'}})

        # Check if seating is allotted
        if script_tag == expected_script_tag or script_tag is None:
            print("Seating not yet allotted.")
            if user['seating'] != 'not_allotted':
                # Update if the seating status was previously different
                user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'seating': 'not_allotted'}})
            return False
        else:
            print("Seating allotted.")
            if user['seating'] == 'allotted':
                print("No change in seating status.")
                return False
            else:
                # Update the seating status in MongoDB if it's newly allotted
                user_collection.update_one({'rollNo': user['rollNo']}, {'$set': {'seating': 'allotted'}})
                return True  # Indicates seating is allotted
    except Exception as e:
        print(f"Error checking seating allotment: {e}")
        return None
