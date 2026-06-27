import streamlit as st
from youtube_project import main

st.title("YouTube Video Q&A")

video_id = st.text_input("Enter Video ID")
query = st.text_input("Ask a Question")

if st.button("Get Answer"):
    answer = main(video_id, query)
    st.write(answer)