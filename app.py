import streamlit as st
import matplotlib.pyplot as plt
import datetime

class BudgetTracker:
    def __init__(self):
        self.expenses = []
        self.budget_limit = 0

    def set_budget_limit(self, limit):
        self.budget_limit = limit

    def add_expense(self, amount, category):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.expenses.append({'amount': amount, 'category': category, 'date': date})
        self.check_budget()

    def check_budget(self):
        total_expense = sum(expense['amount'] for expense in self.expenses)
        if total_expense > self.budget_limit:
            st.warning("⚠️ You have exceeded your budget limit!")
    
    def plot_expenses(self):
        if not self.expenses:
            st.info("No expenses to plot.")
            return

        categories = [expense['category'] for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(categories, amounts, color='skyblue')
        ax.set_title('Expense Analysis by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount Spent ($)')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

# Initialize the BudgetTracker
tracker = BudgetTracker()

st.title("💰 Personal Budget Tracker")
st.sidebar.header("Set Budget Limit")
budget = st.sidebar.number_input("Enter your budget limit", min_value=0.0, step=10.0)
tracker.set_budget_limit(budget)

st.sidebar.header("Add New Expense")
amount = st.sidebar.number_input("Amount", min_value=0.0, step=1.0)
category = st.sidebar.text_input("Category")
if st.sidebar.button("Add Expense"):
    if category and amount > 0:
        tracker.add_expense(amount, category)
        st.success(f"Added ${amount} for {category}")
    else:
        st.error("Please enter valid amount and category.")

st.header("📊 Expense Summary")
if tracker.expenses:
    for expense in tracker.expenses:
        st.write(f"{expense['date']} - ${expense['amount']} - {expense['category']}")

st.header("📈 Expense Chart")
tracker.plot_expenses()