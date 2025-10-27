#  Movie Data Pipeline

- A simple data pipeline that ingests MovieLens data, enriches it via OMDb API, and loads it into a database for analysis.

# Prerequisites

- Python 3.8 or above
- SQLite DB Browser
- OMDb API key (free from [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx))


# Steps to Run

1. **Clone the repository**

git clone <repository_url>
cd movie-data-pipeline

2. **Install dependencies**

pip install -r requirements.txt

3. **Set your OMDb API key**

Open etl.py and update:
API_KEY = "****"
DB_URL = "sqlite:///movies.db"

4. **Run the ETL pipeline**

python etl.py
This will create movies.db and populate it with enriched movie and rating data.

5. **Run SQL queries**

Open the SQLite shell:Execute queries from queries.sql to analyze the data.

Design Choices and Assumptions

Database: I chose SQLite because it's serverless and file-based, making the project easy to set up and run without any external database server.

Data Model: This involved creating a genres table and a movie_genres joining table to correctly handle the one-to-many relationship (one movie can have multiple genres). This is far more efficient for querying than storing genres as a single text string.

API Matching: The OMDb API was unreliable when using the full MovieLens title (e.g., "Toy Story (1995)"). I solved this by using a regular expression to extract the clean title ("Toy Story") and the year ("1995"), then querying the API with both parameters for a much more accurate match.

Assumption: The script assumes movies.csv and ratings.csv are in the same root directory.

Challenges Faced

API Rate Limits: The free OMDb API has a daily request limit. The full dataset (9,000+ movies) is too large.

SQL Execution Error: Python's SQLAlchemy library could not execute the entire schema.sql file at once, as it contains multiple CREATE and DROP statements.
