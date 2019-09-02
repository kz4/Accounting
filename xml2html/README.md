# XML to HTMLs
## Objective
Given a single sec xml file, parse the htmls out
## Sample Input
```
R18.xml is an xml that contains a html with only text in it, future work required to parse the text out and save it in an index
https://www.sec.gov/cgi-bin/viewer?action=view&cik=1800&accession_number=0001047469-11-001056&xbrl_type=v#
Original R18.html source:
https://www.sec.gov/Archives/edgar/data/1800/000104746911001056/R18.xml

R13.xml is an xml that contains a html with text and tables in it, future work required to parse the tables out into CSV format
https://www.sec.gov/cgi-bin/viewer?action=view&cik=896159&accession_number=0001193125-11-047473&xbrl_type=v#
Original R13.html source:
https://www.sec.gov/Archives/edgar/data/896159/000119312511047473/R13.xml
```
## Run
`python3 xml2html.py `
## Sample Result
```
R18.html
R13.html
```
## Future work
Refer to Sample Input
## Note
This file does not include the part where we download the xml from sec archives because we assume that xml is already downloaded to the local