from scraper import scraper
from database import connect

def main():
    # connect to database
    try:
        conn, cur = connect.connect()
    except Exception:
        return


    for i, item in enumerate(scraper.scraper()):
        
        # push each item to database
        column_names = {
            "ID": "id",
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

        item["ID"] = str(i)

        # if there is no "Age", we set it to -1
        if "Age" not in item.keys():
            item["Age"] = -1

        for key in scraper.COLUMNS:
            if key not in item.keys():
                item[key] = ""


        sql = "INSERT INTO players (" + ", ".join([column_names[key] for key in scraper.COLUMNS]) + ") VALUES (" + ", ".join(["%s" for key in scraper.COLUMNS]) + ")"
        val = tuple([item[key] for key in scraper.COLUMNS])

        cur.execute(sql, val)
        conn.commit()

    connect.disconnect(conn,cur)

if __name__ == "__main__":
    main()
