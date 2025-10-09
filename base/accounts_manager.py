import csv
import os
from collections import defaultdict

class AccountsManager:
    def __init__(self):
        self.account_types = {
            # ASSETS
            "Cash [ASSET]": "Assets",
            "Accounts Receivable [ASSET]": "Assets", 
            "Inventory [ASSET]": "Assets",
            "Prepaid Expenses [ASSET]": "Assets",
            "Equipment [ASSET]": "Assets",
            
            # LIABILITIES
            "Accounts Payable [LIABILITY]": "Liabilities",
            "Notes Payable [LIABILITY]": "Liabilities",
            
            # EQUITY
            "Owner's Capital [EQUITY]": "Equities",
            
            # INCOME
            "Sales Revenue [INCOME]": "Income",
            "Service Revenue [INCOME]": "Income",
            
            # EXPENSES
            "Cost of Goods Sold [EXPENSE]": "Expenses",
            "Rent Expense [EXPENSE]": "Expenses",
            "Salaries Expense [EXPENSE]": "Expenses",
            "Utilities Expense [EXPENSE]": "Expenses"
        }
        
        self.normal_balances = {
            "Assets": "Debit",
            "Liabilities": "Credit", 
            "Equities": "Credit",
            "Income": "Credit",
            "Expenses": "Debit"
        }

    def get_account_type(self, account_name):
        """Get the type of account (Asset, Liability, etc.)"""
        return self.account_types.get(account_name, "Unknown")

    def get_normal_balance(self, account_name):
        """Get the normal balance side for an account"""
        account_type = self.get_account_type(account_name)
        return self.normal_balances.get(account_type, "Unknown")

    def calculate_account_balances(self):
        """Calculate current balances for all accounts from transactions"""
        balances = defaultdict(float)
        
        try:
            if not os.path.exists("transactions.csv"):
                return balances
                
            with open("transactions.csv", mode="r", newline="", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(key in row for key in ["Debit", "Credit", "Amount"]):
                        debit_account = row["Debit"]
                        credit_account = row["Credit"]
                        amount = float(row["Amount"])
                        
                        # Add to debit account (increases asset/expense, decreases liability/equity/income)
                        balances[debit_account] += amount
                        
                        # Subtract from credit account (increases liability/equity/income, decreases asset/expense)
                        balances[credit_account] -= amount
                        
        except Exception as e:
            print(f"Error calculating balances: {e}")
            
        return balances

    def get_accounts_by_type(self):
        """Get all accounts organized by type"""
        accounts_by_type = {
            "Assets": [],
            "Liabilities": [],
            "Equities": [],
            "Income": [],
            "Expenses": []
        }
        
        balances = self.calculate_account_balances()
        
        # Show ALL accounts, even those with zero balances
        for account_name, account_type in self.account_types.items():
            balance = balances.get(account_name, 0.0)
            normal_balance = self.get_normal_balance(account_name)
            
            # For accounts with credit normal balance, show positive balance as credit
            if normal_balance == "Credit" and balance < 0:
                balance = abs(balance)
                balance_type = "Credit"
            elif normal_balance == "Debit" and balance > 0:
                balance_type = "Debit"
            elif normal_balance == "Credit" and balance > 0:
                balance_type = "Credit"
            else:
                balance_type = "Debit"
                balance = abs(balance)
            
            accounts_by_type[account_type].append({
                "name": account_name,
                "balance": balance,
                "balance_type": balance_type,
                "normal_balance": normal_balance
            })
        
        # Sort accounts within each type alphabetically
        for account_type in accounts_by_type:
            accounts_by_type[account_type].sort(key=lambda x: x['name'])
        
        return accounts_by_type

    def get_total_by_type(self, account_type):
        """Get total balance for a specific account type"""
        accounts = self.get_accounts_by_type().get(account_type, [])
        total = 0.0
        
        for account in accounts:
            if account["balance_type"] == "Debit":
                total += account["balance"]
            else:
                total -= account["balance"]
                
        return abs(total)

    def get_all_accounts_summary(self):
        """Get summary of all accounts with totals"""
        accounts_by_type = self.get_accounts_by_type()
        summary = {}
        
        for account_type, accounts in accounts_by_type.items():
            total = self.get_total_by_type(account_type)
            summary[account_type] = {
                "accounts": accounts,
                "total": total
            }
            
        return summary
