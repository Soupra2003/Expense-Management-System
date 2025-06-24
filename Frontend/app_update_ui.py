import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")

    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        expenses = []

        for i in range(len(existing_expenses)):
            col1, col2, col3 = st.columns(3)
            amount = existing_expenses[i]['amount']
            category = existing_expenses[i]["category"]
            notes = existing_expenses[i]["notes"]

            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        st.markdown("---")
        
        new_col1, new_col2, new_col3 = st.columns(3)
        with new_col1:
            new_amount = st.number_input(
                "Amount", min_value=0.0, step=1.0, key="new_amount"
            )
        with new_col2:
            new_category = st.selectbox(
                "Category", options=categories, key="new_category"
            )
        with new_col3:
            new_notes = st.text_input("Notes", key="new_notes")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if new_amount > 0:
                expenses.append({
                    'amount': new_amount,
                    'category': new_category,
                    'notes': new_notes
                })

            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")

                # Clear the new input fields only
                if "new_amount" not in st.session_state:
                    st.session_state["new_amount"] = 0.0
                if "new_category" not in st.session_state:
                    st.session_state["new_category"] = categories[0]
                if "new_notes" not in st.session_state:
                    st.session_state["new_notes"] = ""
            else:
                st.error("Failed to update expenses.")
