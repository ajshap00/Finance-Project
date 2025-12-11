import pandas as pd
import gspread
from datetime import date, datetime

gc = gspread.service_account(filename='finance-tracker-project-480905-9a0bc6c23b2a.json')
sh = gc.open("Finance Project Sheet").sheet1
today = date.today().strftime("%Y-%m-%d")

#for csv reading
df2 = pd.read_csv("Discover-2025-YearToDateSummary.csv")
sh.clear()


headers = ["Balance", "Transactions", "Date", "Deposits", "Withdraws"]
sh.update(range_name="A1:F1", values=[headers])

# Get last balance
col_a = sh.col_values(1)
balance = float(col_a[-1]) if len(col_a) > 1 else 0

# List to batch rows
rows_to_add = []

def new_transaction(name, amount, transaction_date=today):
    global balance
    balance += amount
    new_balance = balance
    transaction = name

    new_deposit = f"{abs(amount)}" if amount < 0 else ""
    new_withdraw = f"{abs(amount)}" if amount > 0 else ""

    row_data = [
        new_balance,
        transaction,
        transaction_date,
        new_deposit,
        new_withdraw,
    ]
    
    rows_to_add.append(row_data)

# Loop through CSV

for index, row in df2.iterrows():
    transaction_date = datetime.strptime(row["Post Date"], "%m/%d/%Y").strftime("%Y-%m-%d")
    description = row["Description"]
    amount = float(row["Amount"])

    new_transaction(description, amount, transaction_date)


new_input = input("Would you like to add any new transactions? y/n: ")

while new_input == 'y':
    try:
        description, amount, day = input("Enter Description, Amount, Date (YYYY-MM-DD) separated by commas: ").split(",")
        amount = float(amount)
        new_transaction (description, amount, day)

    except ValueError:
        print("Invalid input format. Please enter exactly: Description,Amount,Date")

    new_input = input("Would you like to add another transaction? y/n: ")

# Append all new transactions in one batch
if rows_to_add:
    sh.append_rows(rows_to_add)

# Reload sheet into DataFrame
data = sh.get_all_values()
df = pd.DataFrame(data)

