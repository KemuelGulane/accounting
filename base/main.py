import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Accounting System")
root.state('zoomed') 

style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 14, "bold"), padding=[20, 10])

root.option_add('*TCombobox*Listbox.font', ('Arial', 18))
  
tabControl = ttk.Notebook(root)
tabControl.pack(expand=1, fill="both")

tab_names = ['New Transaction', 'Transactions', 'Accounts', 'General Journal', 'Balance Sheet']
tabs = []
for name in tab_names:
    tab = ttk.Frame(tabControl)
    tabControl.add(tab, text=name)
    tabs.append(tab)

tab1 = tabs[0]

content_frame = tk.Frame(tab1, bg="white", bd=2, relief="groove")
content_frame.place(relx=0.02, rely=0.05, relwidth=0.95, relheight=0.85)

def on_focus_in(event):
    event.widget.config(highlightbackground="#4CAF50", highlightcolor="#4CAF50")

def on_focus_out(event):
    event.widget.config(highlightbackground="black", highlightcolor="black")


FIELD_WIDTH = 40

def create_entry(parent):
    entry = tk.Entry(parent, font=("Arial", 18), bd=2, relief="solid", highlightthickness=1, width=FIELD_WIDTH)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

def create_combo(parent, values):
    frame = tk.Frame(parent, bg="black", bd=1, relief="solid")

    combo_style = ttk.Style()
    combo_style.configure(
        "Large.TCombobox",
        font=("Arial", 18),
        padding=8 
    )

    combo = ttk.Combobox(frame, values=values, style="Large.TCombobox", width=FIELD_WIDTH - 2)
    combo.pack(fill="x", padx=1, pady=1)

    return frame, combo

tk.Label(content_frame, text="Date (YYYY-MM-DD):", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=20, pady=15, sticky="e")
date_entry = create_entry(content_frame)
date_entry.grid(row=0, column=1, padx=10, pady=15, sticky="we")

tk.Label(content_frame, text="Description:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=20, pady=15, sticky="e")
desc_entry = create_entry(content_frame)
desc_entry.grid(row=1, column=1, padx=10, pady=15, sticky="we")

tk.Label(content_frame, text="Debit Account:", font=("Arial", 14), bg="white").grid(row=2, column=0, padx=20, pady=15, sticky="e")
debit_frame, debit_combo = create_combo(content_frame, [
    "Cash [ASSET]", "Accounts Receivable [ASSET]", "Inventory [ASSET]",
    "Prepaid Expenses [ASSET]", "Equipment [ASSET]",
    "Accounts Payable [LIABILITY]", "Notes Payable [LIABILITY]",
    "Owner's Capital [EQUITY]"
])
debit_frame.grid(row=2, column=1, padx=10, pady=15, sticky="we")

tk.Label(content_frame, text="Credit Account:", font=("Arial", 14), bg="white").grid(row=3, column=0, padx=20, pady=15, sticky="e")
credit_frame, credit_combo = create_combo(content_frame, [
    "Owner's Capital [EQUITY]", "Revenue [INCOME]"
])
credit_frame.grid(row=3, column=1, padx=10, pady=15, sticky="we")

tk.Label(content_frame, text="Amount:", font=("Arial", 14), bg="white").grid(row=4, column=0, padx=20, pady=15, sticky="e")
amount_entry = create_entry(content_frame)
amount_entry.grid(row=4, column=1, padx=10, pady=15, sticky="we")

# --- Save Button ---
def save_transaction():
    print(f"Date: {date_entry.get()}")
    print(f"Description: {desc_entry.get()}")
    print(f"Debit: {debit_combo.get()}")
    print(f"Credit: {credit_combo.get()}")
    print(f"Amount: {amount_entry.get()}")
    print("Transaction saved!\n")

save_btn = tk.Button(
    content_frame,
    text="Save Transaction",
    command=save_transaction,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=8,
    relief="flat"
)
save_btn.grid(row=5, column=1, padx=10, pady=30, sticky="w")

content_frame.columnconfigure(0, weight=0)

for i, text in enumerate(["Transactions Table (Coming Soon)", "Accounts Section", "General Journal", "Balance Sheet"], start=1):
    tk.Label(tabs[i], text=text, font=("Arial", 14)).pack(pady=50)

# Run app
root.mainloop()
