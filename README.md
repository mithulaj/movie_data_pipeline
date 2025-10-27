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

Design Choices
The following choices were made to optimize for simplicity, data integrity, and efficient API matching:
