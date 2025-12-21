# 💰 Finance Manager

A Python-based personal finance management application for tracking transactions, calculating balances, and visualizing earnings versus spending over time.

This project was built as a learning-focused tool to better understand data handling, financial analysis, and desktop application development in Python.

---

## 🚀 Features

- Manual transaction entry through a Tkinter desktop UI
- Running balance calculation from transaction history
- Monthly and yearly cash flow analysis
- Side-by-side bar charts for earnings vs. spending
- Clean, readable financial visualizations
- CSV-based data storage for simplicity and transparency

---

## 🛠️ Tech Stack

- **Python**
- **Pandas** – data processing and aggregation
- **Matplotlib** – financial data visualization
- **Tkinter** – desktop user interface
- **CSV** – transaction storage

---

## 📊 Visualizations

- Monthly earnings vs. spending bar charts
- Running account balance over time
- Adjustable axis scaling and labeling for clarity

---

## 📁 Project Structure
      Finance-Manager/
         │
         ├── finance_sheet.csv # Transaction data
         ├── main.py # Application entry point
         ├── charts.py # Data analysis & plotting
         ├── ui.py # Tkinter interface
         ├── icon.jpg # App icon
         └── README.md

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/ajshap00/finance-manager.git
2. Install dependencies:
    ```bash
    pip install pandas matplotlib gspread os dotenv tkinter plaid

3. Run the application:
    ```bash
    python main.py
