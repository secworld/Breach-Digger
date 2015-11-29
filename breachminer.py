#! /usr/bin/python

import requests
import urllib
import os.path
import xml.etree.ElementTree as ET

   
print "\033[31m \n"            
banner = """\n \
$$$$$$$\                                          $$\       $$\      $$\ $$\                               
$$  __$$\                                         $$ |      $$$\    $$$ |\__|                              
$$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\  $$$$\  $$$$ |$$\ $$$$$$$\   $$$$$$\   $$$$$$\  
$$$$$$$\ |$$  __$$\ $$  __$$\  \____$$\ $$  _____|$$  __$$\ $$\$$\$$ $$ |$$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$  __$$\ $$ |  \__|$$$$$$$$ | $$$$$$$ |$$ /      $$ |  $$ |$$ \$$$  $$ |$$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
$$ |  $$ |$$ |      $$   ____|$$  __$$ |$$ |      $$ |  $$ |$$ |\$  /$$ |$$ |$$ |  $$ |$$   ____|$$ |      
$$$$$$$  |$$ |      \$$$$$$$\ \$$$$$$$ |\$$$$$$$\ $$ |  $$ |$$ | \_/ $$ |$$ |$$ |  $$ |\$$$$$$$\ $$ |      
\_______/ \__|       \_______| \_______| \_______|\__|  \__|\__|     \__|\__|\__|  \__| \_______|\__|      
                                                                                                           
                                                                        Author   : @dH4wk
                                                                        Twitter  : https://twitter.com/dH4wk
                                                                                
"""


headers = {'User-Agent' : 'Digging-for-Pentesting', 'Accept' : 'application/vnd.haveibeenpwned.v2+json'}
BaseUrl = 'https://haveibeenpwned.com/api/v2/pasteaccount/'

def invokeHarvester(domain):
    print '\033[93m [*] Running with configuration : -l 500 -b google '
    os.system('theharvester -d '+domain+' -l 500 -b google -f harv_output.xml')
    tree = ET.parse('harv_output.xml')
    with open('harv_emails.txt', "w") as f:
        for elem in tree.iter(tag='email'):
            print elem.text
            f.write(elem.text+'\n')
    f.close()

def exit_gracefully():
    print 

def invokeBM(EmailList):
    print EmailList
    print ("\033[94m *************************************************************************************")
    choice = raw_input("\033[92m Do you want to go for a detailed analysis \033[93m[Y/N] : ")
    os.system('clear')
    print ("\n  [*] "+"\033[92m"+"I am mining ... Sit back and relax !!!")
    with open(EmailList) as f:
        for email in f:
            Url1 = urllib.quote(email, safe='')
            Url = BaseUrl+Url1
            Url = Url[:-3]
            r = requests.get(Url, headers = headers)
            try:
                JsonData =  (r.json())
            except ValueError:
                print "\n \033[31m [*] No data found for " + email
                
            if (r.status_code == 200):
                print ('\n')
                print ("\033[94m *************************************************************************************")
                print '  \033[93m  [*] Located email account in leaked data dumps for : \033[93m'+email
                print ("\033[94m *************************************************************************************")
                print ('\n')
                for item in JsonData:
                    source = item.get('Source')
                    did = item.get('Id')
                    title = item.get('Title')
                    if title is None:
                        title = "None"
                        
                    if choice.lower() == 'n':
                        print ('\n')
                        print "\033[92m Title of the dump : "+title
                        print "\033[92m Source of the dump : "+source
                        print "\033[92m Breach data can be found at : "+source+"/"+did
                        print ('\n')
                        
                    if choice.lower() == 'y':
                        if source == 'Pastebin':
                            puid = did
                            purl = 'http://pastebin.com/raw.php?i='+puid
                            r1 = requests.get(purl, headers = headers)
                            if r1.status_code != 302:
                                if r1.status_code != 404:
                                    print '\n'
                                    print "\033[94m"+"=============================================================================================================="
                                    print "\033[98m [*]   Got It !!! Dump found at "+purl+' for email account \033[93m'+email
                                    print "\033[94m"+"=============================================================================================================="
                                    CurrPath =  os.getcwd()+'/tmp.txt'
                                    grab = str('wget '+purl+' -O  '+CurrPath+' > /dev/null 2>&1')
                                    os.system(grab)
                                    #CredMiner(CurrPath, email)
                                    print '\033[92m'
                                    os.system('cat '+CurrPath+' | grep -B 1 -A 1 '+email)
                                    if os.path.exists(CurrPath):
                                        #os.system('mv '+CurrPath+' tmp.txt.bkp')
                                        os.system('rm '+CurrPath)
                                    
                                else:
                                    print "\n \033[31m [*] Sorry !!! The pastebin dumb seems to be missing at "+source+"/"+did+"  :( "
    f.close()
                            
if __name__ == "__main__":
    os.system('clear')
    print banner
    try:
        print '[1] Run TheHarvester '
        print '[2] Input email file '
        st = raw_input('Please select an option [1/2] : ')
        if st == "1":
            domain = raw_input('Enter the domain to seed the harvester : ')
            invokeHarvester(domain)
            harvpath = os.getcwd()+'/harv_emails.txt'
            print harvpath
            invokeBM(harvpath)
        elif st == "2":
            EmailList = raw_input("\033[92m Enter the path of the file containing Email Accounts : ")
            invokeBM(EmailList)
        else:
            print "Sorry I am not so intelligent ... Exiting !!!"  
            exit(1)
    
    except KeyboardInterrupt:
        print '\n \n  Exiting ... Bye!!! \n'
        print " \033[92m +++++++  Happy Hunting  +++++++++ \n"
        exit(0)
    

print "\n   \033[92m +++++++  Happy Hunting  +++++++++"
print '\n'
