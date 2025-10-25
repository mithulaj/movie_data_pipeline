-- 1. Movie with the highest average rating
SELECT
    m.title,
    AVG(r.rating) AS avg_rating,
    COUNT(r.rating) AS num_ratings
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title
HAVING COUNT(r.rating) > 10 
ORDER BY avg_rating DESC
LIMIT 1;

-- 2. Top 5 genres with highest average rating
SELECT
    g.name AS genre,
    AVG(r.rating) AS avg_rating,
    COUNT(r.rating) AS num_ratings
FROM genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN ratings r ON mg.movie_id = r.movie_id
GROUP BY g.genre_id, g.name
ORDER BY avg_rating DESC
LIMIT 5;

-- 3. Director with most movies
SELECT
    director,
    COUNT(movie_id) AS movie_count
FROM movies
WHERE director IS NOT NULL AND director != 'N/A'
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

-- 4. Average rating of movies released each year
SELECT
    m.release_year,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year DESC;