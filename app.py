import streamlit as st
import sqlite3
import pandas as pd

from load_data import load_data
from initial_analysis import initial_analysis
from statistical_analysis import statistical_analysis
from subset_analysis import subset_analysis


# Run part 1: Load data and create database
load_data()
print("Database loaded")
# Run part 2: Initial Analysis
initial_analysis()
print("Initial Analysis Complete")
# Run part 3: Statistical Analysis
results = statistical_analysis()
print("Statistical Analysis Complete")
# Run part 4: Subset Analysis
project_count, response_count, sex_count = subset_analysis()
print("Subset Analysis Complete")


print("Creating Dashboard")
st.title("Analysis Results Dashboard")

st.subheader("Cell Type Frequency by Sample")
connection = sqlite3.connect("cell-count.db")


df = pd.read_sql("SELECT * FROM Summary", connection)
st.dataframe(df)

st.subheader(
    "Melanoma PBMC Samples Treated with Miraclib Cell Type Frequency by Response"
)
st.image(["boxplot_yes.png", "boxplot_no.png"], width="content")

st.subheader("T-test Comparison Results")
st.dataframe(results)
st.text(
    "Cd4 t-cells have a significant difference in relative frequencies between responders and non-responders as indicated by a independent-samples"
    " t-test. There was a statistically significant difference between responders (yes) and non-responders (no) where t(1966)=2.0894 and p=0.005."
)
st.text(
    "The other four cell types had no significant difference in relative frequencies between responders and non-responders."
)


st.subheader("Melanoma PBMC Samples Treated with Miraclib Project Distribution")
st.dataframe(project_count)

st.subheader(
    "Melanoma PBMC Samples Treated with Miraclib Subject Response Distribution"
)
st.dataframe(response_count)

st.subheader("Melanoma PBMC Samples Treated with Miraclib Subject Sex Distribution")
st.dataframe(sex_count)

print("Dashboard created")
