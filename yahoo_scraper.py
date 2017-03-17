import getpass
import mechanize
from bs4 import BeautifulSoup
import requests
import csv

login_url = 'https://login.yahoo.com/'
loginu = raw_input('Enter your Yahoo email address: ')
loginp = getpass.getpass()
group_id = raw_input('Enter the bracket group ID: ')

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(login_url)
br.select_form(nr = 0)
br.form['username'] = loginu
br.submit()
br.select_form(nr = 0)
br.form['passwd'] = loginp
br.submit()

url_base = 'https://tournament.fantasysports.yahoo.com'
group_url = '{}/t1/group/{}/standings'.format(url_base,group_id)

brackets = {}
stop = 0

print 'Getting bracket IDs...'
while stop == 0:
	res = br.open(group_url)
	soup = BeautifulSoup(res.read())
	tbl = soup.find('table',class_='Tst-group-standings-table')
	tbl_body = tbl.find('tbody')
	tbl_rows = tbl_body.find_all('tr')
	for row in tbl_rows:
		b_link = row.find('a',class_='Fz-xss')
		b_url = b_link['href']
		b_name = b_link.string
		print b_url, b_name
		if b_url in brackets:
			stop = 1
		else:
			brackets[b_url] = b_name
	tbl_foot = soup.find('ul',class_='My-xl')
	for a in tbl_foot.find_all('a'):
		if a.string[:4] == 'Next':
			next_link = a['href']
			group_url = url_base + next_link

print 'Getting picks...'
with open('madness.csv', 'wb') as csv_file:
	writer = csv.writer(csv_file)
	for k,v in brackets.items():
		entry_url = url_base + k
		r = requests.get(entry_url)
		soup = BeautifulSoup(r.content)
		scraped_picks = soup.find_all('strong',class_='ysf-tpe-user-pick')
		picks = []
		for p in scraped_picks:
			start = str(p).find('</em>') + 6
			end = str(p).find('</b>')
			picks.append(str(p)[start:end])
		writer.writerow([k,v]+picks)
		print k, picks




