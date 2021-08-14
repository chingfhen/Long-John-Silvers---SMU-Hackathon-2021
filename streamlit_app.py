import streamlit as st
import preprocess
import encoders
import datastore
import yaml
from datetime import date
import pandas as pd
from haystack.schema import Document

with open(r'config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

def query(query: str,  top_k = 3, max_words = 30):
    today = date.today()
    date_range = list(pd.date_range(start=today,periods=100))
    query_embedding = encoders.bi_encoder.encode(query, show_progress_bar = False)
    hits = datastore.datastore.query_by_embedding(query_embedding,top_k = 10,filters = {"end_date":date_range})   # bi encoder retrieve
    shortened_hits = []
    for hit in hits:
        shortened_hits.extend(preprocess.split_document(hit,max_words))
    for hit in shortened_hits:
        if not isinstance(hit,Document):
            hit = Document(**hit)
        hit.score = encoders.cross_encoder.predict([query,hit.text], show_progress_bar = False)# cross encoder rerank
    output = []
    for hit in shortened_hits:
        if isinstance(hit,dict):
            continue
        output.append(hit)
    return sorted(output,key = lambda x: x.score, reverse = True)[:top_k]
   
def get_summaries(categories:list):
    today = date.today()
    date_range = list(pd.date_range(start=today,periods=100))
    return datastore.datastore.get_all_documents(config['index'],filters = {"category":categories,"end_date":date_range})     
def prettify(docs):
    if docs[0].meta['name']=="summary":
        return docs[0].text
    output = f"Most likely answer:\n{docs[0].text}\n\nOther possible Answers:\n"
    for i,doc in enumerate(docs[1:]):
        output+=f"{i+1}. {doc.text}\n"
    return output
    
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)
    
st.markdown('<p class="big-font">COVID-19 Rules and Regulations Answerer</p>', unsafe_allow_html=True)

    
category = st.selectbox("Quick Summaries",config["all_categories"])
docs = get_summaries([category])
st.text(prettify(docs))

top_k = st.sidebar.slider("Change number of answers",3,10,3)
max_words = st.sidebar.slider("Change length of answers",10,50,30)


# if st.button('Cinema Summary'):
query_from_user = st.text_input("Not Satisfied? Enter your query here!",value = "")
if query_from_user:
    docs = query(query_from_user,top_k=top_k,max_words = max_words)
    st.text(prettify(docs))
else:
    st.text("")
    

    
