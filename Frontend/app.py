import streamlit as st
from app_update_ui import add_update_tab
from analytics_ui import analytics_tab

st.header("Expense Management System")
st.subheader("Track your Expenses from Now 😁")

tab1, tab2 = st.tabs(['Add/Update', 'Analytics'])

with tab1:
   add_update_tab()
with tab2:
   analytics_tab()