from functions import *

# Creating Database
excelfile = excel_createfile('results')
excelsheet = excel_createsheet('sheet1',excelfile)
#excel_write(excelsheet,0,0,1)
excel_savedatabase(excelfile,'results')



#Creating list of objects
objectlist = []
urllist = []
f = open('keywords','r')
for line in f:
    print ("--------KEYWORD----------- : " + line)
    
    for a in objectlist :
        urllist.append(a.domain)
        
    objectlist.extend(createobjects(line,100,urllist))
temp=0

# Write to excel file from List
for item in objectlist:
    #print(str(item.status) + " -- " + item.domain)
    nextrow = writeobject(item,excelsheet,temp)
    excel_savedatabase(excelfile,'results')
    temp=nextrow
