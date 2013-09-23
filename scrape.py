#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import urllib

MENU_URL = "http://valg.nrk.no/valg2013/valgresultat/kommuner"
KOMMUNE_URL_BASE = "http://valg.nrk.no"

html = urllib.urlopen(MENU_URL).read() #
menu = bs(html)
kommuner = [(x["href"],x["title"]) for x in menu.findAll("a",{"class":"knapp"})]

res = []
for k_url,k in kommuner:
    k_html = urllib.urlopen(KOMMUNE_URL_BASE + k_url).read()
    soup = bs(k_html)
    res.extend([(k,x.find("a").text,x.find("span").text,x.findAll("td")[-1].text) \
    			for x in [x for x in soup.findAll("tr")[1:]]])
    print k

for line in res:
	print "%s\t%s\t%s" % line

f = open("stortingsvalg2013.csv",'w')
for line in res:
	f.write("%s\t%s\t%s\n" % line)
f.close()