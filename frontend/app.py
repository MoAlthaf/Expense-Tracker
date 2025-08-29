import streamlit as st
import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL="http://localhost:8000"

st.title("Expense Tracker")

tab_1, tab_2 = st.tabs(["Add/Update", "Analytics"])

with tab_1:
    expense_date = st.date_input("Expense Date", datetime.date.today(), label_visibility="collapsed")
    if 'expense_date' not in st.session_state or st.session_state['expense_date'] != str(expense_date):
        response = requests.get(f"{API_URL}/expenses/{expense_date}")
        if response.status_code == 200 and response.json():
            st.session_state['expense'] = response.json()
        else:
            st.session_state['expense'] = []
        st.session_state['expense_date'] = str(expense_date)
    expense = st.session_state['expense']

    categories = ["Food", "Shopping", "Rent", "Entertainment", "Other"]
    
    add_expense= st.button("Add Another Expense")
    if add_expense:
        expense.append({'amount': 0.0, 'category': categories[0], 'notes': ''})
        st.session_state['expense'] = expense

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        updated_expenses = []
        for i in range(len(expense)):
            actual_amount = expense[i]['amount'] if i < len(expense) else 0.0
            actual_category = expense[i]['category'] if i < len(expense) else categories[0]
            actual_notes = expense[i].get('notes', '') if i < len(expense) else ''

            col1,col2,col3=st.columns(3)
            with col1:
                amount = st.number_input(f"Amount {i+1}", min_value=0.0, format="%.2f", key=f"amount_{i}",step=1.0,value=actual_amount,label_visibility="collapsed")
            with col2:
                category = st.selectbox(f"Category {i+1}", options=categories, key=f"category_{i}",index=categories.index(actual_category),label_visibility="collapsed")
            with col3:
                notes = st.text_input(f"Notes {i+1}", key=f"notes_{i}",value=actual_notes,label_visibility="collapsed")
            updated_expenses.append({'expense_date': str(expense_date),'amount': amount, 'category': category, 'notes': notes})


    
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            filtered_expenses = [e for e in updated_expenses if e['amount'] > 0]
            response= requests.post(f"{API_URL}/expenses/{expense_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
                # Refresh session state from backend after successful submit
                response = requests.get(f"{API_URL}/expenses/{expense_date}")
                if response.status_code == 200 and response.json():
                    st.session_state['expense'] = response.json()
                else:
                    st.session_state['expense'] = []
            else:
                st.error("Failed to update expenses.")
with tab_2:
    start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7), key="start_date")
    end_date = st.date_input("End Date", datetime.date.today(), key="end_date")
    if st.button("Get Analytics"):
        response = requests.post(f"{API_URL}/analytics", json={"start_date": str(start_date), "end_date": str(end_date)})
        if response.status_code == 200:
            data = response.json()
            df=pd.DataFrame.from_dict(data,orient='index')
            st.dataframe(df)
            st.title("Expense Breakdown")
            fig_bar=px.bar(df,y="total",title="Expense Breakdown by Category",labels={"index":"Category","total":"Total Amount"})
            st.plotly_chart(fig_bar)
        else:
            st.error("Failed to fetch analytics.")