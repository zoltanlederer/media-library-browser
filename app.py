"""This is the entry point — the file Streamlit runs directly. It sets up the app, loads the pages and defines navigation."""

import streamlit as st
from db.database import create_collections_table, get_connection

st.set_page_config(
    page_title="Media Library Browser",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# create collections table if it doesn't exist yet
conn = get_connection()
create_collections_table(conn)
conn.close()

# define navigation — hides the default auto-generated menu
browse = st.Page('pages/1_browse.py', title='Library', icon='🎬')
collections = st.Page('pages/2_collections.py', title='Collections', icon='📚')

pg = st.navigation([browse, collections])
pg.run()