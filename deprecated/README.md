# Getting intangible data
********************
Note that this method is getting deprecated because 
1. It takes a long time for selenium to go to a page and download 
2. It takes sec page a long time to load
********************
## Prerequisite
Python, Selenium and BeautifulSoup
## Objective
Given a list of company, this scraps the Intangible Assets page from SEC for all the companies.
Tesla for example
1. Go to https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K&dateb=&owner=exclude&count=40
2. Click on each Interactive Data
3. Go to Notes to Financial Statements - Intangible Assets - download the html file
4. The naming convention would be: CIK0001318605_2017, CIK0001318605_2018
## Run
`python intangible.py`
## Example
See output folder for sample html result.