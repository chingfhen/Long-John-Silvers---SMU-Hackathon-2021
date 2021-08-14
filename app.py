import streamlit as st
import os
import encoders
import utils
import preprocess
import datastore
import yaml

from datetime import date
import pandas as pd
def query(query: str,  top_k = 3):
    today = date.today()
    date_range = list(pd.date_range(start=today,periods=100))
    query_embedding = encoders.bi_encoder.encode(query, show_progress_bar = False)
    hits = datastore.datastore.query_by_embedding(query_embedding,top_k = 10,filters = {"end_date":date_range})   # bi encoder retrieve
    for hit in hits:
        hit.score = encoders.cross_encoder.predict([query,hit.text], show_progress_bar = False)                                          # cross encoder rerank
    return sorted(hits,key = lambda x: x.score, reverse = True)[:top_k]


st.text(query("heritage centre capacity")[0].text)


