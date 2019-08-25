import pandas as pd
from lxml.html import parse
from pandas.io.parsers import TextParser
import os
import requests
import urllib
import math
import copy
import pandas as pd	
import numpy as np
from bs4 import BeautifulSoup 

# this is for a single table, not complete

class html_tables(object):
    def __init__(self, text):
        self.text      = text
        self.url_soup = BeautifulSoup(self.text)
        
    def read(self):
        self.tables      = []
        self.tables_html = self.url_soup.find_all("table")
        
        # Parse each table
        for n in range(0, len(self.tables_html)):
            # no. of trs in the table
            n_cols = 0
            # no. of max td in the table, depends on the column span
            # Assume there are 24 columns. it could be 24 columns of colspan="1"
            # or 2 columns of colspan="12"
            # or 2 columns of colspan="11" and 2 columns of colspan="1"
            n_rows = 0
            
            for row in self.tables_html[n].find_all("tr"):
                # soup.find_all(["a", "b"])
                # If you pass in a list, Beautiful Soup will allow a string match
                # against any item in that list. This code finds all the <a> tags
                # and all the <b> tags:
                # The TH and TD elements are used for table cells. TH is used for
                # table header cells while TD is used for table data cells
                # it calculates how many columns this row has
                col_tags = row.find_all(["td", "th"])
                # If this row has more than one column, and increment no. of rows
                if len(col_tags) > 0:
                    n_rows += 1
                    if len(col_tags) > n_cols:
                        n_cols = len(col_tags)
            
            # Create dataframe
            df = pd.DataFrame(index = range(0, n_rows), columns = range(0, n_cols))
            
			# Create list to store rowspan values 
            skip_index = [0 for i in range(0, n_cols)]
			
            # Start by iterating over each row in this table
            row_counter = 0
            for row in self.tables_html[n].find_all("tr"):
                # Skip row if it's blank
                if len(row.find_all(["td", "th"])) == 0:
                    next
                else:
                    # Get all cells containing data in this row
                    columns = row.find_all(["td", "th"])
                    col_dim = []
                    row_dim = []
                    col_dim_counter = -1
                    row_dim_counter = -1
                    col_counter = -1
                    this_skip_index = copy.deepcopy(skip_index)
                    
                    for col in columns:
                        
                        # Determine cell dimensions
                        colspan = col.get("colspan")
                        if colspan is None:
                            col_dim.append(1)
                        else:
                            col_dim.append(int(colspan))
                        col_dim_counter += 1
                            
                        rowspan = col.get("rowspan")
                        if rowspan is None:
                            row_dim.append(1)
                        else:
                            row_dim.append(int(rowspan))
                        row_dim_counter += 1
                            
                        # Adjust column counter
                        if col_counter == -1:
                            col_counter = 0  
                        else:
                            col_counter = col_counter + col_dim[col_dim_counter - 1]
                            
                        while skip_index[col_counter] > 0:
                            col_counter += 1

                        # Get cell contents  
                        cell_data = col.get_text()
                        
                        # Insert data into cell
                        df.iat[row_counter, col_counter] = cell_data

                        # Record column skipping index
                        if row_dim[row_dim_counter] > 1:
                            this_skip_index[col_counter] = row_dim[row_dim_counter]
                
                # Adjust row counter 
                row_counter += 1
                
                # Adjust column skipping index
                skip_index = [i - 1 if i > 0 else i for i in this_skip_index]

            df = self.clean(df)

            # Append dataframe to list of tables
            self.tables.append(df)
        
        return(self.tables)

    def clean(self, df):
        # drop rows with any empty rows
        df = df.replace('', np.NaN).dropna(how='all')
        # df.to_csv("ssa2.csv", header = False, index = False)
        
        # drop rows with any empty columns
        df = df.replace('', np.NaN).dropna(axis=1, how='all')
        # df.to_csv("ssa3.csv", header = False, index = False)
        
        # remove empty cols where it is 0, just to be safe,
        # so far havent seen a case that its required
        df = df.replace(to_replace =[0, '0', '', r'^\s*$'],  
                            value =np.NaN)
        df = df.replace({'0':np.nan, 0:np.nan, r'^\s*$':np.nan}).dropna(axis=1, how='all')
        # df.to_csv("ssa4.csv", header = False, index = False)

        # remove something looks similar to space in cols but is not space
        df = df.replace(' ', np.NaN).dropna(axis=1, how='all')
        # df.to_csv("ssa5.csv", header = False, index = False)

        to_remove_and_right_parenthesis_column_indices = set()
        # get number of rows and columns
        rows, cols = df.shape
        for row in range(rows):
            for col in range(cols):
                # negate if it's surrounded by ()
                if str(df.iloc[row, col]).startswith('('):
                    df.iloc[row, col] = float(df.iloc[row, col][1:].replace(',', '')) * (-1)
                # if the left item is $, set the left the $ to that number
                # and then we want to remove this column
                if df.iloc[row, col - 1] == '$':
                    df.iloc[row, col - 1] = df.iloc[row, col]
                    to_remove_and_right_parenthesis_column_indices.add(col)
                # if it's ), remove this column
                if df.iloc[row, col] == ')':
                    to_remove_and_right_parenthesis_column_indices.add(col)

        # df.to_csv("ssa6.csv", header = False, index = False)

        # new columns we wants to save
        new_cols = [col for col in range(cols) if col not in to_remove_and_right_parenthesis_column_indices]

        # reset column index to 0, 1, 2, 3 ...
        # because earlier we have removed a couple columns
        df.columns = range(cols)

        df = df[new_cols].copy()
        df.to_csv("result.csv", header = False, index = False)
        return df

with open('320193_20160924.htm', 'r') as htm:
    ssa = html_tables(htm.read())
    first_table = ssa.read()[0]
    # first_table.to_csv("ssa.csv", header = False, index = False)

# with open('1.htm','r') as htm:
#     parsed = parse(htm.read())
#     doc = parsed.getroot()
#     tables = doc.findall('.//table')
#     table = parse_options_data(tables[0])
#     print('hello')