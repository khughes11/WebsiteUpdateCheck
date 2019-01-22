# This program keeps a list of websites and copies of those websites. Each time the program is run it checks
# to see if those websites are different (is the site longer or shorter).

import os
import urllib.request
import smtplib

#the below is to test grabsite function	
#URL = 'http://books.toscrape.com/'
	

def main():
	sites = downaddlist() # these are sites currently stored
	new_sites = downnewaddress() # these are new sites.
	for s in new_sites:
		site_data = grabsite(s)
		new_site_filename = whatname()
		savefile(site_data,new_site_filename)
		updateaddresslist(s,new_site_filename)
	email_list = []
	for es in sites:
		live_site = grabsite(es)
		saved_site = grabsavedsite(sites[es])
		site_test = comparesites(live_site,saved_site) # sites are the same if this returns true
		if site_test == False:
			email_list.append(es)
			savefile(live_site,sites[es])# add new site to file
	email_body = emailthislist(email_list)
	emaillist(email_body)
	
def downnewaddress():
	if not os.path.isfile("newaddress.txt"):
		print("No new address file")
	else:
		with open('newaddress.txt','r') as newadd:
			newaddress = newadd.readlines()
			if newaddress:
				newaddress = [x.strip('\n') for x in newaddress]
				blank = ""
				newaddress = {newaddress[i]:blank for i in range(0,len(newaddress),1)}
			else:
				print('no new address')
		newadd.close()
	clearfile()
	return newaddress	

def clearfile():
	with open('newaddress.txt','w') as overwrite:
		overwrite.close()

def downaddlist():
	#returns dictionary of address plus name
	addresslist = []
	addressdict = {}
	if not os.path.isfile("addresslist.txt"):
		print( "No Master List")
		return addressdict
	else:
		#print('else')
		with open('addresslist.txt','r') as addlist:
			addresslist = addlist.readlines()
			addresslist = [x.strip('\n') for x in addresslist]
			addresslist.pop(0)
			#print(f'after pop {addresslist}')
			addresslist2 = []
			for x in addresslist:
				y = x.split(',')
				for z in y:
					addresslist2.append(z)
			#print(addresslist2)
			addressdict = {addresslist2[i]:addresslist2[i+1].strip() for i in range(0,len(addresslist2),2)}
	return addressdict

def grabsite(URL):
	#return "arggggg"
	
	req = urllib.request.Request(URL,headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0' })
	handler = urllib.request.urlopen(req)
	handler = handler.read()
	handler = str(handler)
	return handler

def comparesites(oldsite,newsite):

	if len(oldsite) == len(newsite):
		return True
	else:
		return False

def grabsavedsite(filename):
	# Oct 8, this seems to work. 
	with open(filename, 'r') as savefile:
		data = savefile.read()
		return data
		
def whatname():
	#this function returns a file name for a given new site. 
	addressdict = downaddlist()
	#print(f'top level {addressdict}')
	if len(addressdict) == 0:
		#print('if')
		value_to_add = 0
		newfilename = str(value_to_add + 1) + '.txt'
		#print(f'empty dict {newfilename}')
		return newfilename
	else:
		#print('else')
		dictvalues = list(addressdict.values())
		#print(dictvalues)
		intdictvalues = [int(x.strip('.txt')) for x in dictvalues]
		#print(intdictvalues)
		value_to_add = max(intdictvalues)
		newfilename = str(value_to_add + 1) + '.txt'
		#print(f'non empty{newfilename}')
		return newfilename

def savefile(file,name):

	with open(name, 'w') as makenewfile:
		makenewfile.write(file)
	
def updateaddresslist(url,filename):
	with open('addresslist.txt', 'a') as addlist:
		addlist.seek(0,2)
		addlist.write('\n' + url + ', ' + filename)		

def emailthislist(emaillist):
	# makes the message
	message = ""
	for x in emaillist:
		message = message + '\n' + x
	return message
	
def emaillist(emaillist):
	#print(emaillist)
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.starttls()
	server.login("your username", "your password")
	server.sendmail(
	"from@address.com", 
	"to@address.com", 
	f'{emaillist}')
	server.quit()
	#print(f'the email list {emaillist}')
	
if __name__ == '__main__':
	main()

