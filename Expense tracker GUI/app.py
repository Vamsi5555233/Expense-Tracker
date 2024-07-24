import mysql.connector
from decimal import Decimal
from collections import defaultdict
from datetime import datetime
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image


# Function to connect to MySQL database and create schema if not exists
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library"
        )
        if conn.is_connected():
            print("Connected to MySQL database successfully!!")
            create_table(conn)  # Create table if not exists
            return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Function to create 'transactions' table if it does not exist
def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                category_type VARCHAR(50) NOT NULL,
                category_name VARCHAR(100) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL
            )
        """)
        conn.commit()
        print("Table 'transactions' created successfully!")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


# Function to fetch data from database and process it
def fetch_and_process_data():
    conn = connect_to_database()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Fetch all entries from transactions table
        cursor.execute("SELECT * FROM transactions")
        entries = cursor.fetchall()

        # Initialize variables
        income = defaultdict(Decimal)
        expenses = defaultdict(list)

        # Process entries
        for entry in entries:
            date, category_type, category_name, amount = entry[1], entry[2], entry[3], entry[4]
            if category_type == 'Income':
                income[date.strftime('%Y-%m')] += amount
            elif category_type == 'Expense':
                expenses[date.strftime('%Y-%m')].append((category_name, amount))

        # Calculate available balance
        available_balance = sum(income.values()) - sum(sum(exp[1] for exp in expenses[month]) for month in expenses)

        # Prepare formatted report text
        report_text = []
        report_text.append("Financial Report")
        report_text.append(f"Available Balance: {available_balance:.2f}\n")

        # Append total incomes per month with details to report text
        report_text.append("Incomes:")
        for month, income_amount in income.items():
            report_text.append(f"Monthly Income in {month}: {income_amount:.2f}")

        # Append total expenses per month with details to report text
        report_text.append("\nExpenses:")
        for month, exp_items in expenses.items():
            total_expense = sum(item[1] for item in exp_items)
            report_text.append(f"Total Expenses in {month}: {total_expense:.2f}")
            report_text.append("Details:")
            for item in exp_items:
                report_text.append(f"- {item[0]}: {item[1]:.2f}")
            report_text.append("")  # Empty line for separation

        # Calculate overall incomes in a year
        overall_income = sum(income.values())
        report_text.append(f"\nOverall Income in the Year: {overall_income:.2f}")

        # Calculate overall expenses in a year
        overall_expenses = sum(sum(item[1] for item in exp_items) for exp_items in expenses.values())
        report_text.append(f"Overall Expenses in the Year: {overall_expenses:.2f}")

        return report_text, income, expenses

    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL: {e}")
        return None, None, None

    finally:
        cursor.close()
        conn.close()


# Function to add a new transaction to the database
def add_transaction(category_type, category_name, amount, date):
    conn = connect_to_database()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        # Insert new transaction into transactions table
        cursor.execute("INSERT INTO transactions (date, category_type, category_name, amount) VALUES (%s, %s, %s, %s)",
                       (date, category_type, category_name, amount))
        conn.commit()
        print("Transaction added successfully!")
        return True

    except mysql.connector.Error as e:
        print(f"Error adding transaction to MySQL: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


# Function to display GUI for viewing report and adding transactions
def display_gui_report():
    # Initial report fetch
    report_text, income, expenses = fetch_and_process_data()
    if not report_text:
        return

    # Create a placeholder for the chart image
    chart_image = sg.Image(key="-CHART-")

    # Layout for PySimpleGUI window
    layout = [
        [sg.Text("Financial Report", font=("Helvetica", 20))],
        [sg.Column([[sg.Multiline(size=(70, 20), key="-REPORT-", disabled=True)]], vertical_alignment='top'),
         sg.Column([[chart_image]], vertical_alignment='top')],
        [sg.Button("Add Income", key="-ADD_INCOME-"), sg.Button("Add Expense", key="-ADD_EXPENSE-")],
        [sg.Button("Refresh Report", key="-REFRESH-"), sg.Button("Exit", key="-EXIT-")]
    ]

    # Create the PySimpleGUI window
    window = sg.Window("Financial Report", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "-EXIT-":
            break

        elif event == "-REFRESH-":
            report_text, income, expenses = fetch_and_process_data()
            if report_text:
                window["-REPORT-"].update("\n".join(report_text))

                # Plotting expenses bar chart
                if expenses:
                    months = sorted(expenses.keys())
                    expense_totals = [sum(item[1] for item in expenses[month]) for month in months]

                    plt.figure(figsize=(8, 6))
                    plt.bar(months, expense_totals, color='blue')
                    plt.xlabel('Months')
                    plt.ylabel('Total Expenses')
                    plt.title('Monthly Expenses')
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Save chart to a BytesIO object
                    chart_bytes = io.BytesIO()
                    plt.savefig(chart_bytes, format='png')
                    plt.close()
                    chart_bytes.seek(0)

                    # Update the chart image element
                    window["-CHART-"].update(data=chart_bytes.getvalue())

        elif event == "-ADD_INCOME-" or event == "-ADD_EXPENSE-":
            add_type = "Income" if event == "-ADD_INCOME-" else "Expense"
            add_layout = [
                [sg.Text(f"Add {add_type}", font=("Helvetica", 15))],
                [sg.Text("Category Name"), sg.Input(key="-CATEGORY-NAME-")],
                [sg.Text("Amount"), sg.Input(key="-AMOUNT-")],
                [sg.Text("Date (YYYY-MM-DD)"), sg.Input(key="-DATE-")],
                [sg.Button("Submit"), sg.Button("Cancel")]
            ]
            add_window = sg.Window(f"Add {add_type}", add_layout)

            while True:
                add_event, add_values = add_window.read()

                if add_event == sg.WINDOW_CLOSED or add_event == "Cancel":
                    break

                elif add_event == "Submit":
                    category_name = add_values["-CATEGORY-NAME-"]
                    amount = Decimal(add_values["-AMOUNT-"])
                    date = add_values["-DATE-"]

                    if category_name and amount > 0 and date:
                        try:
                            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                            if add_transaction(add_type, category_name, amount, date_obj):
                                sg.popup(f"{add_type} added successfully!")
                                add_window.close()
                                break
                            else:
                                sg.popup_error("Failed to add transaction. Please try again.")
                        except ValueError:
                            sg.popup_error("Please enter a valid date in YYYY-MM-DD format.")
                    else:
                        sg.popup_error("Please enter valid category name, amount, and date.")

            add_window.close()

    window.close()


# Main function to run the GUI application
def main():
    display_gui_report()


if __name__ == "__main__":
    main()
