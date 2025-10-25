DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movies;


CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY, 
    title VARCHAR(255) NOT NULL,
    imdb_id VARCHAR(20),
    release_year INTEGER,
    director VARCHAR(255),
    plot TEXT,
    box_office_revenue BIGINT 
);


CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

CREATE TABLE ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    rated_at DATETIME NOT NULL, 
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
);

CREATE INDEX idx_ratings_movie_id ON ratings (movie_id);
CREATE INDEX idx_movies_release_year ON movies (release_year);
CREATE INDEX idx_movies_director ON movies (director);