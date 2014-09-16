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
opener.addheaders = [('Referer','http://result.pondiuni.edu.in/candidate.asp')]
opener.addheaders = [('Cookie','ASPSESSIONIDAAQAQSTR=KOKBIPMCPKPKHEFBMBGGIGNO')]
opener.addheaders = [('Content-Type','application/x-www-form-urlencoded')]
opener.addheaders = [('Content-Length','141')]
url='http://result.pondiuni.edu.in/ResultDisp.asp'
def retrieve_result(reg_no, dept_id, sem_no, url, opener, out_dir):
    print("Processing " + reg_no)
    value = {'txtregno':reg_no,
            'cmbdegree':dept_id+'~\\'+dept_id+'\\result.mdb',
            #value, What it contains,'cmbdegree'->BTECH for first year
            #BTHCS-> for ComputerScience
            #BTHIT -> Information Technology BTHEC -> ECE
            'cmbexamno':sem_no,
            'dpath':'\\'+dept_id+'\\result.mdb',
            'dname':dept_id,
            'txtexamno':sem_no}
    data=urllib.urlencode(value)
    purl=urllib2.Request(url,data)
    try_count = 5
    while True:
        try:
            res=opener.open(purl)
            break
        except:
            try_count = try_count - 1
            if try_count == 0:
                return -1 # to test ,occurance of error in the program
    page=res.read()
    fin = open(('%s/%s.html' % (out_dir, reg_no)),'w')
    fin.write(page)
    fin.close()
    print("Processing " + reg_no + " successfully")
    return None
