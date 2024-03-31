import streamlit as st
import pandas as pd
import os


st.set_page_config(initial_sidebar_state="collapsed")

def clear_results_history():
    if os.path.exists("results.json"):
        os.remove("results.json")
        st.session_state.pop("results", None)
        st.toast("Results history cleared", icon="🗑️")
    else:
        st.toast("No results history found", icon="❌")

st.title("Results")
st.divider()

placeholder = st.empty()

if "results" not in st.session_state:
    # Display an image
    placeholder.page_link(label="Nothing Here ! Go back to playground and compute results to see the output here",page="Playground.py",icon="❌")
else:
    results = st.session_state.results
    print(results)
    #display wienners as a table with columns slno and candidate name
    st.subheader("Winners")
    df = pd.DataFrame(results["winners"],columns=["Candidate"])
    st.table(df)
    st.subheader("Performance")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Time", results["time"])
    col2.metric("Memory", results["memory"])
    col3.empty()
st.button("Clear Result History", on_click=clear_results_history)
    