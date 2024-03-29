import streamlit as st
st.title("Results")
st.divider()

placeholder = st.empty()


if "results" not in st.session_state:
    placeholder.markdown("## Nothing here")