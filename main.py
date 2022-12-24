from scraper import scraper
from database import connect

def main():
    # connect to database
    try:
        conn, cur = connect.connect()
    except Exception:
        return


    for item in scraper.scraper():
        # push each item to database
    #     "URL", "Name", "Full name", "Date of birth", "Age",
    # "Place of birth", "Country of birth", "Position(s)", "Current club",
    # "National team", "No. appearances current club", "No. goals current club", 
    # "Scraping timestamp"
        item
        column_names = {
            "URL": "url", 
            "Name": "name", 
            "Full name": "full_name", 
            "Date of birth": "date_of_birth", 
            "Age": "age", 
            "Place of birth": "place_of_birth", 
            "Country of birth": "country_of_birth", 
            "Position(s)": "positions", 
            "Current club":"current_club", 
            "National team": "national_team", 
            "No. appearances current club": "apps_curr_club", 
            "No. goals current club": "goals_curr_club", 
            "Scraping timestamp": "scraping_timestamp"
        }
        
        for key in scraper.COLUMNS:
            if key not in item.keys():
                item[key] = ""


        sql = "INSERT INTO players (" + ", ".join([column_names[key] for key in scraper.COLUMNS]) + ") VALUES (" + ", ".join(["%s" for key in scraper.COLUMNS]) + ")"
        val = tuple([item[key] for key in scraper.COLUMNS])
        print(sql)
        print(val)


        cur.execute(sql, val)
        conn.commit()

    connect.disconnect(conn,cur)

if __name__ == "__main__":
    main()