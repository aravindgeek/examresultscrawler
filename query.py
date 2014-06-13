#!/usr/bin/python
# -*- coding: utf-8 -*-
#python script to retrieve exam results
import urllib
import urllib2
opener = urllib2. build_opener()
#building headers a
opener.addheaders = [('Host','result.pondiuni.edu.in')]
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686;rv:14.0) Gecko/20100101 Firefox/14.0.1')]
opener.addheaders = [("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")]
opener.addheaders = [('Accept-Language','en-us,en;q=0.5')]
opener.addheaders = [('Accept-Encoding','gzip, deflate')]
opener.addheaders = [('Connection','keep-alive')]
opener.addheaders = [('Referer','http://result.pondiuni.edu.in/results/candidate.asp')]
opener.addheaders = [('Cookie','ASPSESSIONIDAAQAQSTR=KOKBIPMCPKPKHEFBMBGGIGNO')]
opener.addheaders = [('Content-Type','application/x-www-form-urlencoded')]
opener.addheaders = [('Content-Length','141')]
url='http://result.pondiuni.edu.in/results/ResultDisp.asp'
def retrieve_result(regno_comm,number,dept_id,sem_no,url,opener):
    number=str(number)
    if len(number)==1:
        number='0'+number
    reg_no=regno_comm+number
    print("Processing " + regno_comm + number)
    value={'txtregno':reg_no,'cmbdegree':dept_id+'~\\results\\'+dept_id
    +'\result.mdb','cmbexamno':sem_no,'dpath':'\\results\\'+dept_id+
    '\\result.mdb','dname':dept_id,'txtexamno':sem_no}

    print value
    data=urllib.urlencode(value)
    purl=urllib2.Request(url,data)
    i=0
    while True:
        try:
    	    res=opener.open(purl)
	    break
        except:
            print "some error has occured retrying",i
	    i=i+1	
	        
    page=res.read()
    fin = open((reg_no+'.html'),'w')
    fin.write(page)
    fin.close()
    print("successfully stored "+reg_no+'.html')
    print '========================================================================'
    #value, What it contains,'cmbdegree'->BTECH for first year
    #BTHCS-> for ComputerScience
    #BTHIT -> Information Technology BTHEC -> ECE

#for i in range(start_no,end_no):
    #reg_no=comm_part + str(i)
    ##posting student details
    #print("Processing" + '11td' + str(no+i))
    #value={'txtregno':reg_no,'cmbdegree':'BTECH~\\results\\BTECH\result.mdb','cmbexamno':'B','dpath':'\\results\\BTECH\\result.mdb','dname':'BTECH','txtexamno':'A'}
    #data=urllib.urlencode(value)
    ##print data
    #purl=urllib2.Request(url,data)
    #res=opener.open(purl)
    #page=res.read()
    #print("successfully stored"+'11td'+str(no+i)+'.html')
    #fin=open('11td'+str(no+i)+'A.html','w')
    #fin.write(page)
    #fin.close()

    #Successfully Tested

