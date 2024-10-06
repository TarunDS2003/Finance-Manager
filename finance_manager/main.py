import tkinter as tk
from tkinter import messagebox, ttk
import json

# Global variables
transactions = []
budgets = {}

# Function to load transactions from JSON file
def load_transactions():
    global transactions
    try:
        with open('transactions.json', 'r') as f:
            transactions = json.load(f)
    except FileNotFoundError:
        transactions = []

# Function to save transactions to JSON file
def save_transactions():
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)

# Function to load budgets from JSON file
def load_budgets():
    global budgets
    try:
        with open('budgets.json', 'r') as f:
            budgets = json.load(f)
    except FileNotFoundError:
        budgets = {}

# Function to save budgets to JSON file
def save_budgets():
    with open('budgets.json', 'w') as f:
        json.dump(budgets, f, indent=4)

# Function to add a new transaction
def add_transaction():
    date = entry_date.get()
    description = entry_description.get()
    amount = float(entry_amount.get())
    category = entry_category.get()

    if date.strip() == "" or description.strip() == "" or amount == 0 or category.strip() == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    # Check if the category has a budget
    if category in budgets:
        # Calculate total expenses for the category including the new transaction
        total_expenses = sum(transaction['amount'] for transaction in transactions if transaction['category'] == category) + amount
        
        # Check if adding this transaction exceeds the budget
        if total_expenses > budgets[category]:
            messagebox.showwarning("Budget Exceeded", f"Adding this transaction will exceed the budget for {category} category.")
            return

    transaction = {
        "date": date,
        "description": description,
        "amount": amount,
        "category": category
    }
    transactions.append(transaction)
    save_transactions()
    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_transaction_entries()
    update_transactions_list()

# Function to update transactions listbox
def update_transactions_list():
    transactions_listbox.delete(0, tk.END)
    for idx, transaction in enumerate(transactions, start=1):
        transactions_listbox.insert(tk.END, f"{idx}. Date: {transaction['date']}, Description: {transaction['description']}, Amount: {transaction['amount']}, Category: {transaction['category']}")
        
    # Bind double click on listbox to manage_transaction function
    transactions_listbox.bind("<Double-Button-1>", manage_transaction)

# Function to manage selected transaction (update or delete)
def manage_transaction(event):
    global transactions

    # Get index of selected item in listbox
    selected_idx = transactions_listbox.curselection()
    if not selected_idx:
        return

    idx = selected_idx[0]
    transaction = transactions[idx]

    # Display details of selected transaction in entry fields
    entry_date.delete(0, tk.END)
    entry_date.insert(0, transaction['date'])
    entry_description.delete(0, tk.END)
    entry_description.insert(0, transaction['description'])
    entry_amount.delete(0, tk.END)
    entry_amount.insert(0, transaction['amount'])
    entry_category.delete(0, tk.END)
    entry_category.insert(0, transaction['category'])

    # Configure the button for managing transactions
    button_add.config(text="Save Changes", command=lambda: save_updated_transaction(idx))
    button_delete.config(text="Delete", command=lambda: delete_transaction(idx))

# Function to save updated transaction
def save_updated_transaction(index):
    global transactions

    # Get updated details from entry fields
    date = entry_date.get()
    description = entry_description.get()
    amount = float(entry_amount.get())
    category = entry_category.get()

    if date.strip() == "" or description.strip() == "" or amount == 0 or category.strip() == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Update transaction in the list
    transactions[index] = {
        "date": date,
        "description": description,
        "amount": amount,
        "category": category
    }

    # Save transactions to file and update listbox
    save_transactions()
    update_transactions_list()

    # Reset entry fields and button text after saving
    clear_transaction_entries()
    button_add.config(text="Add Transaction", command=add_transaction)
    button_delete.config(text="")

# Function to delete a transaction
def delete_transaction(index):
    global transactions

    # Confirm deletion with user
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
        # Delete transaction from list
        del transactions[index]

        # Save transactions to file and update listbox
        save_transactions()
        update_transactions_list()

# Function to calculate summary (total income, total expenses, balance)
def calculate_summary():
    total_income = sum(transaction['amount'] for transaction in transactions if transaction['amount'] > 0)
    total_expenses = sum(transaction['amount'] for transaction in transactions if transaction['amount'] < 0)
    balance = total_income + total_expenses
    return total_income, total_expenses, balance

# Function to set budget for a category
def set_budget():
    category = entry_budget_category.get()
    budget_amount = float(entry_budget_amount.get())

    if category.strip() == "" or budget_amount <= 0:
        messagebox.showerror("Error", "Please enter a valid category and budget amount.")
        return
    
    budgets[category] = budget_amount
    save_budgets()
    messagebox.showinfo("Success", f"Budget set successfully for {category}")

