import requests
from bs4 import BeautifulSoup



url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_India'

page=requests.get(url)

soup=BeautifulSoup(page.content,'html')



soup.find_all('table')
# <table class="wikitable sortable jquery-tablesorter" style="text-align:right;">
# </table>