"""Browse page"""

import streamlit as st
from datetime import datetime
from db.database import get_all_media, get_unique_values, save_collection, get_collection_names

POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w300'

st.title('Browse')

current_year = datetime.now().year
min_year_value=1931

# load filter options from the database
genres = get_unique_values('genres')
cast = get_unique_values('cast')
directors = get_unique_values('directors')

# render sidebar filters
st.sidebar.title('Filters')
# map friendly UI labels to the actual values stored in the database
type_options = {'All': None, 'Movie': 'movie', 'TV Show': 'tv_show'}

# render the radio button in the sidebar — the user sees "All", "Movie", "TV Show"
media_type_label = st.sidebar.radio('Type', list(type_options.keys()))

# look up the actual database value for the selected label
# e.g. "TV Show" → "tv_show", "All" → None
media_type = type_options[media_type_label]
selected_genre = st.sidebar.selectbox('Genres', ['All'] + genres)
selected_cast = st.sidebar.selectbox('Actor/Actress', ['All'] + cast)
selected_director = st.sidebar.selectbox('Director', ['All'] + directors)

year_range = st.sidebar.slider('Year', min_value=min_year_value, max_value=current_year, value=(min_year_value, current_year))

min_rating = st.sidebar.slider('Rating', min_value=0.0, max_value=10.0, step=0.1, value=0.0)

if selected_genre == 'All':
    selected_genre = None
if selected_cast == 'All':
    selected_cast = None
if selected_director == 'All':
    selected_director = None

filters = {
    'media_type': media_type,
    'genres': selected_genre,
    'cast': selected_cast,
    'directors': selected_director,
    'imdb_rating': min_rating,
    'year_min': year_range[0],
    'year_max': year_range[1]
    }

results = get_all_media(filters) 

# Poster Grid
st.write(f'{len(results)} titles found') # After fetching results, show how many titles were found
cols = st.columns(6)

for index, row in enumerate(results):
    col = cols[index % 6] # cycle through columns 0,1,2,3,4,5,0,1,2...
    with col:
        if row['poster_path'] is None:
            st.image('https://zoltanlederer.com/assets/poster_placeholder.png')
        else:
            st.image(POSTER_BASE_URL + row['poster_path'])

        st.caption(row['title'])
        st.caption(f"⭐ {row['imdb_rating'] or 'N/A'} · {int(row['year']) if row['year'] else 'N/A'}")
