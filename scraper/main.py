# Description: This file is the main file of the scraper. It will scrape the data from the URLs

import csv
import requests
from bs4 import BeautifulSoup
from datetime import date
from tqdm import tqdm

# open data/playersURLs.csv
urls = []
with open('data/playersURLs.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        urls.append(row[0])

# connect to postgresql database


columns = ["URL", "Name", "Full name", "Date of birth", "Age",
    "Place birth", "Country birth", "Position(s)", "Current club",
    "National team", "No. appearances current club", "No. goals current club", 
    "Scraping timestamp"]

# for each in urls, access the url and scrape the data
for url in tqdm(urls):
    # open the url
    page = requests.get(url)

    attributes = {"URL" : url}
    
    # remember scraping timestamp
    attributes["Scraping timestamp"] = date.today().strftime("%d/%m/%Y")

    # scrape
    soup = BeautifulSoup(page.content, 'html.parser')

    # create object
    object = soup.find(class_="infobox vcard")

    if object is None:
        continue
    
    # find all rows in object table
    rows = object.find_all("tr")
    
    attributes["Name"] = object.find(class_="fn").get_text()

    
    national_team = False
    
    # if insert is False, it means this is not a football player
    insert = True

    # remove first \n
    def remove_newline(text: str):
        if text[0] == '\n':
            return text[1:]
        return text

    for row in rows:
        # function which removes citation at the end if exists
        def remove_citation(text: str):
            if text.find("[") != -1:
                return text[:text.find("[")]
            return text

        if row.find(class_="infobox-label") is not None:
            label = row.find(class_="infobox-label").get_text()
            data = remove_citation(row.find(class_="infobox-data").get_text())
        else:
            # if row is infobox-header which contains substring "International career"
            # it means we passed the club team and now we are in the national team
            if row.find(class_="infobox-header") is not None:
                if row.find(class_="infobox-header").get_text().find("International career") != -1:
                    national_team = True
            continue

        # if there is label "Sport", it means this is not a football player
        if label == "Sport":
            insert = False
            break
        
        if len(label) == 0:
            continue    
        
        if label == "Date of birth":
            # split string into date and age, format: "\n (1996-05-12) 12 May 1996 (age 34)"
            data = data.split(" (age")
            if len(data) == 2:
                data[1] = data[1][1:-1]
                data[0] = data[0].split(") ")[1]
                attributes[label] = data[0]
                attributes["Age"] = data[1]
            else:
                # only date of birth is given
                attributes[label] = data[0]

        elif label == "Place of birth":
            # split string into place and country, format: "Birmingham, England" and possibly "Wilton, Cork, Ireland"
            # split by latest comma
            data = data.rsplit(", ", 1)
            if len(data) == 2:
                attributes[label] = remove_newline(data[0])
                attributes["Country of birth"] = data[1]
            else:
                # only country of birth is given
                attributes[label] = remove_newline(data[0])
        # last digit is minus sign implies current club or national team
        elif label[-1] == "–":
            # infobox-data-a is current club or national team
            data = row.find(class_="infobox-data-a").get_text()
            # if national_team is True, it means we are in the national team
            if national_team:
                label = "National team"
            else:
                label = "Current club"

                # infobox-data-b is number of apps
                attributes["No. appearances current club"] = remove_newline(row.find(class_="infobox-data-b").get_text())
                # infobox-data-c is number of goals with brackets
                goals = row.find(class_="infobox-data-c").get_text()
                # remove brackets
                goals = goals[2:-1]

                attributes["No. goals current club"] = goals
            
            attributes[label] = remove_newline(data)
        elif label in columns:
            attributes[label] = remove_newline(data)
        

    from pprint import pprint
    #pprint(attributes)
    
    if insert:
        # insert the data into the database
        pass
    

    # insert the data into the database



