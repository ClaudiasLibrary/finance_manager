# Finance Manager

The **Finance Manager** application is a simple tool to track and manage your finances. This app allows you to record your income and expenses, edit entries, delete records, and view your balance in real-time. The data is stored in an SQLite database, which ensures that your financial records persist even after you close the application.

## Features

- **Add Transactions**: Record income or expenses with a description and date.
- **Edit Transactions**: Modify existing records.
- **Delete Transactions**: Remove unwanted entries.
- **Balance Display**: View your balance, calculated as the total income minus expenses.
- **Data Persistence**: Financial records are stored in an SQLite database (`finance_manager.db`).
- **Transaction History**: View a detailed table of all transactions, sortable by date, amount, or type.
- **Dynamic Updates**: The balance and transaction list update automatically after each operation.

## Requirements

- Python 3.x
- `tkinter` (for the graphical user interface)
- `sqlite3` (for database functionality)

These libraries are standard with Python, so you don't need to install anything extra.

## How to Use

### Adding a Transaction
1. Select the transaction type (either `income` or `expense`) from the dropdown.
2. Enter the amount in the "Amount" field.
3. Provide a description for the transaction (optional).
4. Enter a date (optional; defaults to today's date).
5. Click the "Add Transaction" button to save the entry.

### Editing a Transaction
1. Click on a transaction in the transaction list (Treeview).
2. Modify any of the fields (type, amount, description, date).
3. Click the "Edit Transaction" button to save your changes.

### Deleting a Transaction
1. Select a transaction from the list.
2. Click the "Delete Transaction" button.
3. Confirm the deletion in the popup.

### Viewing Balance
- The balance is calculated automatically by subtracting total expenses from total income.
- It is displayed at the top of the application window.

### Transaction List
- All transactions are displayed in a table (Treeview) with the following columns:
  - **ID**: A unique identifier for each transaction.
  - **Type**: Whether the transaction is `income` or `expense`.
  - **Amount**: The amount of the transaction.
  - **Description**: A brief description of the transaction (if provided).
  - **Date**: The date when the transaction occurred.

## Code Walkthrough

### SQLite Database

The app uses SQLite to store the financial data in a database. A table called `transactions` is created with the following fields:
- `id`: An auto-incrementing primary key.
- `type`: The transaction type (`income` or `expense`).
- `amount`: The amount of money involved in the transaction.
- `description`: A description of the transaction.
- `date`: The date when the transaction occurred.

SQL queries are used to insert, update, delete, and select transactions.

### Functions

- **add_entry()**: Adds a new transaction (income or expense) to the database. It validates the input and updates the balance and transaction list after adding the transaction.
- **clear_entries()**: Resets the input fields (transaction type, amount, description, date) to their default values.
- **update_balance()**: Calculates and updates the balance by fetching the total income and total expenses from the database.
- **refresh_transactions()**: Refreshes the Treeview widget to show the latest transactions from the database.
- **load_selected_transaction()**: Loads the selected transaction from the Treeview into the input fields for editing.
- **edit_entry()**: Edits an existing transaction based on the selected ID.
- **delete_entry()**: Deletes the selected transaction from the database after a confirmation prompt.

### UI Components

- **Entry Fields**: For entering transaction details (amount, description, date).
- **Buttons**: For adding, editing, and deleting transactions.
- **Treeview**: Displays all transactions in a table format, allowing users to select and edit them.
- **Balance Label**: Shows the current balance, which is updated automatically.

### Treeview (Transaction List)
- The Treeview is used to display the transactions in a tabular format with columns for **ID**, **Type**, **Amount**, **Description**, and **Date**.
- You can select a row in the Treeview to edit or delete the corresponding transaction.

## Installation

1. Clone the repository or download the script.
2. Ensure that Python 3.x is installed on your system.
3. Run the script:

```bash
python finance_manager.py
```

The app will automatically create a `finance_manager.db` database file if it does not already exist.

## License

This project is open-source and available under the MIT License.

## Acknowledgements

- `tkinter` for the graphical user interface.
- `sqlite3` for the database functionality.
