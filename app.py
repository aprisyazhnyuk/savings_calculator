import streamlit as st
import datetime

st.title("Test App")

today = datetime.date.today()

st.write("Today's date is:")
st.write(today)
