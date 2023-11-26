import csv
import os
from os import path
import json
import sqlite3 as sq

rows = []



with open(path.join("movie-data","imdb_movies_shows.csv"), 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        rows.append(line)

# remove header
rows.pop(0)

print(f"Total number of rows: {len(rows)}")

movie_type = list(set([x[1] for x in rows]))
print(movie_type)

age_certifications = list(set([x[3] for x in rows]))
print(f"Age certifications: {age_certifications}")	

genres = []
for x in rows:
    d = eval(x[5])
    genres.extend(d)
genres = list(set(genres))
print(f"Genres: {genres}")

production_countries = []
for x in rows:
    d = eval(x[6])
    
    production_countries.extend(d)
production_countries = list(set(production_countries))
print(f"Production countries: {production_countries}")

film_genres = []

for i,x in enumerate(rows):
    d = eval(x[5])
    for y in d:
        film_genres.append((i,genres.index(y)))

film_production_countries = []

for i,x in enumerate(rows):
    d = eval(x[6])
    for y in d:
        film_production_countries.append((i,production_countries.index(y)))



for i in range(len(rows)):
    rows[i][1] = movie_type.index(rows[i][1])
    rows[i][3] = age_certifications.index(rows[i][3])
    # for col in (1,4,5,6):
    #     del rows[i][col]
    rows[i][2] = int(rows[i][2])
    rows[i][4] = int(rows[i][4])
    rows[i][7] = None if rows[i][7] == "" else float(rows[i][7])
    # rows[i][8] = -1.0 if rows[i][8] == "" else float(rows[i][8])
    rows[i][9] = None if rows[i][9] == "" else float(rows[i][9])
    rows[i][10] = None if rows[i][10] == "" else float(rows[i][10])

    for col in (6,5):
        del rows[i][col]
    
    


print([(pos,*x) for pos,x in enumerate(rows)][0])


conn  = sq.connect(path.join("netflix.db"))

c = conn.cursor()

c.executescript("""
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movies_genres;
                DROP TABLE IF EXISTS movie_types;
DROP TABLE IF EXISTS production_countries;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS age_certifications;    
DROP TABLE IF EXISTS production_countries;

CREATE TABLE IF NOT EXISTS age_certifications ( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
);
                
CREATE TABLE IF NOT EXISTS countries (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
);
                
CREATE TABLE IF NOT EXISTS movie_types (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
);  

CREATE TABLE IF NOT EXISTS movies (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,   
movie_type_id INTEGER NOT NULL,    
release_year INTEGER NOT NULL,
age_certification_id INTEGER NOT NULL,
duration INTEGER NOT NULL,
seasons INTEGER NULL,  
imdb_id INTEGER NULL,     
imdb_score REAL NULL,   
imdb_votes INTEGER NULL,
FOREIGN KEY(age_certification_id) REFERENCES age_certifications(id)             
);     
                
CREATE TABLE IF NOT EXISTS genres (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS movies_genres (
movie_id INTEGER NOT NULL,
genre_id INTEGER NOT NULL,
FOREIGN KEY(movie_id) REFERENCES movies(id),
FOREIGN KEY(genre_id) REFERENCES genres(id)
);



CREATE TABLE IF NOT EXISTS production_countries (
movie_id INTEGER NOT NULL,
country_id INTEGER NOT NULL,
FOREIGN KEY(movie_id) REFERENCES movies(id),
FOREIGN KEY(country_id) REFERENCES countries(id)
);
             
""")	
conn.commit()

c.executemany("INSERT INTO movie_types (id,name) VALUES (?,?)", [x for x in enumerate(movie_type)])
c.executemany("INSERT INTO age_certifications (id,name) VALUES (?,?)", [x for x in enumerate(age_certifications)])
c.executemany("INSERT INTO genres (id,name) VALUES (?,?)", [x for x in enumerate(genres)])
c.executemany("INSERT INTO countries (id,name) VALUES (?,?)", [x for x in enumerate(production_countries)])
c.executemany("INSERT INTO movies (id,title,movie_type_id,release_year,age_certification_id,duration,seasons,imdb_id,imdb_score,imdb_votes) VALUES (?,?,?,?,?,?,?,?,?,?)", [(pos,*x) for pos,x in enumerate(rows)])
c.executemany("INSERT INTO movies_genres (movie_id,genre_id) VALUES (?,?)", film_genres)
c.executemany("INSERT INTO production_countries (movie_id,country_id) VALUES (?,?)", film_production_countries)
conn.commit()