import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API configuration
API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None

def fetch_expenses():
    try:
        response = requests.get(f"{API_BASE_URL}/expenses")
        if response.status_code == 200:
            st.session_state.expenses = response.json()
        else:
            st.error("Failed to fetch expenses")
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server. Make sure the backend is running.")

def fetch_analytics():
    try:
        category_response = requests.get(f"{API_BASE_URL}/analytics/category-totals")
        monthly_response = requests.get(f"{API_BASE_URL}/analytics/monthly-totals")
        
        category_data = category_response.json() if category_response.status_code == 200 else []
        monthly_data = monthly_response.json() if monthly_response.status_code == 200 else []
        
        return category_data, monthly_data
    except requests.exceptions.RequestException:
        return [], []

def add_expense(expense_data):
    try:
        response = requests.post(f"{API_BASE_URL}/expenses", json=expense_data)
        if response.status_code == 200:
            st.success("Expense added successfully!")
            fetch_expenses()
            return True
        else:
            st.error("Failed to add expense")
            return False
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")
        return False

def update_expense(expense_id, expense_data):
    try:
        response = requests.put(f"{API_BASE_URL}/expenses/{expense_id}", json=expense_data)
        if response.status_code == 200:
            st.success("Expense updated successfully!")
            fetch_expenses()
            st.session_state.editing_id = None
            return True
        else:
            st.error("Failed to update expense")
            return False
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")
        return False

def delete_expense(expense_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/expenses/{expense_id}")
        if response.status_code == 200:
            st.success("Expense deleted successfully!")
            fetch_expenses()
            return True
        else:
            st.error("Failed to delete expense")
            return False
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")
        return False

# Main app
def main():
    st.title("💰 Personal Expense Tracker")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add Expense", "View Expenses", "Analytics"])
    
    # Fetch data
    fetch_expenses()
    
    if page == "Add Expense":
        show_add_expense_form()
    elif page == "View Expenses":
        show_expenses_list()
    elif page == "Analytics":
        show_analytics()

def show_add_expense_form():
    st.header("Add New Expense" if st.session_state.editing_id is None else "Edit Expense")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input(
                "Description *",
                value=next((exp['description'] for exp in st.session_state.expenses 
                          if exp['id'] == st.session_state.editing_id), ""),
                placeholder="What did you spend on?"
            )
            amount = st.number_input(
                "Amount ($) *", 
                min_value=0.0, 
                step=0.01,
                value=float(next((exp['amount'] for exp in st.session_state.expenses 
                                if exp['id'] == st.session_state.editing_id), 0.0))
            )
        
        with col2:
            category = st.selectbox(
                "Category",
                ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Other"],
                index=0
            )
            date = st.date_input(
                "Date *",
                value=datetime.now().date()
            )
        
        submitted = st.form_submit_button(
            "Update Expense" if st.session_state.editing_id else "Add Expense"
        )
        
        if submitted:
            if not description or amount <= 0:
                st.error("Please fill in all required fields with valid data")
                return
            
            expense_data = {
                "description": description,
                "amount": float(amount),
                "category": category,
                "date": date.isoformat()
            }
            
            if st.session_state.editing_id:
                success = update_expense(st.session_state.editing_id, expense_data)
            else:
                success = add_expense(expense_data)
            
            if success:
                st.rerun()
    
    if st.session_state.editing_id:
        if st.button("Cancel Edit"):
            st.session_state.editing_id = None
            st.rerun()

def show_expenses_list():
    st.header("Your Expenses")
    
    if not st.session_state.expenses:
        st.info("No expenses found. Add your first expense!")
        return
    
    # Display statistics
    total_spent = sum(expense['amount'] for expense in st.session_state.expenses)
    st.metric("Total Expenses", f"${total_spent:.2f}")
    
    # Expenses table
    df = pd.DataFrame(st.session_state.expenses)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['amount'] = df['amount'].apply(lambda x: f"${x:.2f}")
    
    # Display table
    for expense in st.session_state.expenses:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            
            with col1:
                st.write(f"**{expense['description']}**")
            
            with col2:
                st.write(f"${expense['amount']:.2f}")
            
            with col3:
                st.markdown(f"<span style='background-color: #f0f2f6; padding: 4px 8px; border-radius: 12px; font-size: 12px;'>{expense['category']}</span>", 
                          unsafe_allow_html=True)
            
            with col4:
                st.write(expense['date'])
            
            with col5:
                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("✏️", key=f"edit_{expense['id']}"):
                        st.session_state.editing_id = expense['id']
                        st.rerun()
                with col_delete:
                    if st.button("🗑️", key=f"delete_{expense['id']}"):
                        if delete_expense(expense['id']):
                            st.rerun()
            
            st.divider()

def show_analytics():
    st.header("Spending Analytics")
    
    category_data, monthly_data = fetch_analytics()
    
    if not category_data and not monthly_data:
        st.info("No data available for analytics")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending by Category")
        if category_data:
            df_category = pd.DataFrame(category_data)
            fig_pie = px.pie(
                df_category, 
                values='total', 
                names='category',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No category data available")
    
    with col2:
        st.subheader("Monthly Trends")
        if monthly_data:
            df_monthly = pd.DataFrame(monthly_data)
            fig_bar = px.bar(
                df_monthly,
                x='month',
                y='total',
                labels={'total': 'Total Amount', 'month': 'Month'},
                color_discrete_sequence=['#FF4B4B']
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No monthly data available")
    
    # Statistics
    st.subheader("Summary Statistics")
    if st.session_state.expenses:
        total = sum(exp['amount'] for exp in st.session_state.expenses)
        avg_per_expense = total / len(st.session_state.expenses)
        most_expensive = max(st.session_state.expenses, key=lambda x: x['amount'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenses", f"${total:.2f}")
        with col2:
            st.metric("Average per Expense", f"${avg_per_expense:.2f}")
        with col3:
            st.metric("Most Expensive", f"${most_expensive['amount']:.2f}")

if __name__ == "__main__":
    main()
    