#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import urllib

MENU_URL = "http://valg.nrk.no/valg2013/valgresultat/kommuner"
KOMMUNE_URL_BASE = "http://valg.nrk.no"
OUTPUT_FILE = "stortingsvalg2013.tsv"

# first let's get the name of the municipalities (=kommuner)
html = urllib.urlopen(MENU_URL).read()
menu = bs(html)
kommuner = [(x["href"],x["title"]) for x in menu.findAll("a",{"class":"knapp"})]

# then we iterate through them, getting one html per municipality
# and scraping the relevant data
res = []
for k_url,k in kommuner:
    k_html = urllib.urlopen(KOMMUNE_URL_BASE + k_url).read()
    soup = bs(k_html)
    parties = soup.findAll("tr")[1:]
    res.extend([(k,x.find("a").text,\
    				x.find("span").text.replace('%','').replace(',','.'),\
    				x.findAll("td")[-1].text.replace(' ','')) \
    			for x in parties])
    print k # print the municipality to keep track of progress

# finally we write the data to a csv (tsv) file
f = open(OUTPUT_FILE,'w')
f.write("Municipality\tParty\tPercentage\tVotes\n")
for line in res:
	f.write("%s\t%s\t%s\t%s\n" % line)
f.close()