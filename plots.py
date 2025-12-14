import pandas as pd
import matplotlib.pyplot as mp
import datetime

df = pd.DataFrame(data=(pd.read_csv("finance_sheet.csv")), columns=['Amount', 'Date'])

for i, row in df:
    spending = 0
    earning = 0

    if row["Amount"] > 0:
        earning += row["Amount"]
    elif row["Amount"] < 0:
        spending += row["Amount"]

barplot = df.plot.bar(x='Date',y='Amount')
mp.show(barplot)

print (df)
