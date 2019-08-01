from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=1018724&accession_number=0001018724-19-000004&xbrl_type=v#'

# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(url)

# element is the Notes to Financial Statements link on 
# the left panel. You have to expand it first
element = driver.find_element_by_id('menu_cat3')
element.click()

# Avoid selenium.common.exceptions.ElementNotVisibleException: Message: element not visible
time.sleep(2)

# Clik on the ACQUISITIONS, GOODWILL, AND ACQUIRED INTANGIBLE ASSETS link
driver.find_element_by_xpath('//a[@href="javascript:loadReport(12);"]').click();

# Use BeautifulSoup to parse the DOM
soup = BeautifulSoup(driver.page_source, 'html.parser')

# The whole html is a big table of table, the content is inside its td
s = soup.find("table").find("table").find('tr', class_='ro').find('td', class_="text")

# Intangible Assets is the 6th table inside this td
Primarily_includes = s.findAll('table')[5]

print(Primarily_includes)
