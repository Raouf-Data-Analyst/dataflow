import pandas_gbq
import streamlit as st
from google.oauth2 import service_account
import pandas as pd

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
pandas_gbq.context.credentials = credentials

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query():
    df = pandas_gbq.read_gbq("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10",project_id= "modern-unison-394608")
    return df

df = run_query()

# Print results.
st.write("Some wise words from Shakespeare:")
for index, row in df.iterrows():
    st.write("✍️ " + row['word'])
