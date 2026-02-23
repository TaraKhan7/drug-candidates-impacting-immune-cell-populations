import streamlit as st
import sqlite3
import pandas as pd

from load_data import load_data
from initial_analysis import initial_analysis
from statistical_analysis import statistical_analysis
from subset_analysis import subset_analysis



# Run part 1: Load data and create database
load_data()
# Run part 2: Initial Analysis
initial_analysis()
# Run part 3: Statistical Analysis
statistical_analysis()
# Run part 4: Subset Analysis
project_count, response_count, sex_count = subset_analysis()



st.title("Analysis Results Dashboard")

st.subheader("Cell Type Frequency by Sample")
connection = sqlite3.connect("cell-count.db")


df = pd.read_sql("SELECT * FROM Summary", connection)
st.dataframe(df)

st.subheader("Melanoma PBMC Samples Treated with Miraclib Cell Type Frequency by Response")
st.image(["boxplot_yes.png","boxplot_no.png"], width="content")

st.subheader("Melanoma PBMC Samples Treated with Miraclib Project Distribution")
st.dataframe(project_count)

st.subheader("Melanoma PBMC Samples Treated with Miraclib Subject Response Distribution")
st.dataframe(response_count)

st.subheader("Melanoma PBMC Samples Treated with Miraclib Subject Sex Distribution")
st.dataframe(sex_count)
