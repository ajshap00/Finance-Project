import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv
import gspread
import pandas as pd
import tkcalendar
import datetime
from plaid_connection import get_plaid_transactions, show_error

load_dotenv()
CREDENTIALS = os.getenv("GOOGLE_CREDS")

gc = gspread.service_account(filename=CREDENTIALS)
worksheet = gc.open("Finance Project Sheet").sheet1

sheet_headers = ["Balance", "Description", "Date", "Withdraws", "Deposits"]
csv_headers = ["Description", "Amount", "Date"]
rows_to_add = []

def Run():
    fs = pd.read_csv("finance_sheet.csv")
    fs['Date'] = pd.to_datetime(fs["Date"])
    fs = fs.sort_values(by=['Date'])

    balance = 0
    global rows_to_add
    rows_to_add = []

    for i, row in fs.iterrows():
        amount = float(row["Amount"])
        balance += float(amount)

        deposit = amount if amount > 0 else ""
        withdraw = -amount if amount < 0 else ""

        description = row["Description"].title()
        date = row["Date"].strftime("%Y-%m-%d") 

        rows_to_add.append([balance, description, date, withdraw, deposit])

    rows_to_add = rows_to_add[::-1]

    worksheet.clear()
    worksheet.update(range_name="A1:F1", values=[sheet_headers])

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

        if not os.path.exists('finance_sheet.csv') or os.path.getsize('finance_sheet.csv') == 0:
            new_data.to_csv('finance_sheet.csv', index=False, header=True)
        else:
            new_data.to_csv('finance_sheet.csv', index=False, mode='a', header=False)

