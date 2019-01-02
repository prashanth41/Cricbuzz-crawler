""" This program takes links of 2016,2017 and 2018 GSoC organization pages and 
ouputs the frequency of each organization to a text file """

from bs4 import BeautifulSoup
import requests

years=['2018','2017','2016']
page_links =['https://summerofcode.withgoogle.com/archive/'+years[0]+'/organizations/',
			 'https://summerofcode.withgoogle.com/archive/'+years[1]+'/organizations/',
			 'https://summerofcode.withgoogle.com/archive/'+years[2]+'/organizations/']


def get_organizations(page_link):

	# fetch the content from url
	page_response = requests.get(page_link, timeout=5)
	# parse html
	page_content = BeautifulSoup(page_response.content, "html.parser")


	organizations = page_content.find_all(class_='organization-card__name font-black-54')


	for i in range(len(organizations)):
	   organizations[i]=organizations[i].text

	#print(organizations)
	return(organizations)


temp_organizations=[]
for i in range(len(page_links)):

	temp_organizations.append(get_organizations(page_links[i]))

all_organizations=[]
for i in temp_organizations:
	for j in i:
		all_organizations.append(j)

print(len(all_organizations))


unique_organizations=list(set(all_organizations))
print(len(unique_organizations))

organizations_count={}

for i in unique_organizations:
	organizations_count[i]=0

	for j in all_organizations:

		if i==j:
			organizations_count[i]+=1

organizations_count = dict(sorted(organizations_count.items(), key=lambda x: (-x[1], x[0])))
print(organizations_count)


with open('gsoc_orgs_freq.txt','w+') as f:

	for org in organizations_count.keys():
		f.write(org+'--'+str(organizations_count[org]))
		f.write('\n')

f.close()

