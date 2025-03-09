import streamlit as st
import json

# File to store data
DATA_FILE = "budget_data.json"

# Load existing data or initialize an empty list
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a transaction
def add_transaction(date, category, amount, trans_type):
    data = load_data()
    transaction = {"date": date, "category": category, "amount": amount, "type": trans_type}
    data.append(transaction)
    save_data(data)
    st.success("Transaction added successfully!")

# View transactions
def view_transactions():
    data = load_data()
    if data:
        st.write("### Transaction History")
        st.table(data)
    else:
        st.info("No transactions recorded yet.")

# Get balance
def get_balance():
    data = load_data()
    income = sum(trans["amount"] for trans in data if trans["type"] == "Income")
    expense = sum(trans["amount"] for trans in data if trans["type"] == "Expense")
    balance = income - expense
    
    st.write("### Financial Summary")
    st.write(f"*Total Income:* ${income:.2f}")
    st.write(f"*Total Expenses:* ${expense:.2f}")
    st.write(f"*Current Balance:* ${balance:.2f}")

# Delete transaction
def delete_transaction(index):
    data = load_data()
    if 0 <= index < len(data):
        deleted = data.pop(index)
        save_data(data)
        st.success(f"Deleted transaction: {deleted}")
    else:
        st.error("Invalid transaction index.")

# Streamlit UI
st.title("💰 Personal Budget Tracker")

# Add Transaction
st.sidebar.header("Add New Transaction")
date = st.sidebar.text_input("Enter date (YYYY-MM-DD)")
category = st.sidebar.text_input("Enter category")
amount = st.sidebar.number_input("Enter amount", min_value=0.01)
trans_type = st.sidebar.selectbox("Select type", ["Income", "Expense"])
if st.sidebar.button("Add Transaction"):
    add_transaction(date, category, amount, trans_type)

# View Transactions
view_transactions()

# Display Balance
get_balance()

# Delete Transaction
st.sidebar.header("Delete Transaction")
data = load_data()
if data:
    index = st.sidebar.number_input("Enter transaction index to delete", min_value=0, max_value=len(data)-1, step=1)
    if st.sidebar.button("Delete Transaction"):
        delete_transaction(index)