class Interface:
    def __init__(self, root):   
        #Functions
        #Retry when bad inputs
        def retry():
            clear_description()
            clear_amount()
            clear_day()
            clear_import_start_entry()
            clear_import_end_entry()
            show_error()

        #When done is pressed
        def button_pressed(event = None):
            try:
                if len(get_description()) > 0:
                    input_description = get_description()
                else:
                    retry()
                    return
                input_amount = float(get_amount())            
                input_date = get_day()           

                trans = Transactions(input_description, input_amount, input_date)
                trans.new_transaction()

                clear_description()
                clear_amount()
                clear_day()
                clear_import_start_entry()
                clear_import_end_entry()

                self.label_desc.config(text=input_description)
                self.label_am.config(text=input_amount)
                self.label_date.config(text=input_date)

                Run()
                return
            except ValueError:
                retry()
                return
        
        #Clears data in csv, sheet, and local
        def clear_pressed():
            worksheet.clear()
            worksheet.update(range_name="A1:F1", values=[sheet_headers])
            
            empty_df = pd.DataFrame(columns=csv_headers)
            empty_df.to_csv("finance_sheet.csv", index=False)

            global rows_to_add
            rows_to_add = []

            clear_description()
            clear_amount()
            clear_day()
            clear_import_start_entry()
            clear_import_end_entry()
            return
        
        def import_plaid_transactions():
            trans = get_plaid_transactions(get_import_start_entry(), get_import_end_entry())

            for i in trans:
                t = Transactions(
                desc=i["name"],
                am=-i["amount"],
                date =i["date"]
                )
                t.new_transaction()

            Run()
            return

        #Getters and Clears
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
        def get_import_start_entry():
            return import_start_entry.get_date()
        def clear_import_start_entry():
            import_start_entry.set_date(datetime.date.today())
            return
        def get_import_end_entry():
            return import_end_entry.get_date()
        def clear_import_end_entry():
            import_end_entry.set_date(datetime.date.today())
            return

        #Mainframe
        root.title("Finance Manager")
        root.geometry("450x300")
        root.resizable(False, False)
        icon_path = os.path.join(os.getcwd(), 'icon.png')

        try:
            self.photo_icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, self.photo_icon)
        except tk.TclError as e:
            print("Error loading icon:", e)

        #Style
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure(
            "TFrame",
            background="#FFFFFF"
        )
        style.configure(
            "Title.TLabel",
            foreground="#2E2E2E",
            font=("Gilroy", 12, "bold")
        )
        style.configure(
            "TLabel",
            background="#ffffff",
            foreground="#636363",
            font=("Gilroy", 10, "bold")
        )
        style.configure(
            "TButton",
            relief="flat",
            borderwidth=0,
            foreground="#2E2E2E",
            background="#ddd0e2",
            padding=(10,6),
            font=("Gilroy", 11, "bold")
        )
        style.map(
            "TButton",
            foreground=[("active","#FFFFFF")],
            background=[("active","#947FF1")],
        )
        style.configure(
            "TEntry",
            relief="flat",
            borderwidth=0,
            fieldbackground="#ECEBEB",
            foreground="#525252",
            background="#525252",
            font=("Gilroy", 10, "bold")
        )

        #Frames
        mainframe = ttk.Frame(root, style="TFrame", padding=(3,3,12,12))
        mainframe.grid(column=0,row=0,sticky=(tk.N,tk.W,tk.E,tk.S))

        #Labels
        self.label_desc = ttk.Label(mainframe, text="")
        self.label_desc.grid(column=2,row=3,sticky=(tk.S))
        self.label_am = ttk.Label(mainframe, text="")
        self.label_am.grid(column=2,row=5,sticky=(tk.S))
        self.label_date = ttk.Label(mainframe, text="")
        self.label_date.grid(column=2,row=7,sticky=(tk.S))

        self.label_newtrans = ttk.Label(mainframe,text="Enter New Transaction", style="Title.TLabel")
        self.label_newtrans.grid(column=2,row=1, sticky=(tk.N))
        self.label_desc_text = ttk.Label(mainframe,text="Description:")
        self.label_desc_text.grid(column=1,row=2,sticky=(tk.N))
        self.label_am_text = ttk.Label(mainframe,text="Amount:")
        self.label_am_text.grid(column=1,row=4,sticky=(tk.N))
        self.label_date_text = ttk.Label(mainframe,text="Date:")
        self.label_date_text.grid(column=1,row=6,sticky=(tk.N))
        self.label_newtrans.grid(column=1,row=1, columnspan=3, sticky=(tk.N))
        self.label_last_desc_text = ttk.Label(mainframe,text="Last Transaction:")
        self.label_last_desc_text.grid(column=2,row=2,sticky=(tk.N))
        self.label_last_am_text = ttk.Label(mainframe,text="Last Amount:")
        self.label_last_am_text.grid(column=2,row=4,sticky=(tk.N))
        self.label_last_date_text = ttk.Label(mainframe,text="Last Date:")
        self.label_last_date_text.grid(column=2,row=6,sticky=(tk.N))
        self.label_import_text = ttk.Label(mainframe,text="Import From Bank:")
        self.label_import_text.grid(column=3,row=2,sticky=(tk.N))
        self.label_import_from_text = ttk.Label(mainframe,text="from:")
        self.label_import_from_text.grid(column=3,row=3,sticky=(tk.N))
        self.label_import_to_text = ttk.Label(mainframe,text="to:")
        self.label_import_to_text.grid(column=3,row=5,sticky=(tk.N))

        #Entries
        description=tk.StringVar()
        description_entry = tk.Entry(
            mainframe,
            background="#ECEBEB",
            foreground="#525252",
            insertbackground="#525252",
            font=("Gilroy", 10, "bold"),
            relief="flat",
            highlightthickness=0,
            bd=0,
            textvariable=description)
        description_entry.grid(column=1,row=3,sticky=(tk.N))
        amount=tk.StringVar()
        amount_entry = tk.Entry(
            mainframe,
            background="#ECEBEB",
            foreground="#525252",
            insertbackground="#525252",
            font=("Gilroy", 10, "bold"),
            relief="flat",
            highlightthickness=0,
            bd=0,
            textvariable=amount)
        
        amount_entry.grid(column=1,row=5,sticky=(tk.N))
        date_entry = tkcalendar.DateEntry(master=mainframe, style="TEntry")
        date_entry.grid(column=1,row=7,sticky=(tk.N))

        import_start_entry = tkcalendar.DateEntry(master=mainframe, style="TEntry")
        import_start_entry.grid(column=3,row=4,sticky=(tk.N))
        import_end_entry = tkcalendar.DateEntry(master=mainframe, style="TEntry")
        import_end_entry.grid(column=3,row=6,sticky=(tk.N))

        #Buttons
        done = ttk.Button(mainframe, text="Done", command=button_pressed)
        done.grid(column=1, row=8, sticky=(tk.N), pady=(20,0))
        clear_data = ttk.Button(mainframe, text="Clear Data", command=clear_pressed)
        clear_data.grid(column=2, row=8, sticky=(tk.N), pady=(20,0))
        imports = ttk.Button(mainframe, text="Import From Bank", command=import_plaid_transactions)
        imports.grid(column=3, row=8, sticky=(tk.N), pady=(20,0))
        #Config for making it pretty
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        for i in range(1, 4):
            mainframe.columnconfigure(i, weight=1, uniform="col")   
        for i in range(1, 4):   
            mainframe.rowconfigure(i, weight=1, uniform="row")
        for child in mainframe.winfo_children():
            child.grid_configure(padx=8,pady=8)
        description_entry.focus()
        root.bind("<Return>", button_pressed)

root = tk.Tk()
Interface(root)
root.mainloop()
