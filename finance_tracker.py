from tkinter import *
from tkinter import ttk
import os
from dotenv import load_dotenv
import gspread
import pandas as pd
import tkcalendar
import datetime

load_dotenv()
CREDENTIALS = os.getenv("GOOGLE_CREDS")

gc = gspread.service_account(filename=CREDENTIALS)
worksheet = gc.open("Finance Project Sheet").sheet1

def Run():
    test_df = pd.read_csv("finance_sheet.csv")
    worksheet.clear()
    headers = ["Balance", "Transactions", "Date", "Withdraws", "Deposits"]
    worksheet.update(range_name="A1:F1", values=[headers])

    col_a = worksheet.col_values(1)
    balance = float(col_a[-1] if len(col_a) > 1 else 0)

    rows_to_add=[]

    def add_data(description, amount, date):
        nonlocal balance
        balance += float(amount)
        deposit = amount if amount < 0 else ""
        withdraw = amount if amount > 0 else ""

        data = [
            float(balance),
            description.upper(),
            date,
            deposit,
            withdraw
        ]
        rows_to_add.append(data)

    for i, row in test_df.iterrows():
        description = row["Description"]
        amount = row["Amount"]
        date = row["Date"]

        add_data(description,amount,date)

    if rows_to_add:
        worksheet.append_rows(rows_to_add)

class Transactions:
    def __init__(self, desc, am, date):
        self.desc = desc
        self.am = am
        self.date = date

    def new_transaction(self):
        new_row = {
            "Description": self.desc,
            "Amount": self.am,
            "Date": self.date
            }
        
        new_data = pd.DataFrame([new_row])
        new_data.to_csv('finance_sheet.csv', index=False, mode='a', header=False)

class Interface:
    def __init__(self, root):   

        #Functions
        def retry():
            clear_description()
            clear_amount()
            clear_day()
            self.label_desc.config(text="")
            self.label_am.config(text="ENTER VALID INPUTS")
            self.label_date.config(text="")

        def button_pressed(event = None):
            try:
                if len(get_description()) > 0:
                    input_description = get_description()
                else:
                    retry()
                input_amount = float(get_amount())            
                input_date = get_day()           

                trans = Transactions(input_description, input_amount, input_date)
                trans.new_transaction()

                clear_description()
                clear_amount()
                clear_day()

                Run()
                
                self.label_desc.config(text=input_description)
                self.label_am.config(text=input_amount)
                self.label_date.config(text=input_date)
                return
            except ValueError:
                retry()

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
        def get_day():
            return date_entry.get_date()
        def clear_day():
            date_entry.set_date(datetime.date.today())
            return

        #mainframe
        root.title("Finance Manager")
        root.geometry("450x300")
        root.resizable(False, False)
        mainframe = ttk.Frame(root, width=450, height=200, padding=(3,3,12,12))
        mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        #Labels
        self.label_newtrans = ttk.Label(mainframe,text="ENTER NEW TRANSACTION")
        self.label_newtrans.grid(column=1,row=1, columnspan=3, sticky=(S))
        self.label_desc_text = ttk.Label(mainframe,text="Description:")
        self.label_desc_text.grid(column=1,row=2,sticky=(S))
        self.label_am_text = ttk.Label(mainframe,text="Amount:")
        self.label_am_text.grid(column=2,row=2,sticky=(S))
        self.label_date_text = ttk.Label(mainframe,text="Date:")
        self.label_date_text.grid(column=3,row=2,sticky=(S))

        self.label_desc = ttk.Label(mainframe, text="")
        self.label_desc.grid(column=1,row=5,sticky=(S))
        self.label_am = ttk.Label(mainframe, text="")
        self.label_am.grid(column=2,row=5,sticky=(S))
        self.label_date = ttk.Label(mainframe, text="")
        self.label_date.grid(column=3,row=5,sticky=(S))

        #Buttons
        description=StringVar()
        description_entry = ttk.Entry(mainframe, width=7, textvariable=description)
        description_entry.grid(column=1,row=3,sticky=(W,E))

        amount=StringVar()
        amount_entry = ttk.Entry(mainframe, width=7, textvariable=amount)
        amount_entry.grid(column=2,row=3,sticky=(W,E))

        date_entry = tkcalendar.DateEntry(master=mainframe, width = 7)
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
        root.bind("<Return>", button_pressed)

root = Tk()
Interface(root)
root.mainloop()
