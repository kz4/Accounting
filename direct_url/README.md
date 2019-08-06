# Multi-thread Downloader of Intangible Assets Forms

### 1. Input file: ```tenk2008after.csv```

The downloader use the ```tenk2008after.csv``` as the index file to locate possible targets pages. Keys used are cik and filename. The filename contains the acc number (18 digits number right before the '.txt')

By combining the the cik and acc number, interactive data page can be directly accessed such as

> https://www.sec.gov/cgi-bin/viewer?action=view&cik='+cik+'&accession_number='+acc+'&xbrl_type=v#

Then, the downloader verify whether the tab button ___Notes to financial statement___ and ___Intangible___ is available. If accessible, goes to the javascript tag to find the form number and generate the direct form url like:

> https://www.sec.gov/Archives/edgar/data/'+cik+'/'+re.sub('-', '', acc)+'/R'+serial+'.htm

Finally use the url to directly download the form page

### 2. Usage of the downloader

prepare the input csv, set the concurrency scale ```size``` and run the code.

### 3. Output file ```tenk2008after_xbrl.csv```

For each item in the input file, I output all relevant keys, and add two new keys. The first one is the url to the intangible assets form and the second one is the downloaded html's file name.

### 4. Known issues

Some items provide xml format forms instead htm which causes access denied when trying to download the htm. Simply change the url with .xml ending can solve this problem.