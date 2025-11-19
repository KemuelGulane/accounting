import csv
import os
from datetime import datetime

class GeneralJournal:
    def __init__(self):
        self.journal_entries = []
        self.load_journal_entries()
    
    def load_journal_entries(self):
        """Load journal entries from transactions.csv"""
        self.journal_entries = []
        
        try:
            # Check parent directory first, then current directory for transactions.csv
            csv_file = "../transactions.csv"
            if not os.path.exists(csv_file):
                csv_file = "transactions.csv"
                if not os.path.exists(csv_file):
                    return
                
            with open(csv_file, mode="r", newline="", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(key in row for key in ["Date", "Description", "Debit", "Credit", "Amount"]):
                        # Create two journal entries for each transaction (debit and credit)
                        self.journal_entries.append({
                            "Date": row["Date"],
                            "Description": row["Description"],
                            "Account": row["Debit"],
                            "Debit": row["Amount"],
                            "Credit": ""
                        })
                        
                        self.journal_entries.append({
                            "Date": "",
                            "Description": "",
                            "Account": row["Credit"],
                            "Debit": "",
                            "Credit": row["Amount"]
                        })
                        
        except Exception as e:
            print(f"Error loading journal entries: {e}")
    
    def get_all_journal_entries(self):
        """Return all journal entries"""
        return self.journal_entries
    
    def search_journal_entries(self, search_term=""):
        """Search journal entries by date, description, or account"""
        if not search_term:
            return self.journal_entries
            
        search_lower = search_term.lower()
        filtered_entries = []
        
        # Process entries in pairs (each transaction has 2 entries)
        i = 0
        while i < len(self.journal_entries):
            entry1 = self.journal_entries[i]
            
            # Check if this is a complete transaction pair (first entry has date and description)
            if entry1["Date"] and entry1["Description"]:
                # Get the second entry (next entry should be the credit side)
                entry2 = self.journal_entries[i + 1] if i + 1 < len(self.journal_entries) else None
                
                # Check if any entry in this transaction matches the search
                transaction_matches = False
                if (search_lower in entry1["Date"].lower() or 
                    search_lower in entry1["Description"].lower() or 
                    search_lower in entry1["Account"].lower()):
                    transaction_matches = True
                elif entry2 and search_lower in entry2["Account"].lower():
                    transaction_matches = True
                
                # If transaction matches, add both entries
                if transaction_matches:
                    filtered_entries.append(entry1)
                    if entry2:
                        filtered_entries.append(entry2)
                
                # Move to next transaction pair
                i += 2
            else:
                # Skip entries without proper transaction structure
                i += 1
                
        return filtered_entries
    
    def get_journal_entries_by_date_range(self, start_date, end_date):
        """Get journal entries within a specific date range"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            filtered_entries = []
            for entry in self.journal_entries:
                if entry["Date"]:
                    entry_date = datetime.strptime(entry["Date"], '%Y-%m-%d')
                    if start <= entry_date <= end:
                        filtered_entries.append(entry)
                        
            return filtered_entries
            
        except ValueError:
            return []
    
    def get_totals(self, entries=None):
        """Calculate total debits and credits for given entries"""
        if entries is None:
            entries = self.journal_entries
            
        total_debits = 0.0
        total_credits = 0.0
    
        for entry in entries:
            if entry["Debit"]:
                try:
                    total_debits += float(entry["Debit"])
                except ValueError:
                    pass
            if entry["Credit"]:
                try:
                    total_credits += float(entry["Credit"])
                except ValueError:
                    pass
                    
        return total_debits, total_credits



                