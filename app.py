import streamlit as st
from app2 import get_top_n_similar

st.title("Hotel Similarity Search")

user_input = st.text_input("Enter a string:")

if user_input:
    try:
        similar_hotel_ids, similar_scores = get_top_n_similar(user_input)
        st.write(f"The top 5 most similar hotel IDs are: {', '.join(map(str, similar_hotel_ids))}")
        st.write(f"The similarity scores are: {', '.join(map(str, similar_scores))}")
    except ValueError:
        st.write("The input string was not found in the comments data.")
