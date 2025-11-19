import csv
import os
from datetime import datetime

FILENAME = "transactions.csv"
if not os.path.exists(FILENAME):
    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Debit", "Credit", "Amount"])

def add_transaction(date, description, debit, credit, amount):
    """Add one transaction to the CSV file."""
    try:

        if not all([date, description, debit, credit, amount]):
            raise ValueError("All fields are required")

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

        try:
            float(amount)
        except ValueError:
            raise ValueError("Amount must be a valid number")
        
        with open(FILENAME, mode="a", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([date, description, debit, credit, amount])
        print("✅ Transaction saved to transactions.csv!")
        
    except Exception as e:
        print(f"❌ Error saving transaction: {str(e)}")
        raise

def get_all_transactions():
    """Return a list of all saved transactions as dictionaries."""
    try:
        if not os.path.exists(FILENAME):
            return []
            
        with open(FILENAME, mode="r", newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            transactions = []
            for row in reader:
                if all(key in row for key in ["Date", "Description", "Debit", "Credit", "Amount"]):
                    transactions.append(row)
                else:
                    print(f"Warning: Skipping malformed transaction row: {row}")
            return transactions
            
    except Exception as e:
        print(f"❌ Error reading transactions: {str(e)}")
        return []
