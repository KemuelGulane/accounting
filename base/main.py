import tkinter as tk
from tkinter import ttk, messagebox
from transaction_records import add_transaction, get_all_transactions
from accounts_manager import AccountsManager
from general_journal import GeneralJournal
from general_ledger import GeneralLedger
from balance_sheet import create_balance_sheet_tab
import csv
import re
from datetime import datetime
from tkcalendar import DateEntry

# Gihimo ni nga custom Combobox aron flexible ang pagpangita sa accounts (Bisaya note)
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

# Main window setup sa app (dinhi magsugod ang tanan widgets)
Lobot = tk.Tk()
Lobot.title("Accounting System")
Lobot.state('zoomed')
Lobot.configure(bg="#f0f2f5")

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#f0f2f5", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 16, "bold"), padding=[30, 15], background="#ffffff", foreground="#2c3e50")
style.map("TNotebook.Tab", background=[("selected", "#3498db"), ("active", "#ecf0f1")])
style.configure("TFrame", background="#f0f2f5")
Lobot.option_add('*TCombobox*Listbox.font', ('Segoe UI', 16))

header_frame = tk.Frame(Lobot, bg="#2c3e50", height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

title_label = tk.Label(
    header_frame,
    text="ACCOUNTING SYSTEM",
    font=("Segoe UI", 28, "bold"),
    bg="#2c3e50",
    fg="yellow"
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

tabControl = ttk.Notebook(Lobot)
tabControl.pack(expand=1, fill="both", padx=10, pady=10)

tab_names = [
    'New Transaction',
    'Transactions',
    'Accounts',
    'General Journal',
    'General Legder',
    'Balance Sheet'
]
tabs = []
for name in tab_names:
    tab = ttk.Frame(tabControl)
    tabControl.add(tab, text=name)
    tabs.append(tab)

tab1 = tabs[0]
tab2 = tabs[1]
tab3 = tabs[2]
tab4 = tabs[3]
tab5 = tabs[4]
tab6 = tabs[5]

accounts_manager = AccountsManager()
general_journal = GeneralJournal()
general_ledger = GeneralLedger()

content_frame = tk.Frame(tab1, bg="#ffffff", bd=0, relief="flat")
content_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.85)

shadow_frame = tk.Frame(tab1, bg="#34495e", height=4)
shadow_frame.place(relx=0.02, rely=0.89, relwidth=0.95)

def on_focus_in(event):
    try:
        event.widget.config(highlightbackground="#3498db", highlightcolor="#3498db", highlightthickness=2)
    except tk.TclError:
        pass

def on_focus_out(event):
    try:
        event.widget.config(highlightbackground="#bdc3c7", highlightcolor="#bdc3c7", highlightthickness=1)
    except tk.TclError:
        pass

FIELD_WIDTH = 40

# Helper sa paghimo ug entry box nga pareha tanan
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

# Helper para sa combobox nga naay autocomplete
def create_combo(parent, values):
    frame = tk.Frame(parent, bg="#ecf0f1", bd=2, relief="solid")

    combo_style = ttk.Style()
    combo_style.configure("Large.TCombobox", font=("Segoe UI", 16), padding=10, fieldbackground="#ffffff")

    combo = AutocompleteCombobox(frame, style="Large.TCombobox", width=FIELD_WIDTH - 2)
    combo.set_completion_list(values)
    combo.pack(fill="x", padx=2, pady=2)

    return frame, combo

    

tk.Label(content_frame, text="📅 Date (YYYY-MM-DD):", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=20, pady=20, sticky="e")
date_entry = DateEntry(
    content_frame,
    font=("Segoe UI", 16),
    width=FIELD_WIDTH - 4,
    date_pattern="yyyy-mm-dd",
    background="#3498db",
    foreground="#ffffff",
    borderwidth=2,
    relief="solid",
    state="normal"
)
date_entry.bind("<FocusIn>", on_focus_in)
date_entry.bind("<FocusOut>", on_focus_out)
date_entry.delete(0, tk.END)
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

# Pag-load sa mga transaksyon ug optional filter (Bisaya)
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

# Pagtangtang sa napiling transaksyon (Bisaya)
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

menu = tk.Menu(Lobot, tearoff=0)
menu.add_command(label="Delete Transaction", command=delete_transaction)

def show_context_menu(event):
    row_id = tree.identify_row(event.y)
    if row_id:
        tree.selection_set(row_id)
        menu.post(event.x_root, event.y_root)

tree.bind("<Button-3>", show_context_menu)

# Mosusi nga sakto ang format sa petsa (Bisaya)
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Mosusi nga positive ug numero ang kantidad (Bisaya)
def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

# Mosusi nga napuno ang account nga field (Bisaya)
def validate_account(account_str):
    return account_str.strip() != ""

# Nag-save sa bag-ong transaksyon ngadto sa CSV ug UI (Bisaya)
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
        # Refresh general journal if it exists
        try:
            general_journal.load_journal_entries()
        except:
            pass
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

# Nag-render sa Accounts tab ug chart of accounts (Bisaya)
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

# UI logic para sa General Journal tab (Bisaya)
def create_general_journal_tab():
    """Create the General Journal tab with journal entries display"""
    # Title
    title_label = tk.Label(
        tab4,
        text="📋 GENERAL JOURNAL",
        font=("Segoe UI", 24, "bold"),
        bg="#f0f2f5",
        fg="#2c3e50"
    )
    title_label.pack(pady=(20, 10))
    
    # Search frame
    search_frame = tk.Frame(tab4, bg="#ffffff", bd=2, relief="solid")
    search_frame.pack(fill="x", padx=20, pady=(0, 10))
    
    tk.Label(search_frame, text="🔍 Search Journal:", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(side="left", padx=(15, 15))
    
    journal_search_entry = tk.Entry(
        search_frame, 
        font=("Segoe UI", 14), 
        width=40, 
        bd=2, 
        relief="solid",
        bg="#f8f9fa",
        fg="#2c3e50",
        insertbackground="#3498db"
    )
    journal_search_entry.insert(0, "Type to search journal entries...")
    journal_search_entry.config(fg="gray")
    journal_search_entry.pack(side="left", padx=(0, 15))
    
    def on_journal_search_focus_in(event):
        if journal_search_entry.get() == "Type to search journal entries...":
            journal_search_entry.delete(0, tk.END)
            journal_search_entry.config(fg="black")
    
    def on_journal_search_focus_out(event):
        if not journal_search_entry.get():
            journal_search_entry.insert(0, "Type to search journal entries...")
            journal_search_entry.config(fg="gray")
    
    journal_search_entry.bind("<FocusIn>", on_journal_search_focus_in)
    journal_search_entry.bind("<FocusOut>", on_journal_search_focus_out)
    
    def clear_journal_search():
        journal_search_entry.delete(0, tk.END)
        journal_search_entry.insert(0, "Type to search journal entries...")
        journal_search_entry.config(fg="gray")
        load_journal_entries()
    
    def search_journal_entries(event=None):
        search_term = journal_search_entry.get().strip()
        if search_term == "Type to search journal entries...":
            search_term = ""
        load_journal_entries(search_term)
    
    clear_journal_btn = tk.Button(
        search_frame,
        text="🗑️ Clear",
        command=clear_journal_search,
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
    clear_journal_btn.pack(side="left")

    refresh_journal_btn = tk.Button(
        search_frame,
        text="🔄 Refresh",
        command=lambda: load_journal_entries(
            journal_search_entry.get().strip() if journal_search_entry.get() != "Type to search journal entries..." else ""
        ),
        font=("Segoe UI", 12, "bold"),
        bg="#27ae60",
        fg="white",
        padx=20,
        pady=8,
        relief="flat",
        bd=0,
        cursor="hand2",
        activebackground="#229954",
        activeforeground="white"
    )
    refresh_journal_btn.pack(side="left", padx=(10, 0))
    
    journal_search_entry.bind("<KeyRelease>", search_journal_entries)
    
    # Journal entries tree
    journal_columns = ("Date", "Description", "Account", "Debit", "Credit")
    journal_tree = ttk.Treeview(tab4, columns=journal_columns, show="headings", height=25)
    
    style.configure("Journal.Treeview", font=("Segoe UI", 11), rowheight=25)
    style.configure("Journal.Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#27ae60", foreground="white")
    
    journal_tree.configure(style="Journal.Treeview")
    
    # Configure column widths
    journal_tree.heading("Date", text="Date")
    journal_tree.heading("Description", text="Description")
    journal_tree.heading("Account", text="Account")
    journal_tree.heading("Debit", text="Debit")
    journal_tree.heading("Credit", text="Credit")
    
    journal_tree.column("Date", width=120, anchor="center")
    journal_tree.column("Description", width=300, anchor="w")
    journal_tree.column("Account", width=250, anchor="w")
    journal_tree.column("Debit", width=120, anchor="e")
    journal_tree.column("Credit", width=120, anchor="e")
    
    journal_tree.pack(expand=True, fill="both", padx=20, pady=(0, 10))
    
    # Scrollbar for journal
    journal_scrollbar = ttk.Scrollbar(tab4, orient="vertical", command=journal_tree.yview)
    journal_tree.configure(yscroll=journal_scrollbar.set)
    journal_scrollbar.pack(side="right", fill="y", padx=(0, 20))
    
    def load_journal_entries(search_term=""):
        """Load journal entries into the tree view"""
        try:
            # Clear existing entries
            for item in journal_tree.get_children():
                journal_tree.delete(item)
            
            # Reload journal entries from transactions
            general_journal.load_journal_entries()
            
            # Get filtered entries
            if search_term:
                entries = general_journal.search_journal_entries(search_term)
            else:
                entries = general_journal.get_all_journal_entries()
            
            # Add entries to tree
            for entry in entries:
                journal_tree.insert("", "end", values=(
                    entry["Date"],
                    entry["Description"],
                    entry["Account"],
                    f"₱{entry['Debit']}" if entry["Debit"] else "",
                    f"₱{entry['Credit']}" if entry["Credit"] else ""
                ))
            
            # Add totals row
            total_debits, total_credits = general_journal.get_totals(entries)
            journal_tree.insert("", "end", values=(
                "", "", "TOTALS:",
                f"₱{total_debits:,.2f}",
                f"₱{total_credits:,.2f}"
            ))
            
            # Style the totals row
            totals_item = journal_tree.get_children()[-1]
            journal_tree.set(totals_item, "Date", "")
            journal_tree.set(totals_item, "Description", "")
            journal_tree.set(totals_item, "Account", "TOTALS:")
            journal_tree.set(totals_item, "Debit", f"₱{total_debits:,.2f}")
            journal_tree.set(totals_item, "Credit", f"₱{total_credits:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load journal entries: {str(e)}")
    
    # Load initial data
    load_journal_entries()

# UI ug data reload para sa General Ledger tab (Bisaya)
def create_general_ledger_tab():
    """Create the General Ledger tab."""
    # Title
    title_label = tk.Label(
        tab5,
        text="📚 GENERAL LEGDER",
        font=("Segoe UI", 24, "bold"),
        bg="#f0f2f5",
        fg="#2c3e50"
    )
    title_label.pack(pady=(20, 10))

    search_frame = tk.Frame(tab5, bg="#ffffff", bd=2, relief="solid")
    search_frame.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(
        search_frame,
        text="🔍 Search Ledger:",
        font=("Segoe UI", 16, "bold"),
        bg="#ffffff",
        fg="#2c3e50"
    ).pack(side="left", padx=(15, 15))

    ledger_search_entry = tk.Entry(
        search_frame,
        font=("Segoe UI", 14),
        width=40,
        bd=2,
        relief="solid",
        bg="#f8f9fa",
        fg="#2c3e50",
        insertbackground="#3498db"
    )
    ledger_search_entry.insert(0, "Type to search ledger...")
    ledger_search_entry.config(fg="gray")
    ledger_search_entry.pack(side="left", padx=(0, 15))

    def on_ledger_search_focus_in(event):
        if ledger_search_entry.get() == "Type to search ledger...":
            ledger_search_entry.delete(0, tk.END)
            ledger_search_entry.config(fg="black")

    def on_ledger_search_focus_out(event):
        if not ledger_search_entry.get():
            ledger_search_entry.insert(0, "Type to search ledger...")
            ledger_search_entry.config(fg="gray")

    ledger_search_entry.bind("<FocusIn>", on_ledger_search_focus_in)
    ledger_search_entry.bind("<FocusOut>", on_ledger_search_focus_out)

    def clear_ledger_search():
        ledger_search_entry.delete(0, tk.END)
        ledger_search_entry.insert(0, "Type to search ledger...")
        ledger_search_entry.config(fg="gray")
        load_ledger_entries()

    def search_ledger_entries(event=None):
        search_term = ledger_search_entry.get().strip()
        if search_term == "Type to search ledger...":
            search_term = ""
        load_ledger_entries(search_term)

    clear_ledger_btn = tk.Button(
        search_frame,
        text="🗑️ Clear",
        command=clear_ledger_search,
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
    clear_ledger_btn.pack(side="left")

    refresh_ledger_btn = tk.Button(
        search_frame,
        text="🔄 Refresh",
        command=lambda: load_ledger_entries(
            ledger_search_entry.get().strip() if ledger_search_entry.get() != "Type to search ledger..." else ""
        ),
        font=("Segoe UI", 12, "bold"),
        bg="#8e44ad",
        fg="white",
        padx=20,
        pady=8,
        relief="flat",
        bd=0,
        cursor="hand2",
        activebackground="#7d3c98",
        activeforeground="white"
    )
    refresh_ledger_btn.pack(side="left", padx=(10, 0))

    ledger_search_entry.bind("<KeyRelease>", search_ledger_entries)

    ledger_columns = ("Date", "Description", "Debit Account", "Credit Account", "Amount", "Balance")
    ledger_tree = ttk.Treeview(tab5, columns=ledger_columns, show="headings", height=25)

    style.configure("Ledger.Treeview", font=("Segoe UI", 11), rowheight=28)
    style.configure("Ledger.Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#8e44ad", foreground="white")
    ledger_tree.configure(style="Ledger.Treeview")

    for col, width in zip(ledger_columns, [120, 280, 220, 220, 140, 140]):
        ledger_tree.heading(col, text=col)
        anchor = "e" if col in ("Amount", "Balance") else ("center" if col == "Date" else "w")
        ledger_tree.column(col, width=width, anchor=anchor)

    ledger_tree.pack(expand=True, fill="both", padx=20, pady=(0, 10))

    ledger_scrollbar = ttk.Scrollbar(tab5, orient="vertical", command=ledger_tree.yview)
    ledger_tree.configure(yscroll=ledger_scrollbar.set)
    ledger_scrollbar.pack(side="right", fill="y", padx=(0, 20))

    totals_label = tk.Label(
        tab5,
        text="",
        font=("Segoe UI", 14, "bold"),
        bg="#f0f2f5",
        fg="#2c3e50"
    )
    totals_label.pack(pady=(0, 20))

    def load_ledger_entries(search_term=""):
        try:
            ledger_tree.delete(*ledger_tree.get_children())
            general_ledger.load_ledger_entries()
            entries = general_ledger.search_entries(search_term)

            for entry in entries:
                ledger_tree.insert(
                    "",
                    "end",
                    values=(
                        entry["Date"],
                        entry["Description"],
                        entry["Debit"],
                        entry["Credit"],
                        f"₱{entry['Amount']:,.2f}",
                        f"₱{entry['Balance']:,.2f}"
                    )
                )

            total_amount, last_balance = general_ledger.get_totals(entries)
            totals_label.config(
                text=f"Total Amount: ₱{total_amount:,.2f}   |   Running Balance: ₱{last_balance:,.2f}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ledger entries: {str(e)}")

    load_ledger_entries()


# Pag-instansya sa tanan tabs (Bisaya)
# Create General Journal tab
create_general_journal_tab()

# Create General Ledger tab
create_general_ledger_tab()

# Create Balance Sheet tab
create_balance_sheet_tab(tab6, accounts_manager)

load_transactions()

Lobot.mainloop()
