import streamlit as st
st.set_page_config(layout="wide")

st.title("Testing the Review Evaluator")


text=st.text_area("Enter a review text to evaluate:",)

rating=st.number_input("Rating", min_value=1, max_value=5, step=1)
st.text_input("Google maps link (optional)")
st.button("Evaluate")

if st.button("Evaluate"):
    if not text:
        st.error("Please enter a review text.")
    elif not rating:
        st.error("Please enter a rating between 1 and 5.")
    else:
        st.write("Evaluating...")
   # Call the evaluation function here and display results

st.button("Clear")

if st.button("Clear"):
    text=""
    rating=0

