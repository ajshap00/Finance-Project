from tkinter import *
from tkinter import ttk
import os
from dotenv import load_dotenv
import gspread
import pandas as pd

load_dotenv()

CREDENTIALS = os.getenv("GOOGLE_CREDS")

gc = gspread.service_account(filename=CREDENTIALS)
test_df = pd.read_csv("test.csv")

worksheet = gc.open("Finance Project Sheet").sheet1
worksheet.clear()

headers = ["Balance", "Transactions", "Date", "Withdraws", "Deposits"]
worksheet.update(range_name="A1:F1", values=[headers])

col_a = worksheet.col_values(1)

def add_data():
    for i in test_df:
        try:
            worksheet.append_row(values={
                "Balance": i[1],
                "Transactions": i[0],
                "Date": i[2],
                "Withdraw": i[0] if i[0] > 0 else "",
                "Deposit": i[0] if i[0] < 0 else ""}
            )
        except ValueError:
            return "Try again"

class Transactions:
    def __init__(self, desc, am, date):
        self.desc = desc
        self.am = am
        self.date = date

    def new_transaction(self):
        try:
            new_row = {
                "Description": self.desc,
                "Amount": self.am,
                "Date": self.date
                }
            
            new_data = pd.DataFrame([new_row])
            new_data.to_csv('test.csv', index=False, mode='a', header=False)

        except ValueError:
            return "Bad inputs, try again..."

class Interface:
    def __init__(self, root):   

        #Functions
        def button_pressed():
            input_description = get_description()
            input_amount = get_amount()
            input_date = get_date()

            trans = Transactions(input_description, input_amount, input_date)
            trans.new_transaction()

            clear_description()
            clear_amount()
            clear_date()

            ttk.Label(mainframe, text=input_description).grid(column=1,row=5,sticky=(S))
            ttk.Label(mainframe, text=input_amount).grid(column=2,row=5,sticky=(S))
            ttk.Label(mainframe, text=input_date).grid(column=3,row=5,sticky=(S))
            return

        def get_description():
            return description_entry.get()
        def clear_description():
            description_entry.delete(0, 'end')
            return
        def get_amount():
            return amount_entry.get()
        def clear_amount():
            amount_entry.delete(0, 'end')
            return
        def get_date():
            return date_entry.get()
        def clear_date():
            date_entry.delete(0, 'end')
            return

        #mainframe
        root.title("Finance Manager")
        root.geometry("450x200")
        root.resizable(False, False)
        mainframe = ttk.Frame(root, width=450, height=200, padding=(3,3,12,12))
        mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        #Labels
        ttk.Label(mainframe,text="ENTER NEW TRANSACTION").grid(column=1,row=1, columnspan=3, sticky=(N))
        ttk.Label(mainframe,text="Description:").grid(column=1,row=2,sticky=(S))
        ttk.Label(mainframe,text="Amount:").grid(column=2,row=2,sticky=(S))
        ttk.Label(mainframe,text="Date:").grid(column=3,row=2,sticky=(S))

        #Buttons
        description=StringVar()
        description_entry = ttk.Entry(mainframe, width=7, textvariable=description)
        description_entry.grid(column=1,row=3,sticky=(W,E))

        amount=StringVar()
        amount_entry = ttk.Entry(mainframe, width=7, textvariable=amount)
        amount_entry.grid(column=2,row=3,sticky=(W,E))

        date=StringVar()
        date_entry = ttk.Entry(mainframe, width=7, textvariable=date)
        date_entry.grid(column=3,row=3,sticky=(W,E))

        done = ttk.Button(mainframe, width=7, text="Done", command=button_pressed)
        done.grid(column=2, row=4,rowspan=2, sticky=(N,W,E))

        #Config for making it pretty
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1,weight=1)
        mainframe.columnconfigure(2,weight=1)
        mainframe.columnconfigure(3,weight=1)
        mainframe.rowconfigure(4,weight=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)
        description_entry.focus()
        root.bind("<Return>", done)

root = Tk()
Interface(root)
root.mainloop()
add_data()