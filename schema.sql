-- Drop tables in order of dependency to ensure a clean run
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movies;

-- Store core movie info.
-- We use the movie_id from the CSV as the Primary Key.
CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY, -- CRITICAL FIX: Use the ID from MovieLens
    title VARCHAR(255) NOT NULL,
    imdb_id VARCHAR(20),
    release_year INTEGER,
    director VARCHAR(255),
    plot TEXT,
    box_office_revenue BIGINT -- Stored as a number for analysis
);

-- Store unique genre names
CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Joining table for the many-to-many relationship
CREATE TABLE movie_genres (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

-- Store ratings, linked to the movies table
CREATE TABLE ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    rated_at DATETIME NOT NULL, -- Use DATETIME for the converted timestamp
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
);

-- Add indexes for faster query performance
CREATE INDEX idx_ratings_movie_id ON ratings (movie_id);
CREATE INDEX idx_movies_release_year ON movies (release_year);
CREATE INDEX idx_movies_director ON movies (director);