import tkinter as tk
from tkinter import ttk, messagebox
from transaction_records import add_transaction, get_all_transactions
from accounts_manager import AccountsManager
import csv
import re
from datetime import datetime

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list
        
        self.bind('<KeyRelease>', self._on_keyrelease)
        self.bind('<Button-1>', self._on_click)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<Down>', self._on_down_key)
        self.bind('<Up>', self._on_up_key)
        self.bind('<Return>', self._on_return_key)
        self['state'] = 'normal'

        self.dropdown_open = False
        self._listbox_window = None
        self._listbox_widget = None

    def _on_click(self, event):
        if not self.dropdown_open:
            typed = self.get().strip().lower()
            if typed:
                filtered = [s for s in self._completion_list if typed in s.lower()]
                self['values'] = filtered
            else:
                self['values'] = self._completion_list
            self.dropdown_open = True

    def _on_focus_in(self, event):
        typed = self.get().strip().lower()
        if typed:
            filtered = [s for s in self._completion_list if typed in s.lower()]
            self['values'] = filtered
        else:
            self['values'] = self._completion_list

    def _on_keyrelease(self, event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Return"):
            return
        if event.keysym == "Escape":
            self.dropdown_open = False
            return

        typed = self.get().strip().lower()
        if not typed:
            self['values'] = self._completion_list
        else:
            filtered = [item for item in self._completion_list if typed in item.lower()]
            self['values'] = filtered

    def _on_down_key(self, event):
        self.dropdown_open = True
        return None

    def _on_up_key(self, event):
        self.dropdown_open = True
        return None

    def _on_return_key(self, event):
        self.dropdown_open = False
        return None

    def _hide_suggestions(self):
        self.dropdown_open = False

root = tk.Tk()
root.title("Accounting System")
root.state('zoomed')
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#f0f2f5", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 16, "bold"), padding=[30, 15], background="#ffffff", foreground="#2c3e50")
style.map("TNotebook.Tab", background=[("selected", "#3498db"), ("active", "#ecf0f1")])
style.configure("TFrame", background="#f0f2f5")
root.option_add('*TCombobox*Listbox.font', ('Segoe UI', 16))

header_frame = tk.Frame(root, bg="#2c3e50", height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

title_label = tk.Label(
    header_frame,
    text="ACCOUNTING SYSTEM",
    font=("Segoe UI", 28, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1"
)
title_label.pack(expand=True)

subtitle_label = tk.Label(
    header_frame,
    text="BSIT 2-A ACCOUNTING PROGRAM",
    font=("Segoe UI", 12),
    bg="#2c3e50",
    fg="#bdc3c7"
)
subtitle_label.pack()

tabControl = ttk.Notebook(root)
tabControl.pack(expand=1, fill="both", padx=10, pady=10)

tab_names = ['New Transaction', 'Transactions', 'Accounts', 'General Journal', 'Balance Sheet']
tabs = []
for name in tab_names:
    tab = ttk.Frame(tabControl)
    tabControl.add(tab, text=name)
    tabs.append(tab)

tab1 = tabs[0]
tab2 = tabs[1]
tab3 = tabs[2]

accounts_manager = AccountsManager()

content_frame = tk.Frame(tab1, bg="#ffffff", bd=0, relief="flat")
content_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.85)

shadow_frame = tk.Frame(tab1, bg="#34495e", height=4)
shadow_frame.place(relx=0.02, rely=0.89, relwidth=0.95)

def on_focus_in(event):
    event.widget.config(highlightbackground="#3498db", highlightcolor="#3498db", highlightthickness=2)

def on_focus_out(event):
    event.widget.config(highlightbackground="#bdc3c7", highlightcolor="#bdc3c7", highlightthickness=1)

FIELD_WIDTH = 40

def create_entry(parent):
    entry = tk.Entry(
        parent, 
        font=("Segoe UI", 16), 
        bd=2, 
        relief="solid", 
        highlightthickness=1, 
        width=FIELD_WIDTH,
        bg="#ffffff",
        fg="#2c3e50",
        insertbackground="#3498db"
    )
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

def create_combo(parent, values):
    frame = tk.Frame(parent, bg="#ecf0f1", bd=2, relief="solid")

    combo_style = ttk.Style()
    combo_style.configure("Large.TCombobox", font=("Segoe UI", 16), padding=10, fieldbackground="#ffffff")

    combo = AutocompleteCombobox(frame, style="Large.TCombobox", width=FIELD_WIDTH - 2)
    combo.set_completion_list(values)
    combo.pack(fill="x", padx=2, pady=2)

    return frame, combo

    

tk.Label(content_frame, text="📅 Date (YYYY-MM-DD):", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=20, pady=20, sticky="e")
date_entry = create_entry(content_frame)
date_entry.grid(row=0, column=1, padx=10, pady=20, sticky="we")

tk.Label(content_frame, text="📝 Description:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=1, column=0, padx=20, pady=20, sticky="e")
desc_entry = create_entry(content_frame)
desc_entry.grid(row=1, column=1, padx=10, pady=20, sticky="we")

tk.Label(content_frame, text="💳 Debit Account:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=2, column=0, padx=20, pady=20, sticky="e")
debit_frame, debit_combo = create_combo(content_frame, [
    "Cash [ASSET]", "Accounts Receivable [ASSET]", "Inventory [ASSET]",
    "Prepaid Expenses [ASSET]", "Equipment [ASSET]",
    "Accounts Payable [LIABILITY]", "Notes Payable [LIABILITY]",
    "Owner's Capital [EQUITY]",
    "Sales Revenue [INCOME]", "Service Revenue [INCOME]", 
    "Cost of Goods Sold [EXPENSE]", "Rent Expense [EXPENSE]", "Salaries Expense [EXPENSE]",
    "Utilities Expense [EXPENSE]"
])
debit_frame.grid(row=2, column=1, padx=10, pady=20, sticky="we")

tk.Label(content_frame, text="💳 Credit Account:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=3, column=0, padx=20, pady=20, sticky="e")
credit_frame, credit_combo = create_combo(content_frame, [
    "Cash [ASSET]", "Accounts Receivable [ASSET]", "Inventory [ASSET]",
    "Prepaid Expenses [ASSET]", "Equipment [ASSET]",
    "Accounts Payable [LIABILITY]", "Notes Payable [LIABILITY]",
    "Owner's Capital [EQUITY]",
    "Sales Revenue [INCOME]", "Service Revenue [INCOME]", 
    "Cost of Goods Sold [EXPENSE]", "Rent Expense [EXPENSE]", "Salaries Expense [EXPENSE]",
    "Utilities Expense [EXPENSE]"
])
credit_frame.grid(row=3, column=1, padx=10, pady=20, sticky="we")

tk.Label(content_frame, text="💰 Amount:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=4, column=0, padx=20, pady=20, sticky="e")
amount_entry = create_entry(content_frame)
amount_entry.grid(row=4, column=1, padx=10, pady=20, sticky="we")

columns = ("Date", "Description", "Debit", "Credit", "Amount")
tree = ttk.Treeview(tab2, columns=columns, show="headings", height=25)

style.configure("Treeview", font=("Segoe UI", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"), background="#3498db", foreground="white")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250, anchor="center")

search_frame = tk.Frame(tab2, bg="#ffffff", bd=2, relief="solid")
search_frame.pack(fill="x", padx=20, pady=(20, 10))

tk.Label(search_frame, text="🔍 Search Transactions:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(side="left", padx=(15, 15))

search_entry = tk.Entry(
    search_frame, 
    font=("Segoe UI", 14), 
    width=40, 
    bd=2, 
    relief="solid",
    bg="#f8f9fa",
    fg="#2c3e50",
    insertbackground="#3498db"
)
search_entry.insert(0, "Type to search transactions...")
search_entry.config(fg="gray")
search_entry.pack(side="left", padx=(0, 15))

def on_search_focus_in(event):
    if search_entry.get() == "Type to search transactions...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")

def on_search_focus_out(event):
    if not search_entry.get():
        search_entry.insert(0, "Type to search transactions...")
        search_entry.config(fg="gray")

search_entry.bind("<FocusIn>", on_search_focus_in)
search_entry.bind("<FocusOut>", on_search_focus_out)

def clear_search():
    search_entry.delete(0, tk.END)
    search_entry.insert(0, "Type to search transactions...")
    search_entry.config(fg="gray")
    load_transactions()

def search_transactions(event=None):
    search_term = search_entry.get().strip()
    if search_term == "Type to search transactions...":
        search_term = ""
    load_transactions(search_term)

clear_btn = tk.Button(
    search_frame,
    text="🗑️ Clear",
    command=clear_search,
    font=("Segoe UI", 12, "bold"),
    bg="#e74c3c",
    fg="white",
    padx=20,
    pady=8,
    relief="flat",
    bd=0,
    cursor="hand2",
    activebackground="#c0392b",
    activeforeground="white"
)
clear_btn.pack(side="left")

search_entry.bind("<KeyRelease>", search_transactions)

tree.pack(expand=True, fill="both", padx=20, pady=(0, 20))

scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

def load_transactions(search_term=""):
    try:
        for item in tree.get_children():
            tree.delete(item)
        
        transactions = get_all_transactions()
        for row in transactions:
            if all(key in row for key in ["Date", "Description", "Debit", "Credit", "Amount"]):
                if search_term:
                    search_lower = search_term.lower()
                    if (search_lower in row["Date"].lower() or 
                        search_lower in row["Description"].lower() or 
                        search_lower in row["Debit"].lower() or 
                        search_lower in row["Credit"].lower() or 
                        search_lower in row["Amount"].lower()):
                        tree.insert("", "end", values=(row["Date"], row["Description"], row["Debit"], row["Credit"], row["Amount"]))
                else:
                    tree.insert("", "end", values=(row["Date"], row["Description"], row["Debit"], row["Credit"], row["Amount"]))
            else:
                print(f"Warning: Skipping malformed transaction row: {row}")
                
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")

def delete_transaction():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a transaction to delete.")
        return

    confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this transaction?")
    if not confirm:
        return

    try:
        values = tree.item(selected[0], "values")
        
        rows = []
        try:
            with open("transactions.csv", mode="r", newline="", encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if [str(v) for v in row] != [str(v) for v in values]:
                        rows.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "Transactions file not found.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error reading transactions file: {str(e)}")
            return

        try:
            with open("transactions.csv", mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)
        except Exception as e:
            messagebox.showerror("Error", f"Error writing transactions file: {str(e)}")
            return

        tree.delete(selected[0])
        messagebox.showinfo("Deleted", "Transaction deleted successfully.")
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Delete Transaction", command=delete_transaction)

def show_context_menu(event):
    row_id = tree.identify_row(event.y)
    if row_id:
        tree.selection_set(row_id)
        menu.post(event.x_root, event.y_root)

tree.bind("<Button-3>", show_context_menu)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

def validate_account(account_str):
    return account_str.strip() != ""

def save_transaction():
    date = date_entry.get().strip()
    desc = desc_entry.get().strip()
    debit = debit_combo.get().strip()
    credit = credit_combo.get().strip()
    amount = amount_entry.get().strip()

    if not date or not desc or not debit or not credit or not amount:
        messagebox.showwarning("Missing Fields", "Please fill out all fields before saving.")
        return
    
    if not validate_date(date):
        messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format (e.g., 2024-01-15).")
        date_entry.focus()
        return
    
    if not validate_amount(amount):
        messagebox.showerror("Invalid Amount", "Please enter a valid positive number for the amount.")
        amount_entry.focus()
        return
    
    if not validate_account(debit) or not validate_account(credit):
        messagebox.showerror("Invalid Account", "Please select valid debit and credit accounts.")
        return
    
    if debit == credit:
        messagebox.showerror("Invalid Transaction", "Debit and credit accounts cannot be the same.")
        return

    try:
        add_transaction(date, desc, debit, credit, amount)

        date_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        debit_combo.set("")
        credit_combo.set("")
        amount_entry.delete(0, tk.END)

        load_transactions()
        messagebox.showinfo("Success", "Transaction saved successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")

save_btn = tk.Button(
    content_frame,
    text="💾 SAVE TRANSACTION",
    command=save_transaction,
    font=("Segoe UI", 18, "bold"),
    bg="#27ae60",
    fg="white",
    padx=50,
    pady=15,
    relief="flat",
    bd=0,
    cursor="hand2",
    activebackground="#2ecc71",
    activeforeground="white"
)
save_btn.grid(row=5, column=1, padx=10, pady=40, sticky="ew")

button_frame = tk.Frame(content_frame, bg="#ffffff")
button_frame.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

cancel_btn = tk.Button(
    button_frame,
    text="🔄 Clear Form",
    command=lambda: (date_entry.delete(0, tk.END), desc_entry.delete(0, tk.END), debit_combo.set(""), credit_combo.set(""), amount_entry.delete(0, tk.END)),
    font=("Segoe UI", 14, "bold"),
    bg="#e74c3c",
    fg="white",
    padx=30,
    pady=10,
    relief="flat",
    bd=0,
    cursor="hand2",
    activebackground="#c0392b",
    activeforeground="white"
)
cancel_btn.pack(side="left", padx=(0, 10))

content_frame.columnconfigure(0, weight=0)

def create_accounts_tab():
    accounts_frame = tk.Frame(tab3, bg="#f0f2f5")
    accounts_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    title_label = tk.Label(
        accounts_frame,
        text="📊 CHART OF ACCOUNTS",
        font=("Segoe UI", 24, "bold"),
        bg="#f0f2f5",
        fg="#2c3e50"
    )
    title_label.pack(pady=(0, 20))
    
    def refresh_accounts():
        for widget in accounts_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != title_label:
                widget.destroy()
        
        summary = accounts_manager.get_all_accounts_summary()
        
        y_position = 80
        
        for account_type, data in summary.items():
            # Show all account types, even if empty
                
            type_frame = tk.Frame(accounts_frame, bg="#ffffff", bd=2, relief="solid")
            type_frame.place(x=20, y=y_position, width=900, height=200)
            
            type_colors = {
                "Assets": "#27ae60",
                "Liabilities": "#e74c3c", 
                "Equities": "#3498db",
                "Income": "#f39c12",
                "Expenses": "#9b59b6"
                }
            
            type_label = tk.Label(
                type_frame,
                text=f"{account_type.upper()}",
                font=("Segoe UI", 16, "bold"),
                bg=type_colors.get(account_type, "#95a5a6"),
                fg="white"
            )
            type_label.pack(fill="x", pady=(0, 10))
            
            accounts_tree = ttk.Treeview(
                type_frame,
                columns=("Account", "Balance"),
                show="headings",
                height=8
            )
            
            style.configure("Accounts.Treeview", font=("Segoe UI", 10))
            style.configure("Accounts.Treeview.Heading", font=("Segoe UI", 10, "bold"))
            
            accounts_tree.heading("Account", text="Account Name")
            accounts_tree.heading("Balance", text="Balance")
            accounts_tree.column("Account", width=400, anchor="w")
            accounts_tree.column("Balance", width=150, anchor="e")
            
            accounts_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            if data["accounts"]:
                for account in data["accounts"]:
                    balance_text = f"{account['balance']:,.2f}"
                    if account["balance_type"] == "Credit":
                        balance_text = f"({balance_text})"
                    
                    accounts_tree.insert("", "end", values=(account['name'], f"₱{balance_text}"))
            else:
                accounts_tree.insert("", "end", values=("No accounts in this category", "₱0.00"))
            
            total_label = tk.Label(
                type_frame,
                text=f"Total {account_type}: ₱{data['total']:,.2f}",
                font=("Segoe UI", 12, "bold"),
                bg="#ffffff",
                fg=type_colors.get(account_type, "#95a5a6")
            )
            total_label.pack(pady=(0, 10))
            
            y_position += 220
    
    refresh_btn = tk.Button(
        accounts_frame,
        text="🔄 Refresh Accounts",
        command=refresh_accounts,
        font=("Segoe UI", 14, "bold"),
        bg="#3498db",
        fg="white",
        padx=20,
        pady=10,
        relief="flat",
        bd=0,
        cursor="hand2",
        activebackground="#2980b9",
        activeforeground="white"
    )
    refresh_btn.place(x=20, y=20)
    
    refresh_accounts()

create_accounts_tab()

for i, text in enumerate(["📋 General Journal", "📈 Balance Sheet"], start=3):
    tk.Label(tabs[i], text=text, font=("Segoe UI", 24, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=100)
    tk.Label(tabs[i], text="Coming Soon...", font=("Segoe UI", 16), bg="#f0f2f5", fg="#7f8c8d").pack()

load_transactions()

root.mainloop()
