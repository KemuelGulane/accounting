import csv
import os


# Klase para sa General Ledger data gikan sa CSV (Bisaya)
class GeneralLedger:
    """Simple general ledger loader backed by transactions.csv."""

    REQUIRED_FIELDS = ["Date", "Description", "Debit", "Credit", "Amount"]

    def __init__(self):
        self.ledger_entries = []
        self.load_ledger_entries()

    def _resolve_transactions_path(self):
        """Return the first existing transactions.csv path."""
        potential_paths = ["../transactions.csv", "transactions.csv"]
        for path in potential_paths:
            if os.path.exists(path):
                return path
        return None

    def load_ledger_entries(self):
        """Load transactions and compute a running balance."""
        self.ledger_entries = []
        running_balance = 0.0

        csv_path = self._resolve_transactions_path()
        if not csv_path:
            return

        try:
            with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not all(field in row for field in self.REQUIRED_FIELDS):
                        continue

                    try:
                        amount = float(row["Amount"])
                    except (TypeError, ValueError):
                        amount = 0.0

                    running_balance += amount

                    self.ledger_entries.append(
                        {
                            "Date": row["Date"],
                            "Description": row["Description"],
                            "Debit": row["Debit"],
                            "Credit": row["Credit"],
                            "Amount": amount,
                            "Balance": running_balance,
                        }
                    )
        except Exception as exc:
            print(f"Error loading ledger entries: {exc}")

    def get_all_entries(self):
        return self.ledger_entries

    def search_entries(self, search_term=""):
        if not search_term:
            return self.ledger_entries

        search_lower = search_term.lower()
        filtered = []
        for entry in self.ledger_entries:
            if (
                search_lower in entry["Date"].lower()
                or search_lower in entry["Description"].lower()
                or search_lower in entry["Debit"].lower()
                or search_lower in entry["Credit"].lower()
            ):
                filtered.append(entry)
        return filtered

    def get_totals(self, entries=None):
        entries = entries or self.ledger_entries
        total_amount = 0.0
        last_balance = 0.0

        for entry in entries:
            total_amount += entry.get("Amount", 0.0)
            last_balance = entry.get("Balance", last_balance)

        return total_amount, last_balance

