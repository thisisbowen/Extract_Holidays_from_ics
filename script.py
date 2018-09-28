import requests
import json
import dateutil
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime as dt
import csv
from icalendar import Calendar, Event

#Get iso code for available countries on website
my_url = "https://www.officeholidays.com/ics/"
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()
page_soup = BeautifulSoup(page_html, "html.parser")
fish_soup = page_soup.find("table",{"class":"info-table"}).findAll("a")
iso_code = []
for fish in fish_soup:
    iso_code.append(fish["href"][-2:])

#Read ics file and output results
with open("holiday.csv",'w',encoding = 'UTF-8', newline='') as fd:
    writer = csv.writer(fd)
    writer.writerow(["Location","Category", "Title", "Date"])
    base_url = "https://www.officeholidays.com/ics/ics_country_code.php?iso="
    for iso in iso_code:
        url = base_url + iso
        response = requests.get(url)
        gcal = Calendar.from_ical(response.content) #Convert into ics 
        for component in gcal.walk():
            if component.name == "VEVENT" and dateutil.parser.parse(component.get('dtstart').to_ical()).date() > dt.date.today():
                row = [
                    component.get('summary').split(":")[0].strip(), # Get Country
                    "Holiday",
                    component.get('summary').split(":")[1].strip(), # Get name of Holiday
                    dateutil.parser.parse(component.get('dtstart').to_ical()).date()  
                ]
                writer.writerow(row)