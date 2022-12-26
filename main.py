from scraper import scraper
from database import connect
from tqdm import tqdm
import sys

COLUMN_NAMES = {
    "Player ID": "player_id",
    "URL": "url", 
    "Name": "name", 
    "Full name": "full_name", 
    "Date of birth": "date_of_birth", 
    "Age": "age", 
    "Dead": "dead",
    "Place of birth": "place_of_birth", 
    "Country of birth": "country_of_birth", 
    "Position(s)": "positions", 
    "Current club":"current_club", 
    "National team": "national_team", 
    "No. appearances current club": "apps_curr_club", 
    "No. goals current club": "goals_curr_club",
    "No. appearances national team": "apps_nat_team", 
    "No. goals national team": "goals_nat_team",  
    "Scraping timestamp": "scraping_timestamp"
}

# replace empty strings with None
def replace_empty_string(text: str):
    if text == "":
        return None
    return text

def generate_sql(item):
    sql = "INSERT INTO players ("
    sql += ", ".join([COLUMN_NAMES[key] for key in scraper.COLUMNS])
    sql += ") VALUES (" + ", ".join(["%s" for _ in scraper.COLUMNS]) + ")"
    sql += "ON CONFLICT (url) DO UPDATE SET "
    sql += ", ".join([COLUMN_NAMES[key] + "=%s" for key in scraper.COLUMNS[1:]])
    
    val = tuple([replace_empty_string(item.get(key)) for key in scraper.COLUMNS])
    val += tuple([replace_empty_string(item.get(key)) for key in scraper.COLUMNS[1:]])

    return sql, val

def delete_row(item):
    sql = "DELETE FROM players WHERE url=%s"
    val = tuple([item["URL"]])

    return sql, val

def main(playersURLs, playersData):
    # connect to database
    try:
        conn, cur = connect.connect()
    except Exception:
        return

    print("Started importing data...")

    # open data/playersData.csv, read it and add it to database
    with open(playersData, "r") as f:
        # first line are names of columns separated by commas
        columns = f.readline().strip().split(";")
        columns[0] = "Name"

        for line in tqdm(f):
            line = line.strip().split(";")
            
            item = {columns[i]: line[i] for i in range(len(columns))}
            
            # if row is empty, skip it
            if item["No data"] == "1":
                continue
            

            # keep only the columns from COLUMN_NAMES
            item = {key: replace_empty_string(item.get(key)) for key in COLUMN_NAMES.keys() if key in item.keys()}
            
            if item["Dead"] != '0':
                item["Dead"] = 1
            
            

            sql, val = generate_sql(item)

            cur.execute(sql, val)
            conn.commit()

    print("Finished importing data.")
    print("Started scraping data...")

    # now add items from scraper to database
    for item, insert in scraper.scraper(playersURLs):
        
        # push each item to database
        if insert:
            sql, val = generate_sql(item)
        else:
            # drop row
            sql,val = delete_row(item)

        cur.execute(sql, val)
        conn.commit()

    print("Finished scraping data.")
    connect.disconnect(conn,cur)

if __name__ == "__main__":
    # accept two arguments: path to playersURLs.csv and path to playersData.csv
    if len(sys.argv) != 3:
        print("Usage: python main.py <path/to/playersURLs.csv> <path/to/playersData.csv>")
        exit(1)

    playersURLs = sys.argv[1]
    playersData = sys.argv[2]

    main(playersURLs, playersData)
