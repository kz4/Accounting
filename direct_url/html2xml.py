import os
import csv
import re
import shutil
import urllib3
import multiprocessing
import csv
import time

# thread pool size
size = 32 

urllib3.disable_warnings()

# set socket pool
http = urllib3.PoolManager(size)

# folder where xml files are downloaded to
path = 'xml'

def get_all_files(dir):
    """
    Returns all file that's less than 1kb, which should be xml instead
    """
    # get all current dir file names
    file_names = [f for f in os.listdir(dir)]
    # # get current file name absolute path
    # file = [os.path.join(os.path.join(os.path.abspath('.'), dir), f) for f in file_names]
    # # print(file)
    # return file
    # print(file_names)
    return sorted(file for file in file_names if os.path.getsize(os.path.join(dir, file)) < 1000)

def extract_xml(files):
    """
    Returns a dict of file_name and its URL that should be xml
    """
    with open('tenk2008after_xbrl.csv', 'rt') as f:
        csvReader = csv.reader(f, delimiter=",")
        csvData = list(csvReader)
        # every line is a list of two tuples
        # e.g.  
        # "('788920', '0001003297-10-000227', 'PRO DEX INC', '10-K', '28SEP2010', '2010')","('no Financial Statements', './htm/None')"
        # "('80424', '0001193125-10-188769', 'PROCTER & GAMBLE CO', '10-K', '13AUG2010', '2010')","('https://www.sec.gov/Archives/edgar/data/80424/000119312510188769/R9.htm', './htm//80424_0001193125-10-188769.html')"
        # 9: " './htm//"
        # -2: "')"
        file_url = {line[1].split(',')[1][9:-2]: line[1].split(',')[0][2:-1] for line in csvData if line[1] != "('no Financial Statements', './htm/None')"}
        return file_url

def download_xml(file, file_url):
    file_name = file.replace('html', 'xml')
    file_to_download = file_url[file].replace('htm', 'xml')
    try:
        # download the xml
        print('Downloading: ' + file_to_download)
        with http.request('GET', file_to_download, preload_content=False) as r, open(os.path.join(path, file_name), 'wb') as out_file:       
            shutil.copyfileobj(r, out_file)
    except Exception as e:
        print(e)
        file_name = 'not downloadable'
    return file_to_download, file_name

def start_process():
    print ('Starting to download...', multiprocessing.current_process().name)

def create_output_dir():
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    start = time.time()

    create_output_dir()
    # get all files that are less than 1kb
    files = get_all_files('htm')
    file_url = extract_xml(files)

    xml_store = open('xml_store.csv','wt')
    writer = csv.writer(xml_store, delimiter = ',')

    pool = multiprocessing.Pool(processes=size, initializer=start_process)
    pool_outputs = [pool.apply_async(download_xml, args=(file, file_url)) for file in files]
    pool_outputs = [p.get() for p in pool_outputs]

    print ('Waiting for all subprocesses done...')

    for row in pool_outputs:
        try:
            writer.writerow(row)
        except:
            writer.writerow(['write unsuccessful'])
    xml_store.close()

    end = time.time()
    print('time')
    print(end - start)

if __name__ == "__main__":
    main()