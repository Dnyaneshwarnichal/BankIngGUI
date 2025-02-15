import tkinter as tk
from tkinter import messagebox

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self.balance}"

class BankingSystem:
    def __init__(self, root):
        self.accounts = {}

        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x500")  # Increased size for better fitting
        self.root.config(bg="#f4f4f9")  # Light background color for the entire window

        # Widgets for account creation
        self.create_account_frame = tk.Frame(root, bg="#f4f4f9")
        self.create_account_frame.pack(pady=10)

        self.acc_num_label = tk.Label(self.create_account_frame, text="Account Number:", bg="#f4f4f9", font=("Helvetica", 12))
        self.acc_num_label.grid(row=0, column=0)
        self.acc_num_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 12))
        self.acc_num_entry.grid(row=0, column=1)

        self.acc_holder_label = tk.Label(self.create_account_frame, text="Account Holder:", bg="#f4f4f9", font=("Helvetica", 12))
        self.acc_holder_label.grid(row=1, column=0)
        self.acc_holder_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 12))
        self.acc_holder_entry.grid(row=1, column=1)

        self.initial_balance_label = tk.Label(self.create_account_frame, text="Initial Balance:", bg="#f4f4f9", font=("Helvetica", 12))
        self.initial_balance_label.grid(row=2, column=0)
        self.initial_balance_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 12))
        self.initial_balance_entry.grid(row=2, column=1)

        self.create_acc_button = tk.Button(self.create_account_frame, text="Create Account", command=self.create_account, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.create_acc_button.grid(row=3, columnspan=2, pady=5)

        # Widgets for transactions
        self.transaction_frame = tk.Frame(root, bg="#f4f4f9")
        self.transaction_frame.pack(pady=10)

        self.trans_acc_num_label = tk.Label(self.transaction_frame, text="Account Number:", bg="#f4f4f9", font=("Helvetica", 12))
        self.trans_acc_num_label.grid(row=0, column=0)
        self.trans_acc_num_entry = tk.Entry(self.transaction_frame, font=("Helvetica", 12))
        self.trans_acc_num_entry.grid(row=0, column=1)

        self.amount_label = tk.Label(self.transaction_frame, text="Amount:", bg="#f4f4f9", font=("Helvetica", 12))
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.transaction_frame, font=("Helvetica", 12))
        self.amount_entry.grid(row=1, column=1)

        self.deposit_button = tk.Button(self.transaction_frame, text="Deposit", command=self.deposit, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        self.deposit_button.grid(row=2, column=0, pady=5)

        self.withdraw_button = tk.Button(self.transaction_frame, text="Withdraw", command=self.withdraw, bg="#F44336", fg="white", font=("Helvetica", 12, "bold"))
        self.withdraw_button.grid(row=2, column=1, pady=5)

        # Widgets for account information
        self.info_frame = tk.Frame(root, bg="#f4f4f9")
        self.info_frame.pack(pady=10)

        self.info_acc_num_label = tk.Label(self.info_frame, text="Account Number:", bg="#f4f4f9", font=("Helvetica", 12))
        self.info_acc_num_label.grid(row=0, column=0)
        self.info_acc_num_entry = tk.Entry(self.info_frame, font=("Helvetica", 12))
        self.info_acc_num_entry.grid(row=0, column=1)

        self.info_button = tk.Button(self.info_frame, text="Display Info", command=self.display_info, bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"))
        self.info_button.grid(row=1, columnspan=2, pady=5)

    def create_account(self):
        acc_num = self.acc_num_entry.get()
        acc_holder = self.acc_holder_entry.get()
        try:
            initial_balance = float(self.initial_balance_entry.get())
            if acc_num and acc_holder:
                self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
                self.show_custom_message("Success", "Account created successfully!")
            else:
                self.show_custom_message("Error", "Account number and holder name cannot be empty!", "error")
        except ValueError:
            self.show_custom_message("Error", "Invalid initial balance. Please enter a valid number!", "error")

    def deposit(self):
        acc_num = self.trans_acc_num_entry.get()
        try:
            amount = float(self.amount_entry.get())

            if acc_num in self.accounts:
                try:
                    self.accounts[acc_num].deposit(amount)
                    self.show_custom_message("Success", f"Deposited {amount}. New balance is {self.accounts[acc_num].get_balance()}!")
                except ValueError as e:
                    self.show_custom_message("Error", str(e), "error")
            else:
                self.show_custom_message("Error", "Account not found!", "error")
        except ValueError:
            self.show_custom_message("Error", "Please enter a valid amount.", "error")

    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get()
        try:
            amount = float(self.amount_entry.get())

            if acc_num in self.accounts:
                try:
                    self.accounts[acc_num].withdraw(amount)
                    self.show_custom_message("Success", f"Withdrew {amount}. New balance is {self.accounts[acc_num].get_balance()}!")
                except InsufficientFundsError as e:
                    self.show_custom_message("Error", str(e), "error")
                except ValueError as e:
                    self.show_custom_message("Error", str(e), "error")
            else:
                self.show_custom_message("Error", "Account not found!", "error")
        except ValueError:
            self.show_custom_message("Error", "Please enter a valid amount.", "error")

    def display_info(self):
        acc_num = self.info_acc_num_entry.get()

        if acc_num in self.accounts:
            account_info = self.accounts[acc_num].display_account_info()
            self.show_custom_message("Account Info", account_info)
        else:
            self.show_custom_message("Error", "Account not found!", "error")

    def show_custom_message(self, title, message, msg_type="info"):
        popup = tk.Toplevel(self.root)
        popup.geometry("500x250")  # Increased dialog box size
        popup.title(title)
        popup.config(bg="#f4f4f9")

        label = tk.Label(popup, text=message, font=("Helvetica", 14), bg="#f4f4f9", wraplength=450)
        label.pack(pady=30)

        button = tk.Button(popup, text="OK", command=popup.destroy, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        button.pack(pady=10)

        if msg_type == "error":
            label.config(fg="red")
            button.config(bg="#F44336")

        popup.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
