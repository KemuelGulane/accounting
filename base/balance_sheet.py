import tkinter as tk
from tkinter import ttk, messagebox


# Nag-set up sa Balance Sheet tab nga adunay Assets ug Liabilities/Equity (Bisaya)
def create_balance_sheet_tab(tab, accounts_manager):
    """Render Balance Sheet tab with Assets and Liabilities & Equity containers."""
    title_label = tk.Label(
        tab,
        text="📈 BALANCE SHEET",
        font=("Segoe UI", 24, "bold"),
        bg="#f0f2f5",
        fg="#2c3e50"
    )
    title_label.pack(pady=(20, 10))

    container = tk.Frame(tab, bg="#f0f2f5")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    cards_frame = tk.Frame(container, bg="#f0f2f5")
    cards_frame.pack(fill="both", expand=True)

    assets_frame = tk.Frame(cards_frame, bg="#ffffff", bd=2, relief="solid")
    assets_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    liabilities_frame = tk.Frame(cards_frame, bg="#ffffff", bd=2, relief="solid")
    liabilities_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

    tk.Label(
        assets_frame,
        text="💼 Assets",
        font=("Segoe UI", 20, "bold"),
        bg="#ffffff",
        fg="#27ae60"
    ).pack(fill="x", pady=(0, 10), padx=10)

    tk.Label(
        liabilities_frame,
        text="⚖️ Liabilities & Equity",
        font=("Segoe UI", 20, "bold"),
        bg="#ffffff",
        fg="#c0392b"
    ).pack(fill="x", pady=(0, 10), padx=10)

    assets_tree = ttk.Treeview(
        assets_frame,
        columns=("Account", "Amount"),
        show="headings",
        height=12
    )
    assets_tree.heading("Account", text="Account")
    assets_tree.heading("Amount", text="Amount")
    assets_tree.column("Account", width=300, anchor="w")
    assets_tree.column("Amount", width=150, anchor="e")
    assets_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    liabilities_tree = ttk.Treeview(
        liabilities_frame,
        columns=("Account", "Amount"),
        show="headings",
        height=12
    )
    liabilities_tree.heading("Account", text="Account")
    liabilities_tree.heading("Amount", text="Amount")
    liabilities_tree.column("Account", width=300, anchor="w")
    liabilities_tree.column("Amount", width=150, anchor="e")
    liabilities_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    assets_total_label = tk.Label(
        assets_frame,
        text="Total Assets: ₱0.00",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
        fg="#27ae60"
    )
    assets_total_label.pack(pady=(0, 10))

    liabilities_total_label = tk.Label(
        liabilities_frame,
        text="Total Liabilities & Equity: ₱0.00",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
        fg="#c0392b"
    )
    liabilities_total_label.pack(pady=(0, 10))

    def populate_balance_sheet():
        try:
            for tree in (assets_tree, liabilities_tree):
                for item in tree.get_children():
                    tree.delete(item)

            summary = accounts_manager.get_all_accounts_summary()

            assets_data = summary.get("Assets", {"accounts": [], "total": 0.0})
            liabilities_data = summary.get("Liabilities", {"accounts": [], "total": 0.0})
            equities_data = summary.get("Equities", {"accounts": [], "total": 0.0})

            for account in assets_data["accounts"]:
                assets_tree.insert(
                    "",
                    "end",
                    values=(account["name"], f"₱{account['balance']:,.2f}")
                )

            liabilities_tree.insert("", "end", values=("— Liabilities —", ""))
            for account in liabilities_data["accounts"]:
                liabilities_tree.insert(
                    "",
                    "end",
                    values=(account["name"], f"₱{account['balance']:,.2f}")
                )

            liabilities_tree.insert("", "end", values=("— Equity —", ""))
            for account in equities_data["accounts"]:
                liabilities_tree.insert(
                    "",
                    "end",
                    values=(account["name"], f"₱{account['balance']:,.2f}")
                )

            assets_total_label.config(text=f"Total Assets: ₱{assets_data['total']:,.2f}")
            liabilities_equity_total = liabilities_data["total"] + equities_data["total"]
            liabilities_total_label.config(
                text=f"Total Liabilities & Equity: ₱{liabilities_equity_total:,.2f}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load balance sheet: {str(e)}")

    refresh_balance_btn = tk.Button(
        container,
        text="🔄 Refresh Balance Sheet",
        command=populate_balance_sheet,
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
    refresh_balance_btn.pack(pady=(10, 0))

    populate_balance_sheet()

