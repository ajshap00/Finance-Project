import plaid
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.exceptions import ApiException
from dotenv import load_dotenv
from tkinter import messagebox
load_dotenv()
import os

ACCESS_TOKEN = os.getenv("PLAID_ACCESS_TOKEN")

config = Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_CLIENT_SECRET"),
    }
)

api_client = ApiClient(config)
plaid_client = plaid_api.PlaidApi(api_client)

def show_error():
        messagebox.showerror(title="Finance Tracker", message="Invalid Inputs", icon="warning")
        return

def get_plaid_transactions(start, end):
    try:
        request = TransactionsGetRequest(
            access_token = ACCESS_TOKEN,
            start_date = start,
            end_date = end
        )
        messagebox.showinfo(title="Finance Tracker", message="Success!", icon="info")
    except ApiException:
        show_error()
    response = plaid_client.transactions_get(request)
    return response["transactions"]