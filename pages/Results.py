import streamlit as st
import pandas as pd
import os
from components.nav_page import nav_page
import json
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
    df1 = pd.DataFrame(results["bitmask_rep"],columns=["Bitmask representation"])
    # df1 = df1.style.format({"Bitmask representation": "{:.0f}"})
    # df1["Bitmask representation"] = df1["Bitmask representation"].apply(lambda x: f"{int(x):.0f}")
    st.subheader("BitMasks")

    # bitmask_len=len(str(results["bitmask_rep"][0]))

    if len(results["bitmask_rep"])<100:
        # df = pd.DataFrame(results["bitmask_rep"],columns=["Bitmask representation"])
        st.table(df1)
    else:
        st.warning("Bitmask representation is too large to display. Download the csv file to view the complete representation")
        # col4.download_button(label="Download Vote Data", key="download_results", help="Download the results", data=st.session_state.votes_df.to_csv(index=False), file_name="votes.csv")
        # st.button("Download BitMasks", on_click=st.download_button, args=(df.to_csv(index=False), "bitmasks.csv", "Download BitMasks"), help="Download the bitmasks as a csv file")
        csv_data = df1.to_csv(index=False)

        st.download_button(label="Download Bitmasks",
        key="download_bitmasks",
        help="Download the bitmasks as a CSV file",
        data=csv_data,
        file_name="bitmasks.csv")

    st.subheader("Performance")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Time", results["time"])
    col2.metric("Memory", results["memory"])
    # col2.metric("Memory", results["memory"])
    col3.metric("Total Operations", results["total_ops"])
    st.subheader("Graphs")
    with open("results.json","r") as f:
        data = json.load(f)
    chart_data =[]
    for elem in data:
        chart_data.append({
            "No_of_Voters":elem["num_voters"],
            "No_of_Candidates":elem["num_candidates"],
            "Group_Size":elem["group_size"],
            "Time":float(elem["time"][:-3]),
            "Memory":float(elem["memory"][:-3]),
            "Total_Operations":elem["total_ops"],
            "bitmask_len":elem["bitmask_len"]

        })
    st.subheader("Variation with No_of_Voters")
       #elements all values where  m,x is the same as the current results
    n_data = [elem for elem in chart_data if elem["No_of_Candidates"]==results["num_candidates"] and elem["Group_Size"]==results["group_size"]]
    if len(n_data)>1:
        df = pd.DataFrame(n_data)
        st.line_chart(data = df[["No_of_Voters","Time"]].set_index("No_of_Voters"),y="Time")
        st.line_chart(data = df[["No_of_Voters","Memory"]].set_index("No_of_Voters"),y="Memory")
        st.line_chart(data = df[["No_of_Voters","Total_Operations"]].set_index("No_of_Voters"),y="Total_Operations")
    else:
        st.warning("Not enough data to plot graphs for variation with n ,vary n for the same m and x you entered now to see the graphs")

    st.subheader("Variation with No_of_Candidates")
    #flter out the data with same n and x
    m_data = [elem for elem in chart_data if elem["No_of_Voters"]==results["num_voters"] and elem["Group_Size"]==results["group_size"]]
    
    if len(m_data)>1:
        df = pd.DataFrame(m_data)
        st.line_chart(df[["No_of_Candidates","Time"]].set_index("No_of_Candidates"), y="Time")
        st.line_chart(df[["No_of_Candidates","Memory"]].set_index("No_of_Candidates"), y="Memory")
        st.line_chart(df[["No_of_Candidates","Total_Operations"]].set_index("No_of_Candidates"), y="Total_Operations")
        st.line_chart(df[["No_of_Candidates","bitmask_len"]].set_index("No_of_Candidates"), y="bitmask_len")

    else:
        st.warning("Not enough data to plot graphs for variation with m ,vary m for the same n and x you entered now to see the graphs")

    st.subheader("Variation with Group_Size")
    #flter out the data with same n and m
    x_data = [elem for elem in chart_data if elem["No_of_Voters"]==results["num_voters"] and elem["No_of_Candidates"]==results["num_candidates"]]
    if len(x_data)>1:
        df = pd.DataFrame(x_data)
        st.line_chart(df[["Group_Size","Time"]].set_index("Group_Size"), y="Time")
        st.line_chart(df[["Group_Size","Memory"]].set_index("Group_Size"), y="Memory")
        st.line_chart(df[["Group_Size","Total_Operations"]].set_index("Group_Size"), y="Total_Operations")
        st.line_chart(df[["Group_Size","bitmask_len"]].set_index("Group_Size"), y="bitmask_len")
    else:
        st.warning("Not enough data to plot graphs for variation with x ,vary x for the same n and m you entered now to see the graphs")

         
        
        
st.button("Clear Result History", on_click=clear_results_history)
st.page_link(label="Go back to playground",page="Playground.py",icon="🔙")