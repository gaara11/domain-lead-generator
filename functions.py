from googlescraper import *
import urllib.request
import re
import csv
import xlwt3 as xlwt

### -----------------------------------------Functions to get data --------------------------------------------

# Function to return list of URLS. (Depends on GoogleScraper)
def geturls(search,results_per_page,pages):
    result = []
    temp = scrape(search,results_per_page,pages,0)
    for url in temp:
        #temp = url.netloc
        hostname = url.hostname.split(".")
        hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
        #print (hostname)
        result.append(hostname)
    return result

# Function to creat url to pull info from
def whois_urlcreator(domain):
    #base_url="http://www.whoisfly.com/"
    base_url="http://www.freewhois.us/index.php?query="
    fullurl=base_url+domain+"&submit=Whois"
    return fullurl

# Function to extract whoisinfo from whoisurl. (Depends on urllib.request)
def getwhoisinfo(whoisurl):
    f=urllib.request.urlopen(whoisurl)
    try:
        result = f.read().decode('utf-8')
    except:
        result = ""
    return result
# Function to extract email IDs from whois info.(depends on Re)
def getwhoisemail(whoisinfo):
    #r = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
    r = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
    results = r.findall(whoisinfo)
    #for i in results:
     #   i=i.decode('utf-8') 
    return list(set(results))
# Function to writetocsv
def writetocsv():
    with open('emails.csv', 'w', newline='') as csvfile:
        emailwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        emailwriter.writerow(['a','b','c'])

## --------------------------------Excel Functions------------------------------------

# Function to create excel file, return wb. 
def excel_createfile(filename):
    wb=xlwt.Workbook()
    wb.add_sheet("test")
    wb.save(filename+'.xls')
    return wb
def excel_createsheet(sheetname,database):
    ws=database.add_sheet("Sheet1")
    return ws

# Function to writetoexcel and save
def excel_write(sheet,row,column,value):
    sheet.write(row,column,value)
    return row
def excel_savedatabase(database,name):
    database.save(name+'.xls')

excelfile = excel_createfile('abcd')
excelsheet = excel_createsheet('sheet1',excelfile)
excel_write(excelsheet,0,0,1)
excel_savedatabase(excelfile,'abcde')

#Function to write object to excel
def writeobject (item,sheet,row):
    excel_write(sheet,row,0,item.domain)
    excel_write(sheet,row,1,item.status)
    i=row
    final = row
    for a in item.emails:
        final = excel_write(sheet,i,2,a)
        i=i+1
    return final+1
    
# -------------------------Object ----------------------------------	
#Class to create Object
class excelitem(object):
    def __init__(self,domain,status,emails):
        self.domain = domain
        self.status = status
        self.emails = emails
    def showstatus(self):
        print (self.status)

def createobjects(keyword,results,prelist):
    b = geturls(keyword,results,1)
    print ("Length of Original URL list : " + str(len(b)))
    urllist = list(set(b))
    for e in prelist:
        if e in urllist:
            urllist.remove(e) 
    
    print ("Length of Final URL list : "+ str(len(urllist)))
    result = []
    for url in urllist:
        info = getwhoisinfo(whois_urlcreator(url))
        print(url + " emails :", end=" ")
        email = getwhoisemail(info)
        status=0
        if (len(email)==0):
            print ("No URLS")
            status=0
        else:
            print (len(email))
            status=1
        item=excelitem(url,status,email)
        result.append(item)
    return result


