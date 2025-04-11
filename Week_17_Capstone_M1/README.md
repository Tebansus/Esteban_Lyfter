# Money Management System

A financial tracking application built with Python, PySimpleGUI, and SQLite3.

## Features


- Add and manage categories.
- View transaction history with dates and balances in a table format.
- Reset functionality to clear all data.
- Prevent withdrawing more than account total.
- Automatic balance tracking.



## How to Use

1. **Starting the Application**
   - Run `main.py` to launch the application.
   - The database will be automatically created if it doesn't exist.

2. **Managing Categories**
   - Click "Add Category" to create new withdrawing/income categories.
   - Categories are required for all transactions.

3. **Adding Money**
   - Click "Add_Money" to add income
   - Select a category, you can't add it if no category exists.
   - Enter the amount and type of income.
   - The balance updates automatically inb the table.

4. **Withdrawing Money**
   - Click "Withdraw" to record expenses.
   - Select a category.
   - Enter the amount and type of withdrawal.
   - System prevents withdrawing more than the account has available.

5. **Resetting the Tool**
   - Click Reset Tool to clear all data.
   - Requires confirmation to prevent accidental resets.


