import requests
from bs4 import BeautifulSoup
def raw_data(web_address_list):
	'''
	Takes in list of string web addresses; e.g. "http://student.mit.edu/catalog/m6a.html"
	Outputs dictionary; keys = class number; values = (class name, prereq)
	'''
	prereq_dict = {}
	name_dict = {}
	for web in web_address_list:
		# parse into soup object
		page = requests.get(web)
		soup = BeautifulSoup(page.content, 'html.parser')
		# put into dictionary
		p_text = [i.text for i in soup.find_all('p')]
		for item in p_text[:10]:
			p_list = item.split('\n')
			course_list = p_list[0].split(' ')
			number = course_list[0]
			name = ' '.join(course_list[1:])
			name_dict[number] = name
			for i in p_list:
				if i[:6] == 'Prereq':
					prereqs = i[8:]
					print(prereqs)
					prereq_dict[number]= i[8:]
	return prereq_dict, name_dict

# course 6 raw data

basic = ["http://student.mit.edu/catalog/m6a.html"]

# basic = ["http://student.mit.edu/catalog/m6a.html",\
# 'http://student.mit.edu/catalog/m6b.html',\
# 'http://student.mit.edu/catalog/m6c.html']
cs_prereq, cs_name = raw_data(basic)




