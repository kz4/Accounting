import xml.etree.ElementTree as ET 

def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile)
  
    # get root element 
    root = tree.getroot()
    htmls = []
    for child in root.getchildren():
        # level of Rows, we want to identify the Rows
        # tag and go in, there are other tags in this level
        # such as Columns, so we check the tag is 'Rows'
        if child.tag == 'Rows':
            # 'Rows' only contains 'Row'
            for row in child.getchildren():
                for ggchild in row.getchildren():
                    # level of Cells, there are other tags in this level
                    # such as Id, IsAbstractGroupTitle, Level, ElementName 
                    if ggchild.tag == 'Cells':
                        # 'Cells' only contains 'Cell'
                        for cell in ggchild.getchildren():
                            nonNumbericText = cell.find('NonNumbericText')
                            if nonNumbericText.text:
                                htmls.append(nonNumbericText.text)
    return htmls

def main():
    filename = 'R18.xml'
    htmls = parseXML(filename)
    print('There are %d of htmls' % len(htmls))

    # assuming there should be only one html
    # TODO: do we have an example there are multiple 
    # htmls?
    html = open(filename.replace('xml', 'html'), "w")
    html.write(htmls[0])
    html.close()

if __name__ == "__main__": 
    main() 