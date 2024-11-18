import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import sqlite3

# Create and connect to SQLite database
conn = sqlite3.connect("finance_manager.db")
cursor = conn.cursor()

# Create table for storing finance records
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,  -- 'income' or 'expense'
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
''')
conn.commit()


# Function to add an entry (income or expense)
def add_entry():
    entry_type = entry_type_var.get()
    amount = entry_amount_var.get()
    description = entry_description_var.get()
    date = entry_date_var.get()

    if not amount or amount <= 0:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        return

    if entry_type == "Select":
        messagebox.showerror("Invalid Input", "Please select income or expense.")
        return

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")  # Default to today's date

    # Insert the transaction into the database
    cursor.execute("INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)",
                   (entry_type, amount, description, date))
    conn.commit()

    messagebox.showinfo("Success", f"{entry_type.capitalize()} of {amount} added successfully!")
    clear_entries()
    update_balance()
    refresh_transactions()


# Function to clear the input fields
def clear_entries():
    entry_type_var.set("Select")  # Reset the transaction type
    entry_amount_var.set(0.0)     # Reset the amount to a float (0.0)
    entry_description_var.set("")  # Reset the description to an empty string
    entry_date_var.set(datetime.today().strftime("%Y-%m-%d"))  # Reset the date to today's date


# Function to update the balance
def update_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expenses = cursor.fetchone()[0] or 0
    balance = total_income - total_expenses
    balance_label.config(text=f"Balance: ${balance:.2f}")


# Function to refresh the Treeview by reloading transactions
def refresh_transactions():
    # Clear the current rows in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Fetch updated transactions from the database
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    # Insert the new rows into the Treeview
    for row in rows:
        # Assuming row[0] is the ID and row contains all transaction details
        tree.insert("", "end", iid=row[0], values=row)  # Insert the row with the correct ID
    print("Treeview has been refreshed.")


# Function to load selected transaction into entry fields for editing
def load_selected_transaction(_):  # Accept event parameter with a default value
    selected_item = tree.selection()  # Get the selected item(s)

    if not selected_item:  # Check if no item is selected
        messagebox.showerror("Error", "No transaction selected.")
        return

    # We expect only one selection, so take the first element of the tuple
    selected_item_id = selected_item[0]

    # Debug: Check the selected item ID
    print(f"Selected Item ID: {selected_item_id}")

    # Fetch the values from the selected row using the item ID
    selected_data = tree.item(selected_item_id, "values")

    # Debug: Print out the values returned by the selected row
    print(f"Selected Data: {selected_data}")

    if selected_data:
        entry_id_var.set(selected_data[0])  # Set the ID in the entry field
        entry_type_var.set(selected_data[1])  # Set the type (income/expense)
        entry_amount_var.set(selected_data[2])  # Set the amount (float)
        entry_description_var.set(selected_data[3])  # Set the description
        entry_date_var.set(selected_data[4])  # Set the date


# Function to edit the selected transaction
def edit_entry():
    entry_id = entry_id_var.get()
    entry_type = entry_type_var.get()
    amount = entry_amount_var.get()
    description = entry_description_var.get()
    date = entry_date_var.get()

    if not entry_id:
        messagebox.showerror("Error", "No transaction selected for editing.")
        return

    if not amount or amount <= 0:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        return

    if entry_type == "Select":
        messagebox.showerror("Invalid Input", "Please select income or expense.")
        return

    cursor.execute("UPDATE transactions SET type = ?, amount = ?, description = ?, date = ? WHERE id = ?",
                   (entry_type, amount, description, date, entry_id))
    conn.commit()

    messagebox.showinfo("Success", f"Transaction updated successfully!")
    clear_entries()
    update_balance()
    refresh_transactions()


# Function to delete the selected transaction
def delete_entry():
    selected_item = tree.selection()  # Get the selected item(s)

    if not selected_item:  # Check if no item is selected
        messagebox.showerror("Error", "No transaction selected for deletion.")
        return

    # We expect only one selection, so take the first element of the tuple
    selected_item_id = selected_item[0]

    # Debug: Check the selected item ID
    print(f"Selected Item ID for Deletion: {selected_item_id}")

    # Confirm deletion with the user
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this transaction?")
    if not confirm:
        return  # If the user clicks 'No', do not proceed

    # Check if the selected item exists in the database
    selected_item_id = int(selected_item_id)  # Ensure it's an integer if needed
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (selected_item_id,))
    transaction = cursor.fetchone()

    if not transaction:
        messagebox.showerror("Error", "Transaction not found in the database.")
        print(f"Transaction with ID {selected_item_id} was not found in the database.")
        return

    # Delete the transaction from the database
    cursor.execute("DELETE FROM transactions WHERE id = ?", (selected_item_id,))
    conn.commit()
    print(f"Transaction with ID {selected_item_id} deleted from the database.")

    # Delete the item from the Treeview
    tree.delete(selected_item_id)
    print(f"Transaction with ID {selected_item_id} deleted from the Treeview.")

    # Show success message
    messagebox.showinfo("Success", "Transaction deleted successfully!")

    # Update the balance and refresh the Treeview
    update_balance()
    refresh_transactions()


# Setting up the main application window
root = tk.Tk()
root.title("Finance Manager")

# Variables for Entry fields
entry_id_var = tk.StringVar()
entry_type_var = tk.StringVar(value="Select")
entry_amount_var = tk.DoubleVar()
entry_description_var = tk.StringVar()
entry_date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))

# Layout for the form to add/edit a transaction
entry_type_label = tk.Label(root, text="Transaction Type:")
entry_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_type_menu = tk.OptionMenu(root, entry_type_var, "Select", "income", "expense")
entry_type_menu.grid(row=0, column=1, padx=10, pady=10)

entry_amount_label = tk.Label(root, text="Amount:")
entry_amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_amount_entry = tk.Entry(root, textvariable=entry_amount_var)
entry_amount_entry.grid(row=1, column=1, padx=10, pady=10)

entry_description_label = tk.Label(root, text="Description:")
entry_description_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_description_entry = tk.Entry(root, textvariable=entry_description_var)
entry_description_entry.grid(row=2, column=1, padx=10, pady=10)

entry_date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
entry_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_date_entry = tk.Entry(root, textvariable=entry_date_var)
entry_date_entry.grid(row=3, column=1, padx=10, pady=10)

# Buttons for adding/editing transactions
add_button = tk.Button(root, text="Add Transaction", command=add_entry)
add_button.grid(row=4, column=0, padx=10, pady=20)

edit_button = tk.Button(root, text="Edit Transaction", command=edit_entry)
edit_button.grid(row=4, column=1, padx=10, pady=20)

# Button to delete transaction
delete_button = tk.Button(root, text="Delete Transaction", command=delete_entry)
delete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Label to display current balance
balance_label = tk.Label(root, text="Balance: $0.00")
balance_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Create the treeview to display transactions
columns = ("ID", "Type", "Amount", "Description", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

# Bind a function to select a row for editing
tree.bind("<ButtonRelease-1>", load_selected_transaction)

# Update the balance and transactions on startup
update_balance()
refresh_transactions()

# Start the Tkinter event loop
root.mainloop()

# Close the database connection when the app is closed
conn.close()
