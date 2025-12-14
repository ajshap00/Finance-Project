import pandas as pd
import matplotlib.pyplot as mp
from matplotlib.ticker import MultipleLocator
import datetime

def show_plot():
    df = pd.read_csv("finance_sheet.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df["Balance"] = df["Amount"].cumsum()

    summary = df.assign(
        Earnings=df["Amount"].where(df["Amount"] > 0, 0),
        Spending=df["Amount"].where(df["Amount"] < 0, 0)
    )

    monthly_summary = summary.groupby(
        summary["Date"].dt.to_period("M")
    )[["Earnings", "Spending"]].sum().abs()

    monthly_summary.index = monthly_summary.index.strftime("%b %y")
    
    ax = monthly_summary.plot(
        kind="bar",
        figsize=(10,4),
        width=0.8
    )
    ax.bar_label(ax.containers[0])
    ax.bar_label(ax.containers[1])
    ax.set_ylim(0, monthly_summary.max().max() * 1.1)
    ax.margins(y=0.05)
    mp.xticks(rotation=0)

    mp.title("Monthly Earnings vs Spending")
    mp.xlabel("Month")
    mp.ylabel("Amount")
    mp.tight_layout()
    mp.show()
    return