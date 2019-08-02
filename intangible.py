from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from os.path import join

output_dir = 'output'
prefix = 'https://www.sec.gov'
urls = ['https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K&dateb=&owner=exclude&count=40', 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116132&type=10-K&dateb=&owner=exclude&count=40', 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K&dateb=&owner=exclude&count=40']

# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)

def scrap_intangible(url):
    driver.get(url)

    # element is the Notes to Financial Statements link on 
    # the left panel. You have to expand it first
    element = driver.find_element_by_id('menu_cat3')
    element.click()

    # Avoid selenium.common.exceptions.ElementNotVisibleException: Message: element not visible
    time.sleep(2)

    # Clik on the ACQUISITIONS, GOODWILL, AND ACQUIRED INTANGIBLE ASSETS link
    # driver.find_element_by_xpath('//a[@href="javascript:loadReport(12);"]').click();
    try:
        driver.find_element_by_partial_link_text('Intangible').click();
    except Exception:
        try:
            driver.find_element_by_partial_link_text('INTANGIBLE').click();
        except Exception:
            print(url + ' does not have intangible section')
            return None
    
    # Use BeautifulSoup to parse the DOM
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # The whole html is a big table of table, the content is inside its td
    s = soup.find("table").find("table")
    # Company such as coach doesn't follow this format
    # .find('tr', class_='ro').find('td', class_="text")

    return s

def scrap_company(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find(id="seriesDiv").find("table")
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    year_companyLink = {}
    for row in rows:
        cols = row.find_all('td')
        # The first row is the name row and we only want the role
        # with a Interactive Data button
        if not cols or 'Interactive Data' not in cols[1].get_text():
            continue
        # Fourth column is the date with the four char being the year
        # We also want to fetch the second href as the first one is Documents
        year_companyLink[cols[3].text.strip()[:4]] = cols[1].find_all('a')[1]['href']
    print('year_companyLink dict:')
    print(year_companyLink)
    return year_companyLink

def write_file(s, file_name):
    print('Writing file: ' + file_name)
    with open(join(output_dir, file_name), 'wb') as f:
        f.write(s.encode('utf-8'))

def create_output_dir():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def create_file_name(url, year):
    a, b = url.find('cik='), url.find('&accession_number')
    return ''.join(['CIK', url[a+4:b], '_', year, '.html'])

def main():
    create_output_dir()
    for url in urls:
        year_companyLink = scrap_company(url)
        for year, companyLink in year_companyLink.items():
            url = '/'.join(s.strip('/') for s in [prefix, companyLink])
            print('Going to URL: ' + url)
            s = scrap_intangible(url)
            if s:
                write_file(s, create_file_name(url, year))
            else:
                write_file('NA', create_file_name(url, year))
if __name__ == "__main__":
    main()