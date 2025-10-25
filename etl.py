import pandas as pd
import requests
from sqlalchemy import create_engine, text
import time
import re
import logging
import sqlite3  


API_KEY = "2d16b56"  
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_year_from_title(title):
    """Extracts the release year from a MovieLens title (e.g., 'Toy Story (1995)')"""
    match = re.search(r'\((\d{4})\)$', title)
    if match:
        year = match.group(1)
        title = title.replace(f'({year})', '').strip()
        return title, year
    return title, None

def clean_box_office(value):
    """Converts OMDb BoxOffice string (e.g., '$1,234,567') to integer"""
    if pd.isna(value) or value == 'N/A':
        return None
    try:
        return int(str(value).replace('$', '').replace(',', ''))
    except ValueError:
        return None

def fetch_omdb_data(title, year):
    """Fetch data from OMDb API using both title and year for accuracy"""
    params = {'t': title, 'apikey': API_KEY}
    if year:
        params['y'] = year
    
    try:
        res = requests.get("http://www.omdbapi.com/", params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
        if data.get("Response") == "True":
            return {
                "director": data.get("Director"),
                "plot": data.get("Plot"),
                "box_office": clean_box_office(data.get("BoxOffice")),
                "imdb_id": data.get("imdbID"),
                "release_year": data.get("Year")
            }
    except requests.exceptions.RequestException as e:
        logging.warning(f"API call failed for {title} ({year}): {e}")
        
    logging.warning(f"Movie not found in OMDb: {title} ({year})")
    return {"director": None, "plot": None, "box_office": None, "imdb_id": None, "release_year": year}

# --- EXTRACT ---
logging.info("Starting EXTRACT phase...")
try:
    movies_df = pd.read_csv("movies.csv")
    ratings_df = pd.read_csv("ratings.csv")
    logging.info(f"Loaded {len(movies_df)} movies and {len(ratings_df)} ratings.")
except FileNotFoundError:
    logging.error("movies.csv or ratings.csv not found.")
    exit()

# --- TRANSFORM ---
logging.info("Starting TRANSFORM phase...")
enriched_data = []
all_genres = set()
movie_genres_list = []

logging.info(f"Enriching {len(movies_df)} movies from OMDb...")
movies_df = movies_df.head(500) 
logging.info(f"Processing a sample of {len(movies_df)} movies to stay under API limits.")

for _, row in movies_df.iterrows():
    movie_id = row["movieId"]
    original_title = row["title"]
    
    clean_title, year = extract_year_from_title(original_title)
    info = fetch_omdb_data(clean_title, year)
    
    enriched_data.append({
        "movie_id": movie_id,
        "title": clean_title,
        "director": info["director"],
        "plot": info["plot"],
        "box_office_revenue": info["box_office"],
        "imdb_id": info["imdb_id"],
        "release_year": info.get("release_year") or year
    })
    
    genres = row["genres"].split('|')
    for genre_name in genres:
        if genre_name != "(no genres listed)":
            all_genres.add(genre_name)
            movie_genres_list.append({"movie_id": movie_id, "genre_name": genre_name})

final_movies_df = pd.DataFrame(enriched_data)

# 2. Transform Genres
genres_df = pd.DataFrame(sorted(list(all_genres)), columns=['name'])
genres_df['genre_id'] = genres_df.index + 1
genre_map = {name: gid for gid, name in zip(genres_df['genre_id'], genres_df['name'])}

movie_genres_map_df = pd.DataFrame(movie_genres_list)
movie_genres_map_df['genre_id'] = movie_genres_map_df['genre_name'].map(genre_map)
final_movie_genres_df = movie_genres_map_df[['movie_id', 'genre_id']].dropna()

# 3. Transform Ratings
ratings_df['rated_at'] = pd.to_datetime(ratings_df['timestamp'], unit='s')
ratings_df = ratings_df.rename(columns={'userId': 'user_id', 'movieId': 'movie_id'})
final_ratings_df = ratings_df[['user_id', 'movie_id', 'rating', 'rated_at']]


logging.info("Starting LOAD phase...")

try:
    db_path = DB_URL.replace("sqlite:///", "") # Getting 'movies.db' from the URL
    with open("schema.sql", 'r') as f:
        schema_script = f.read()
    
    con = sqlite3.connect(db_path)
    con.executescript(schema_script)
    con.commit()
    con.close()
    logging.info("Database schema applied.")
except Exception as e:
    logging.error(f"Failed to apply schema: {e}")
    exit() 

# 2. Load data using pandas and SQLAlchemy engine
try:
    final_movies_df.to_sql("movies", con=engine, if_exists="append", index=False)
    logging.info(f"Loaded {len(final_movies_df)} records into 'movies'.")

    genres_df.to_sql("genres", con=engine, if_exists="append", index=False)
    logging.info(f"Loaded {len(genres_df)} records into 'genres'.")

    final_movie_genres_df.to_sql("movie_genres", con=engine, if_exists="append", index=False)
    logging.info(f"Loaded {len(final_movie_genres_df)} records into 'movie_genres'.")

    processed_movie_ids = final_movies_df['movie_id'].unique()
    final_ratings_df = final_ratings_df[final_ratings_df['movie_id'].isin(processed_movie_ids)]
    
    final_ratings_df.to_sql("ratings", con=engine, if_exists="append", index=False)
    logging.info(f"Loaded {len(final_ratings_df)} records into 'ratings'.")

    logging.info("✅ ETL process completed successfully!")
except Exception as e:
    logging.error(f"Data loading failed: {e}")