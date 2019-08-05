import csv
import re,shutil
from bs4 import BeautifulSoup
import urllib3
import multiprocessing

#thread pool size
size = 32 


urllib3.disable_warnings()

#set socket pool
http = urllib3.PoolManager(size)

#path to store htm files
path = './htm/'


# main function to find and download intangible assets htm
def get_table(cik,acc,path):
    url = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='+cik+'&accession_number='+acc+'&xbrl_type=v#' # url to the initial html
    try:
        soup = BeautifulSoup(http.request('GET', url).data,'lxml')
    except:
        # page is not available
        table_url = 'no available XBRL'
        file_name = 'None'
    else:
        try:
            # find 'Notes to Financial Statements' tab
            tab_button = soup.find(text = 'Notes to Financial Statements',name ='a',href = "#")

            #move next to the list of tab contents
            menulist = tab_button.next_sibling.next_sibling
        except:
            table_url = 'no Financial Statements'
            file_name = 'None'
        else:
            #find 'Intangible' tab
            item_button = menulist.find(text = re.compile(r"(.*)Intangible(.*)",re.I),name ='a',class_ = "xbrlviewer")
            if item_button is None:
                table_url = 'no Intangible Assets'
                file_name = 'None'
            else:
                # get its href with the report number
                item_button = item_button['href']

                # find the report number
                serial = re.findall(r'\((.*?)\)', item_button)[0]

                #url to the table page
                table_url = 'https://www.sec.gov/Archives/edgar/data/'+cik+'/'+re.sub('-', '', acc)+'/R'+serial+'.htm'
                file_name = '/'+cik+'_'+acc+'.html'
                try:
                    #download the table page
                    with http.request('GET', table_url, preload_content=False) as r, open(path+file_name, 'wb') as out_file:       
                        shutil.copyfileobj(r, out_file)
                except:
                    file_name = 'not downloadable'

    print('finish processing item with cik: %s, acc: %s, url: %s'%(cik,acc,table_url))
    return table_url,path+file_name



        


# load all items in the input csv file
def get_link_list(listcsv):
    with open(listcsv,'rt') as indicies:
        csvReader = csv.reader(indicies, delimiter=",")
        csvData = list(csvReader)

        #cik, acc, others
        link_list = [(line[2],line[3][:-4].split('/')[3],line[0],line[1],line[4],line[5]) for line in csvData[1:]]
        return link_list


def concurrency(args):
    # worker only accept one list of arguments
    return args, get_table(args[0],args[1],path)

def start_process():
    print ('Starting',multiprocessing.current_process().name)

if __name__ == "__main__":
    listcsv = './tenk2008after.csv'
    url_list = get_link_list(listcsv)
    tasks = url_list

    print('loading finished')

    storage = open('./tenk2008after_xbrl.csv','wt')
    writer = csv.writer(storage,delimiter = ',')

    # pool_size = multiprocessing.cpu_count()
    pool_size = size
    pool = multiprocessing.Pool(processes=pool_size, initializer=start_process, )
    pool_outputs = pool.map(concurrency, tasks)

    print ('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print ('All subprocesses done.')
    for row in pool_outputs:
        try:
            writer.writerow(row)
        except:
            writer.writerow(['write unsuccessful'])
    storage.close()
    

    # with open('./tenk2008after_short.csv','rt') as indicies, open('./tenk2008after_xbrl.csv','wt') as storage:
    #     reader = csv.reader(indicies,delimiter = ',')
    #     writer = csv.writer(storage,delimiter = ',')
    #     header = next(reader)
    #     header.extend(['table_url','table_file'])
    #     writer.writerow(header)
    #     for line in reader:
    #         out_buffer = line 
    #         cik = line[2]
    #         acc = line[3][:-4].split('/')[3]
    #         out_buffer.extend(get_table(cik,acc,'./htm/'))
    #         writer.writerow(out_buffer)
    #         storage.flush()




