import streamlit as st
import pandas as pd
import random


st.set_page_config(initial_sidebar_state="collapsed",page_title="Playground")
# Side bar with dark mode toggle and contribute button

def generate_random_votes(num_voters, num_candidates):
    print("Generating random votes")
    votes = []
    for i in range(num_voters):
        vote = []
        for j in range(num_candidates):
            vote.append(random.randint(0, 1))  # Randomly generate 0 or 1 as a vote
        votes.append(vote)
    df = pd.DataFrame(votes, columns=[f"Candidate {i+1}" for i in range(num_candidates)])
    print(df)
    return df

# Inside the button click callback
def generate_random_votes_callback():
    votes_df = generate_random_votes(st.session_state.num_voters, st.session_state.num_candidates)
    st.session_state.votes_df = votes_df

def generate_random_params():
    print("Generating random params")
    st.session_state.num_candidates = random.randint(1, 100)
    st.session_state.num_voters = random.randint(1, int(1e8))
    st.session_state.group_size = random.randint(1, st.session_state.num_voters)
    st.session_state.pop("votes_df", None)

def reset_params():
    st.session_state.num_candidates = 1
    st.session_state.num_voters = 1
    st.session_state.group_size = 1
    st.session_state.pop("votes_df", None)
    #placeholder.empty()

st.title("Unanimous Voting Algorithm using Homomorphic Encryption")
st.markdown("[![Contribute](https://img.shields.io/badge/Contribute-on%20GitHub-brightgreen)](Contribute)")
st.divider()
st.header("Playground")

if 'num_voters' not in st.session_state:
    st.session_state.num_voters = 1
if 'num_candidates' not in st.session_state:
    st.session_state.num_candidates = 1
if 'group_size' not in st.session_state:
    st.session_state.group_size = 1

num_voters = st.number_input("Select the number of voters (n)", min_value=1, max_value=int(1e8), value=st.session_state.num_voters)
num_candidates = st.number_input("Select the number of candidates (m)", min_value=1, max_value=int(1e2), value=st.session_state.num_candidates)
group_size = st.number_input("Select the group size (x)", min_value=1, max_value=int(1e8), value=st.session_state.group_size)

col1, col2, col3 = st.columns(3)
col1.button(label="Generate Random Votes", key="generate_random_votes", help="Generate random votes", on_click=generate_random_votes_callback)
col2.button(label="Reset Params", key="reset_params", help="Reset parameters", on_click=reset_params)

# Display the table below the buttons
placeholder = st.empty()
if 'votes_df' in st.session_state:
    with placeholder.container():
        st.subheader("Votes")
        st.table(st.session_state.votes_df)
        col3, col4,col5 = st.columns(3)
        col3.button(label="Compute Results", key="compute_results", help="Compute the results")
        col4.download_button(label="Download Vote Data", key="download_results", help="Download the results", data=st.session_state.votes_df.to_csv(index=False), file_name="votes.csv")
        col5.empty()
