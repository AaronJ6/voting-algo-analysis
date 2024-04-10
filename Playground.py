import streamlit as st
import pandas as pd
import random
import json
import os
import time
from components.nav_page import nav_page
from components.confirm import confirm

st.set_page_config(initial_sidebar_state="collapsed")



def generate_random_votes(num_voters, num_candidates):
    print("Generating random votes !!")
    winners = []
    # others = [] #! Removed others as it is unnecessary
    for i in range(0,num_candidates):
        ran=random.randint(0,1)
        if(ran==1):
            winners.append(i+1)
        # else:
        #     others.append(i+1)

    print("winners :", winners)
    votes = []
    for i in range(num_voters):
        vote = []
        for j in range(num_candidates):
            if j in winners:
                vote.append(1)
            else:
                vote.append(random.choice([1,0]))  #! Randomly generate 0 for no and 1 for yes as a vote
        votes.append(vote)
    print("Votes : ",votes)

    df = pd.DataFrame(votes, columns=[f"Candidate {i+1}" for i in range(num_candidates)])
    print(df)
    print(winners)
    return df

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
    st.session_state.pop("results", None)

def compute_results_callback():
    print("computing results")
    results = {
        "winners":["Candidate 1"],
        "time":"100ms",
        "memory":"100MB"
        
    }
    
    st.session_state.results = results
    #add to results.json if not exists create it
    #add the results to the json file
    results['n'] = st.session_state.num_voters
    results['m'] = st.session_state.num_candidates
    results['x'] = st.session_state.group_size
    if os.path.exists("results.json"):
        with open("results.json","r") as f:
            data = json.load(f)
        data.append(results)
        with open("results.json","w") as f:
            json.dump(data,f,indent=4)
    else:   
        with open("results.json","w") as f:
            json.dump([results],f,indent=4)
    st.toast("Results computed successfully . Check the results page for the output",icon="🎉")
    #go to results page using javascript
    nav_page("Results",timeout_secs=3,delay=3000)
  





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
st.session_state.num_voters = num_voters  # Assign input value to session_state variable
num_candidates = st.number_input("Select the number of candidates (m)", min_value=1, max_value=int(1e2), value=st.session_state.num_candidates)
st.session_state.num_candidates = num_candidates  # Assign input value to session_state variable
group_size = st.number_input("Select the group size (x)", min_value=1, max_value=int(1e8), value=st.session_state.group_size)
st.session_state.group_size = group_size  # Assign input value to session_state variable

col1, col2, col3 = st.columns(3)
col1.button(label="Generate Random Votes", key="generate_random_votes", help="Generate random votes", on_click=generate_random_votes_callback)
col2.button(label="Reset Params", key="reset_params", help="Reset parameters", on_click=reset_params)

placeholder = st.empty()
link_placeholder = st.empty()
if 'votes_df' in st.session_state:
    with placeholder.container():
        st.subheader("Votes")
        if st.session_state.num_voters<100:
            st.table(st.session_state.votes_df)
        else:
            st.markdown('''
                        >Table too large to display.Please download the data to view it
                        ''')
        col3, col4, col5 = st.columns(3)
        col3.button(label="Compute Results", key="compute_results", help="Compute the results",on_click=compute_results_callback)
        col4.download_button(label="Download Vote Data", key="download_results", help="Download the results", data=st.session_state.votes_df.to_csv(index=False), file_name="votes.csv")
        col5.empty()
if "results" in st.session_state:
    st.page_link(disabled= "results" not in st.session_state, label="View Results", page="./pages/Results.py",icon="📊")

    

    

