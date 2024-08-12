import streamlit as st

st.title("Trung tam tin hoc")
st.subheader("How to run streamlit app")

menu = ["Home", "About"]
choice = st.sidebar.selectbox('Menu', menu)
if choice == 'Home':
    st.subheader('Streamlit From Windows')
elif choice == 'About':
    st.subheader("[Trung tam tin hoc](https://csc.edu.vn)")