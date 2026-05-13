# Media Library Browser

> 🚧 Work in progress

A Streamlit-based media browser for exploring a personal movie and TV show library.

## Features

- Browse 3,000+ movies and TV shows with poster images fetched from TMDB
- Filter by genre, actor, year, rating, or keyword
- Create and manage named collections
- Import from IMDB or Plex, export any list to CSV
- Runs locally in the browser at `localhost:8501`
- Sample dataset deployed on Streamlit Community Cloud for portfolio demonstration

## Requirements

- Python 3.10+
- streamlit
- requests

## Installation & Usage

Coming soon.

## Project Structure

```
media-library-browser/
│
├── app.py                  # entry point — Streamlit runs this
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── .gitkeep            # keeps the folder in Git without exposing the database
│
├── db/
│   └── database.py         # all database queries live here
│
├── pages/                  # Streamlit multipage folder
│   ├── 1_browse.py         # Browse page
│   └── 2_collections.py    # Collections page
│
└── utils/
    └── helpers.py          # small reusable functions
```