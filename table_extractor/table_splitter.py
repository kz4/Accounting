import os
from bs4 import BeautifulSoup 


def table_extractor(html_text):
    soup = BeautifulSoup(html_text,"lxml")
    tables = soup.find_all(lambda tag:tag.name == 'table' and not tag.has_attr('id')) #search the html file with a css selector to find the table tag without the id attributes
    return tables

def package(html_file,tables):
    path = './'+html_file.split('.',1)[0]
    folder = os.path.exists(path)

    if not folder:                   
        os.makedirs(path)    # create a folder that has the same name as the htm file
    else:
        path = path+'_n'
        os.makedirs(path)

    for i,table in enumerate(tables):
        text = '<html><body>'+ str(table) + '</body></html>' # wrap each table with html headers and save them in separate html files
        with open(path+'/'+str(i)+'.htm','wt+') as outfile:
            outfile.write(text)

	

if __name__ == "__main__":
    html_file = 'R9.htm'
    with open(html_file,'rt') as inputfile:
        tables = table_extractor(inputfile.read())
        package(html_file, tables)

