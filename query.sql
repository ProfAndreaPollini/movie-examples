-- SQLite
SELECT
    movies.title,
    movie_types.name,
    age_certifications.name
FROM
    movies
JOIN age_certifications ON movies.age_certification_id = age_certifications.id
JOIN movie_types ON movies.movie_type_id = movie_types.id
WHERE
    movies.id = 0

SELECT
    movies.title,
    genres.name
FROM
    movies
JOIN movies_genres ON movies.id = movies_genres.movie_id
JOIN genres ON movies_genres.genre_id = genres.id
WHERE
    movies.id = 0

SELECT movies.title 
FROM movies
JOIN movies_genres ON movies.id = movies_genres.movie_id
JOIN genres ON movies_genres.genre_id = genres.id
WHERE genres.name = 'crime'