# Function to display budgets
def display_budgets():
    budget_message = "Current Budgets:\n"
    for category, budget in budgets.items():
        budget_message += f"{category}: {budget}\n"
    messagebox.showinfo("Budgets", budget_message)

# Function to clear entry fields after adding or updating a transaction
def clear_transaction_entries():
    entry_date.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)

# Function to clear entry fields in the budget management section
def clear_budget_entries():
    entry_budget_category.delete(0, tk.END)
    entry_budget_amount.delete(0, tk.END)

# Initialize GUI
def main():
    global root, entry_date, entry_description, entry_amount, entry_category, transactions_listbox, button_add, button_delete, entry_budget_category, entry_budget_amount
    
    root = tk.Tk()
    root.title("Personal Finance Manager")

    # Configure colors and fonts
    root.configure(bg="#F0F0F0")  # Set background color
    root.option_add("*Font", "Arial 10")  # Set default font
    
    # Create GUI components with styling
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), foreground='black', background='#4CAF50', padx=10, pady=5)
    style.configure('TLabel', font=('Arial', 12), background='#F0F0F0')
    style.configure('TEntry', font=('Arial', 12), padx=5, pady=5)

    label_date = ttk.Label(root, text="Date (YYYY-MM-DD):")
    label_date.grid(row=0, column=0, padx=10, pady=10)
    entry_date = ttk.Entry(root, width=20)
    entry_date.grid(row=0, column=1, padx=10, pady=10)

    label_description = ttk.Label(root, text="Description:")
    label_description.grid(row=1, column=0, padx=10, pady=10)
    entry_description = ttk.Entry(root, width=40)
    entry_description.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    label_amount = ttk.Label(root, text="Amount:")
    label_amount.grid(row=2, column=0, padx=10, pady=10)
    entry_amount = ttk.Entry(root, width=20)
    entry_amount.grid(row=2, column=1, padx=10, pady=10)

    label_category = ttk.Label(root, text="Category:")
    label_category.grid(row=3, column=0, padx=10, pady=10)
    entry_category = ttk.Entry(root, width=40)
    entry_category.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    button_add = ttk.Button(root, text="Add Transaction", command=add_transaction)
    button_add.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    button_delete = ttk.Button(root, text="", command="")
    button_delete.grid(row=4, column=2, padx=10, pady=10)

    transactions_listbox = tk.Listbox(root, width=80, height=10, font=('Arial', 10))
    transactions_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    label_summary = ttk.Label(root, text="Summary:")
    label_summary.grid(row=6, column=0, padx=10, pady=10)

    button_summary = ttk.Button(root, text="Show Summary", command=show_summary)
    button_summary.grid(row=6, column=1, padx=10, pady=10)

    button_exit = ttk.Button(root, text="Exit", command=root.quit)
    button_exit.grid(row=6, column=2, padx=10, pady=10)

    # Budget Management Section
    label_budget = ttk.Label(root, text="Budget Management")
    label_budget.grid(row=7, column=0, padx=10, pady=10)

    label_budget_category = ttk.Label(root, text="Category:")
    label_budget_category.grid(row=8, column=0, padx=10, pady=10)
    entry_budget_category = ttk.Entry(root, width=40)
    entry_budget_category.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

    label_budget_amount = ttk.Label(root, text="Budget Amount:")
    label_budget_amount.grid(row=9, column=0, padx=10, pady=10)
    entry_budget_amount = ttk.Entry(root, width=20)
    entry_budget_amount.grid(row=9, column=1, padx=10, pady=10)

    button_set_budget = ttk.Button(root, text="Set Budget", command=set_budget)
    button_set_budget.grid(row=10, column=0, padx=10, pady=10)

    button_display_budgets = ttk.Button(root, text="Display Budgets", command=display_budgets)
    button_display_budgets.grid(row=10, column=1, padx=10, pady=10)

    button_clear_budget = ttk.Button(root, text="Clear Budget Entries", command=clear_budget_entries)
    button_clear_budget.grid(row=10, column=2, padx=10, pady=10)

    button_clear_transactions = ttk.Button(root, text="Clear Transaction Entries", command=clear_transaction_entries)
    button_clear_transactions.grid(row=11, column=0, padx=10, pady=10, columnspan=3)

    # Load transactions from file and update listbox
    load_transactions()
    update_transactions_list()

    # Load budgets from file
    load_budgets()

    root.mainloop()

# Function to display summary in a message box
def show_summary():
    income, expenses, balance = calculate_summary()
    summary_message = f"Total Income: {income}\nTotal Expenses: {expenses}\nBalance: {balance}"
    messagebox.showinfo("Summary", summary_message)

if __name__ == "__main__":
    main()
