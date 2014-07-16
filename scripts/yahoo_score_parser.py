from bs4 import BeautifulSoup
import urllib2

# url = "http://sports.yahoo.com/nfl/pittsburgh-steelers-baltimore-ravens-20131128033/"
# req = urllib2.Request(url)
# resp = urllib2.urlopen(req)
# html = resp.read()
# f = open('box_score_html.txt', 'w+')
# f.write(html)

f = open('box_score_html.txt', 'r')
html = f.read()
f.close()
soup = BeautifulSoup(html)
passing = soup.find_all("table", summary="PASSING")

for passing_section in passing:
    #print passing_section
    tbody = passing_section.find("tbody")
    tr = tbody.find_all("tr")
    print tr
    for row in tr:
        th = row.find("th", class_="athlete")
        name = th.get_text()
        yards = row.find("td", class_="yards").get_text()
        touchdowns = row.find("td", class_="touchdowns").get_text()
        interceptions = row.find("td", class_="interceptions").get_text()
        fumbles_lost = row.find("td", class_="fumbles-lost").get_text()


    print "XXX"

#print passing
#print passing.find_all("th", class_="athlete")