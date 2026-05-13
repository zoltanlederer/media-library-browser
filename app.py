"""This is the entry point — the file Streamlit runs directly. It sets up the app and loads the pages."""

import streamlit as st
from db.database import create_collections_table, get_connection

st.set_page_config(
    page_title="Media Library Browser",
    page_icon="🎬",
    layout="wide"
)

st.title('Media Library Browser')
st.write('Browse your personal collection of movies and TV shows. Filter by genre, actor, year, or rating.')

conn = get_connection()
create_collections_table(conn)
conn.close()