import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
st.title("Results")
st.divider()

placeholder = st.empty()

if "results" not in st.session_state:
    # Display an image
    placeholder.page_link(label="Nothing Here ! Go back to playground and compute results to see the output here",page="Home.py",icon="❌")