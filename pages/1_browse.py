"""Browse page"""

import streamlit as st
from datetime import datetime
from db.database import get_all_media, get_unique_values, save_collection, get_collection_names

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

rate_range = st.sidebar.slider('Rating', min_value=0.0, max_value=10.0, step=0.1, value=(0.0, 10.0))

# get_all_media({})