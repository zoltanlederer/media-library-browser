"""Browse page — displays a filterable, sortable grid of movie and TV show posters"""

import streamlit as st
from datetime import datetime
from db.database import get_all_media, get_unique_values, save_collection, get_collection_names

# ── Constants ──────────────────────────────────────────────────────────────
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w300'  # TMDB base URL for poster images
POSTER_PLACEHOLDER = 'https://zoltanlederer.com/assets/poster_placeholder.png'  # fallback image
MIN_YEAR = 1931       # earliest year in the database
RESULTS_PER_PAGE = 24 # number of posters to show per page

# ── Page title ─────────────────────────────────────────────────────────────
st.title('Media Library Browser')
st.write('Browse your personal collection of movies and TV shows. Filter by genre, actor, year, or rating.')

# initialise page number — only sets it to 0 if it doesn't exist yet
if 'page' not in st.session_state:
    st.session_state.page = 0

# ── Load filter options from the database ──────────────────────────────────
# these are loaded once and used to populate the sidebar dropdowns
current_year = datetime.now().year
genres = get_unique_values('genres')
cast = get_unique_values('cast')
directors = get_unique_values('directors')

# ── Sidebar filters ────────────────────────────────────────────────────────
st.sidebar.title('Filters')

# type filter — map friendly labels to database values
type_options = {'All': None, 'Movie': 'movie', 'TV Show': 'tv_show'}
media_type_label = st.sidebar.radio('Type', list(type_options.keys()))
media_type = type_options[media_type_label]  # e.g. "TV Show" → "tv_show", "All" → None

# sort order
sort_options = {
    'Title A-Z': ('title', True),
    'Title Z-A': ('title', False),
    'Year (newest first)': ('year', False),
    'Year (oldest first)': ('year', True),
}
selected_sort = st.sidebar.selectbox('Sort by', sort_options)

# dropdown filters
selected_genre = st.sidebar.selectbox('Genre', ['All'] + genres)
selected_cast = st.sidebar.selectbox('Actor/Actress', ['All'] + cast)
selected_director = st.sidebar.selectbox('Director', ['All'] + directors)

# range filters
year_range = st.sidebar.slider('Year', min_value=MIN_YEAR, max_value=current_year, value=(MIN_YEAR, current_year))
min_rating = st.sidebar.slider('Minimum rating', min_value=0.0, max_value=10.0, step=0.1, value=0.0)

# convert 'All' selections to None so get_all_media() ignores them
if selected_genre == 'All':
    selected_genre = None
if selected_cast == 'All':
    selected_cast = None
if selected_director == 'All':
    selected_director = None

# ── Fetch results ──────────────────────────────────────────────────────────
filters = {
    'media_type': media_type,
    'genres': selected_genre,
    'cast': selected_cast,
    'directors': selected_director,
    'imdb_rating': min_rating,
    'year_min': year_range[0],
    'year_max': year_range[1]
}

# reset to page 0 when filters change
current_filters = (media_type, selected_genre, selected_cast, selected_director, min_rating, year_range, selected_sort)
if 'last_filters' not in st.session_state:
    st.session_state.last_filters = current_filters
if current_filters != st.session_state.last_filters:
    st.session_state.page = 0
    st.session_state.last_filters = current_filters

results = get_all_media(filters) # full list

# sort full results after fetching
sort_key, ascending = sort_options[selected_sort]
results = sorted(results, key=lambda row: row[sort_key] or '', reverse=not ascending)

# slice it for the current page
start = st.session_state.page * RESULTS_PER_PAGE
end = start + RESULTS_PER_PAGE
page_results = results[start:end]
total_pages = len(results) // RESULTS_PER_PAGE

# ── Poster grid ────────────────────────────────────────────────────────────
st.write(f'{len(results)} titles found')
cols = st.columns(6)

for index, row in enumerate(page_results):
    col = cols[index % 6]  # cycle through columns 0,1,2,3,4,5,0,1,2...
    with col:
        if row['poster_path'] is None:
            st.image(POSTER_PLACEHOLDER)
        else:
            st.image(POSTER_BASE_URL + row['poster_path'])
        st.caption(row['title'])
        st.caption(f"⭐ {row['imdb_rating'] or 'N/A'} · {int(row['year']) if row['year'] else 'N/A'}")

# ── Pagination ─────────────────────────────────────────────────────────────
col_prev, col_info, col_next = st.columns([2, 5, 1])

with col_prev:
    if st.button('← Previous', disabled=st.session_state.page == 0):
        st.session_state.page -= 1

with col_info:
    st.markdown(
        f"<p style='text-align: center; margin-top: 6px;'>"
        f"Page {st.session_state.page + 1} of {total_pages + 1}"
        f"</p>",
        unsafe_allow_html=True
    )

with col_next:
    if st.button('Next →', disabled=st.session_state.page >= total_pages):
        st.session_state.page += 1