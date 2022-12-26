Install dependency for Postgres python API:
- `sudo apt-get install libpq-dev`

Install requirements:
- `pip install -r requirements.txt`

Install PostgreSQL with following commands:
- `sudo apt update`
- `sudo apt install postgresql postgresql-contrib`
- `sudo systemctl start postgresql.service`

PostgreSQL shell commands
- \l (show all databases)
- \c players (switch to database "players")
- \dt (show all relations)

Enter PostgreSQL shell with the following command:
- `sudo -u postgres psql postgres`

- Create table with following:

```sql
CREATE TABLE players (
 ID SERIAL,
 url varchar(255) NOT NULL,
 player_id varchar(255),
 name varchar(255),
 full_name varchar(255),
 date_of_birth varchar(255),
 age int,
 dead varchar(255),
 place_of_birth varchar(255),
 country_of_birth varchar(255),
 positions varchar(255),
 current_club varchar(255),
 national_team varchar(255),
 apps_curr_club int,
 goals_curr_club int,
 apps_nat_team int,
 goals_nat_team int,
 scraping_timestamp varchar(255),
 PRIMARY KEY (url)
);
```

Run scraper with following command
- `python3 main.py data/playersURLs.csv data/playersData.csv`

Expected output will be something like this:
```bash
Connecting to the PostgreSQL database...
PostgreSQL database version:
('PostgreSQL 10.22 (Ubuntu 10.22-0ubuntu0.18.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0, 64-bit',)
Started importing data...
99it [00:00, 419.94it/s]
Finished importing data.
Started scraping data...
109it [00:53,  2.02it/s]
Finished scraping data.
Database connection closed.
```

- Add columns

```sql
ALTER TABLE players ADD age_category varchar(255);
ALTER TABLE players ADD goals_per_club_game float;
```

- Update those columns

```sql
UPDATE players
SET age_category = (
CASE
    WHEN age > 0 AND age <= 23 THEN 'Young'
    WHEN age >= 24 AND age <= 32 THEN 'MidAge'
    WHEN age >= 33 THEN 'Old'
END);
```
```sql
UPDATE players
SET goals_per_club_game = CAST(goals_curr_club AS FLOAT(2))/apps_curr_club
WHERE 
goals_curr_club IS NOT NULL AND  
apps_curr_club > 0;
```
- the average age, the average number of
appearances and the total number of players by club

```sql
SELECT AVG(age) AS years, AVG(apps_curr_club) AS apps, COUNT(*) AS total, current_club
FROM players
GROUP BY current_club;
```

- for every player from one chosen club,
extract the number of players who are younger, play in the same position and have a
higher number of national team appearances than that player

```sql
SELECT COUNT(*)-1 AS num,p1.name FROM players p1 
LEFT JOIN players p2 
ON p2.age < p1.age AND p1.positions=p2.positions AND p1.apps_nat_team < p2.apps_nat_team
GROUP BY p1.name;
```

- number of updated players
```sql
SELECT COUNT(*) FROM players
WHERE id <= 91 AND scraping_timestamp IS NOT NULL;
```