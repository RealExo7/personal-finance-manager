import tkinter as tk
import json
import matplotlib.pyplot as plt
from datetime import datetime

# File for saving transactions
transactions_file = "transactions.json"

# Predefined categories and currencies
categories_list = ["Housing", "Food", "Entertainment", "Transportation", "Utilities"]
currencies_list = ["EUR", "USD", "RON"]
current_year = datetime.now().year
months_list = [datetime(1, i, 1).strftime('%B') for i in range(1, 13)]

# Function to save transactions to a file
def save_transaction(amount, category, currency, date):
    transaction = {"amount": amount, "category": category, "currency": currency, "date": date}
    with open(transactions_file, 'a') as file:
        json.dump(transaction, file)
        file.write("\n")

# Function to add a new transaction
def add_transaction():
    transaction_window = tk.Toplevel(window)
    transaction_window.title("Add Transaction")

    label_amount = tk.Label(transaction_window, text="Amount:")
    label_amount.pack()
    entry_amount = tk.Entry(transaction_window)
    entry_amount.pack()

    label_category = tk.Label(transaction_window, text="Category:")
    label_category.pack()
    category_var = tk.StringVar(transaction_window)
    category_var.set(categories_list[0])  # Set default category
    category_menu = tk.OptionMenu(transaction_window, category_var, *categories_list)
    category_menu.pack()

    label_currency = tk.Label(transaction_window, text="Currency:")
    label_currency.pack()
    currency_var = tk.StringVar(transaction_window)
    currency_var.set(currencies_list[0])  # Set default currency
    currency_menu = tk.OptionMenu(transaction_window, currency_var, *currencies_list)
    currency_menu.pack()

    label_date = tk.Label(transaction_window, text="Date (YYYY-MM-DD):")
    label_date.pack()
    entry_date = tk.Entry(transaction_window)
    entry_date.pack()
    entry_date.insert(0, str(datetime.now().date()))  # Set default to today

    button_add = tk.Button(transaction_window, text="Add", command=lambda: save_transaction(entry_amount.get(), category_var.get(), currency_var.get(), entry_date.get()))
    button_add.pack()

# Function to generate a graph of expenses by category
def generate_graph():
    # Read transactions from the file
    categories = {}
    with open(transactions_file, 'r') as file:
        transactions = file.readlines()
        for transaction in transactions:
            data = json.loads(transaction)
            category = data["category"]
            amount = float(data["amount"])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

    # Create a bar graph of expenses by category
    labels = list(categories.keys())
    values = list(categories.values())

    plt.bar(labels, values)
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title('Expenses by Category')
    plt.show()

# Function to generate annual report based on selected year with months included
def generate_annual_report(year):
    annual_expenses = {}

    with open(transactions_file, 'r') as file:
        transactions = file.readlines()
        for transaction in transactions:
            data = json.loads(transaction)
            transaction_date = datetime.strptime(data["date"], "%Y-%m-%d")
            if transaction_date.year == year:
                category = data["category"]
                amount = float(data["amount"])
                month = transaction_date.month

                if category not in annual_expenses:
                    annual_expenses[category] = {}

                if month not in annual_expenses[category]:
                    annual_expenses[category][month] = 0

                annual_expenses[category][month] += amount

    # Save the annual report to a text file
    report_filename = f"annual_report_{year}.txt"
    with open(report_filename, 'w') as report_file:
        report_file.write(f"Annual Report for {year}:\n")
        for category, months in annual_expenses.items():
            report_file.write(f"{category}:\n")
            for month, total in months.items():
                report_file.write(f"  {months_list[month - 1]}: {total} {data['currency']}\n")
    
    print(f"Annual report saved to {report_filename}")

# Function to generate monthly report based on selected month and year
def generate_report(month, year):
    monthly_expenses = {}

    with open(transactions_file, 'r') as file:
        transactions = file.readlines()
        for transaction in transactions:
            data = json.loads(transaction)
            transaction_date = datetime.strptime(data["date"], "%Y-%m-%d")
            if transaction_date.month == month and transaction_date.year == year:
                category = data["category"]
                amount = float(data["amount"])
                if category in monthly_expenses:
                    monthly_expenses[category] += amount
                else:
                    monthly_expenses[category] = amount

    # Save the report to a text file
    report_filename = f"monthly_report_{datetime(year, month, 1).strftime('%B_%Y')}.txt"
    with open(report_filename, 'w') as report_file:
        report_file.write(f"Monthly Report for {datetime(year, month, 1).strftime('%B %Y')}:\n")
        for category, amount in monthly_expenses.items():
            report_file.write(f"{category}: {amount} {data['currency']}\n")
    
    print(f"Monthly report saved to {report_filename}")

# Main window function
def create_window():
    global window
    window = tk.Tk()
    window.title("Personal Finance Manager")
    window.geometry("400x300")

    label = tk.Label(window, text="Welcome to the Personal Finance Manager!")
    label.pack()

    add_button = tk.Button(window, text="Add Transaction", command=add_transaction)
    add_button.pack()

    graph_button = tk.Button(window, text="View Graph", command=generate_graph)
    graph_button.pack()

    # Month and year selection for report generation
    label_month = tk.Label(window, text="Select Month:")
    label_month.pack()

    month_var = tk.StringVar(window)
    month_var.set(months_list[datetime.now().month - 1])  # Default to current month
    month_menu = tk.OptionMenu(window, month_var, *months_list)
    month_menu.pack()

    label_year = tk.Label(window, text="Select Year:")
    label_year.pack()

    year_var = tk.StringVar(window)
    year_var.set(str(current_year))  # Default to current year
    year_menu = tk.OptionMenu(window, year_var, *[str(year) for year in range(current_year - 10, current_year + 1)])
    year_menu.pack()

    monthly_report_button = tk.Button(window, text="Generate Monthly Report", command=lambda: generate_report(months_list.index(month_var.get()) + 1, int(year_var.get())))
    monthly_report_button.pack()

    annual_report_button = tk.Button(window, text="Generate Annual Report", command=lambda: generate_annual_report(int(year_var.get())))
    annual_report_button.pack()

    window.mainloop()

# Start the application
if __name__ == "__main__":
    create_window()
