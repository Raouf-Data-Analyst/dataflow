# streamlit_app.py

import pandas_gbq
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd 


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
pandas_gbq.context.credentials = credentials

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
df = pandas_gbq.read_gbq("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10")

# Print results.
st.write("Some wise words from Shakespeare:")
for row in rows:
    st.write("✍️ " + row['word'])
