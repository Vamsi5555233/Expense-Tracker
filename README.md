 Financial Management System

This project is a Financial Management System that allows users to track their incomes and expenses, generate financial reports, and visualize monthly expenses through a graphical chart. The system uses a MySQL database to store transaction data and PySimpleGUI for the graphical user interface.

---

1. Features

1. Add Transactions: Users can add new income or expense transactions.
2. View Report: Generates a financial report showing available balance, total incomes and expenses per month, and overall incomes and expenses in the year.
3. Expense Visualization: Displays a bar chart of monthly expenses.

---

2. Requirements

To run this project, you will need the following:

1. Python: Ensure you have Python 3.6 or higher installed.
2. MySQL: MySQL server must be installed and running.
3. Python Libraries:
    - mysql-connector-python
    - PySimpleGUI
    - matplotlib
    - numpy
    - pillow

---

3. Installation

i. Clone the Repository:
    ```sh
    git clone https://github.com/your-repo/financial-management-system.git
    cd financial-management-system
    ```

ii. Set Up the Python Environment:
    - It's recommended to use a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
    ```

iii. Install the Required Libraries:
    ```sh
    pip install mysql-connector-python PySimpleGUI matplotlib numpy pillow
    ```

iv. Set Up MySQL Database:
    - Ensure your MySQL server is running.
    - Create a database named `library`:
    ```sql
    CREATE DATABASE library;
    ```

---

4. Usage

i. Run the Application:
    ```sh
    python main.py
    ```

ii. Using the Application:
    - Add Transactions: Click on "Add Income" or "Add Expense" buttons to add a new transaction.
    - View Report: The financial report is displayed along with a bar chart of monthly expenses.
    - Refresh Report: Click "Refresh Report" to update the report and chart with the latest data.

---

5. Code Structure

- **main.py**: The main file that contains the application code.
- **connect_to_database()**: Connects to the MySQL database and creates the `transactions` table if it doesn't exist.
- **create_table(conn)**: Creates the `transactions` table.
- **fetch_and_process_data()**: Fetches data from the database and processes it to generate the financial report.
- **add_transaction(category_type, category_name, amount, date)**: Adds a new transaction to the database.
- **display_gui_report()**: Displays the GUI for viewing the report and adding transactions.
- **main()**: The main function that runs the application.

---

6. Database Schema

- **transactions**:
    - `id`: INT, primary key, auto-increment
    - `date`: DATE, not null
    - `category_type`: VARCHAR(50), not null (e.g., "Income" or "Expense")
    - `category_name`: VARCHAR(100), not null
    - `amount`: DECIMAL(10, 2), not null

---

7. Notes

- Ensure the MySQL server is running before starting the application.
- The database connection details are hardcoded for simplicity. For a production system, consider using environment variables or a configuration file for database credentials.
- Handle invalid inputs gracefully in the GUI for better user experience.

---


8. Contribution

Contributions are welcome! Please fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

9. Contact

For any inquiries or issues, please contact satyavoluvamsikrishna@gmail.com

---

This README file provides an overview of the project, including installation instructions, usage guidelines, and a brief description of the code structure. Feel free to modify it as needed for your specific project details.
