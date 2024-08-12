import streamlit as st
import pandas as pd
import subprocess
import sys

st.title("Trung tam tin hoc")
st.subheader("How to run streamlit app")

menu = ["Home", "About", "Hotel Comments", "Hotel Comments Recommendation"]
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Home':
    st.subheader('Streamlit From Windows')
elif choice == 'About':
    st.subheader("Trung tam tin hoc")
elif choice == 'Hotel Comments':
    st.subheader("hotel_comments")
    hotel_comments = pd.read_csv("hotel_comments_6.csv")
    st.write(hotel_comments)
elif choice == 'Hotel Comments Recommendation':
    st.subheader("hotel_comments_recommendation")
    subprocess.run([f"{sys.executable}", "cosin_gensim.py"])
