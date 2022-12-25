- sudo apt-get install libpq-dev

Enter PostgreSQL shell:
- sudo -u postgres psql postgres



SQL shell commands
- \l (show all databases)
- \c players (switch to database "players")
- \dt (show all relations)

CREATE TABLE players (
	ID int NOT NULL,
	url varchar(255),
	name varchar(255),
	full_name varchar(255),
	date_of_birth varchar(255),
	age int,
	place_of_birth varchar(255),
	country_of_birth varchar(255),
	positions varchar(255),
	current_club varchar(255),
	national_team varchar(255),
	apps_curr_club varchar(255),
	goals_curr_club varchar(255),
	scraping_timestamp varchar(255),
	PRIMARY KEY (ID)
);

