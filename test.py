import streamlit as st
import pandas as pd
import random
import json
import os
import time
from components.nav_page import nav_page
from lightphe import LightPHE
from memory_profiler import memory_usage


st.set_page_config(initial_sidebar_state="collapsed")



def generate_random_votes(num_voters, num_candidates):
    print("Generating random votes")
    # Here we are deciding the winners randomly with a prob of 0.5
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

    df = pd.DataFrame(votes, columns=[f"Candidate {i+1}" for i in range(num_candidates)])
    print(df)
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
    results = {}

    start_time = time.time()
    # Get memory usage before the code section
    mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)

    #add to results.json if not exists create it
    #add the results to the json file
    results['n'] = st.session_state.num_voters
    results['m'] = st.session_state.num_candidates
    results['x'] = st.session_state.group_size

    algo="Paillier"
    cs = LightPHE(algorithm_name = algo)
    bitdiff = int(results['x'].bit_length())
    votes = st.session_state.votes_df.values.tolist()
    enc_votes = []
    for j in range(votes):
        curval=0
        if votes[j]==1:
            curval = curval | (1<<(j*bitdiff)) #! the j-1 is removed because j is zero-index here unlike space_opt.py

        encrypted = cs.encrypt(curval)
        enc_votes.append(encrypted)

    # Unity element in this scenario is when one votes for all the candidates
    unity_elem = 0
    for i in range(0, results['m']):
        unity_elem = unity_elem | (1<<(i*bitdiff))
    unity_elem = cs.encrypt(unity_elem)

    # Here we are taking the sum of all the votes but within the constraints of group size and then decrypting it to get the result
    while(len(enc_votes)>1):
        last=0
        while(len(enc_votes)%results['x']!=0):
            enc_votes.append(unity_elem)
        group_votes = []
        while(last<len(enc_votes)):
            sumvote = cs.encrypt(0)
            for i in range(last,min(last+results['x'],len(enc_votes))):
                sumvote = sumvote + enc_votes[i]

            # Now this group vote is sent to the central server to decrypt and reencrypt
            # Computation in the central server
                
            decrypted_vote = cs.decrypt(sumvote)
            updated_vote = 0

            for i in range(0,results['m']):
                val=0
                for j in range(0,bitdiff):
                    if decrypted_vote & (1<<(i*bitdiff+j)):
                        val += (1<<j)
                if val==results['x']:
                    updated_vote = updated_vote | (1<<(i*bitdiff))
            
            updated_vote = cs.encrypt(updated_vote)
            
            group_votes.append(updated_vote)
            last += results['x']

        enc_votes = group_votes
    # This will be the final result after the computation
    decrypted_vote = cs.decrypt(votes[0])

    final_winners = []
    for i in range(0,results['m']):
        if decrypted_vote & (1<<(i*bitdiff)):
            final_winners.append(i+1)
    
    mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)
    end_time = time.time()
    # print(final_winners)

    results = {
        "winners":final_winners,
        "time":end_time - start_time,
        "memory":mem_usage_after - mem_usage_before        
    } 
    st.session_state.results = results

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
    nav_page("Results",timeout_secs=3)





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