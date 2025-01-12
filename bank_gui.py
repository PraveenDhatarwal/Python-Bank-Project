import customtkinter as ctk
from tkinter import messagebox
from register import SignUp, SignIn
from bank import Bank
from database import db_query
import random

class BankApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Bank Management System")
        self.window.geometry("800x600")
        self.current_user = None
        self.account_number = None
        
        # Set the theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.show_main_screen()
    
    def show_main_screen(self):
        self.clear_window()
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Welcome label
        self.label = ctk.CTkLabel(self.main_frame, text="Welcome to Bank Management System", font=("Arial", 24))
        self.label.pack(pady=20)
        
        # Create buttons
        self.create_account_btn = ctk.CTkButton(self.main_frame, text="Create Account", command=self.create_account)
        self.create_account_btn.pack(pady=10)
        
        self.login_btn = ctk.CTkButton(self.main_frame, text="Login", command=self.login)
        self.login_btn.pack(pady=10)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
    def create_account(self):
        account_window = ctk.CTkToplevel(self.window)
        account_window.title("Create Account")
        account_window.geometry("400x600")
        
        ctk.CTkLabel(account_window, text="Create New Account", font=("Arial", 20)).pack(pady=20)
        
        username_entry = ctk.CTkEntry(account_window, placeholder_text="Username")
        username_entry.pack(pady=10)
        
        password_entry = ctk.CTkEntry(account_window, placeholder_text="Password", show="*")
        password_entry.pack(pady=10)
        
        name_entry = ctk.CTkEntry(account_window, placeholder_text="Full Name")
        name_entry.pack(pady=10)
        
        age_entry = ctk.CTkEntry(account_window, placeholder_text="Age")
        age_entry.pack(pady=10)
        
        city_entry = ctk.CTkEntry(account_window, placeholder_text="City")
        city_entry.pack(pady=10)
        
        def submit():
            username = username_entry.get()
            password = password_entry.get()
            name = name_entry.get()
            age = age_entry.get()
            city = city_entry.get()
            
            # Generate unique account number
            while True:
                account_number = random.randint(10000000, 99999999)
                temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
                if not temp:
                    break
            
            try:
                from customer import Customer
                cobj = Customer(username, password, name, age, city, account_number)
                cobj.createuser()
                bobj = Bank(username, account_number)
                bobj.create_transaction_table()
                messagebox.showinfo("Success", f"Account created successfully!\nYour account number is: {account_number}")
                account_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        submit_btn = ctk.CTkButton(account_window, text="Create Account", command=submit)
        submit_btn.pack(pady=20)
    
    def login(self):
        login_window = ctk.CTkToplevel(self.window)
        login_window.title("Login")
        login_window.geometry("400x300")
        
        ctk.CTkLabel(login_window, text="Login to Your Account", font=("Arial", 20)).pack(pady=20)
        
        username_entry = ctk.CTkEntry(login_window, placeholder_text="Username")
        username_entry.pack(pady=10)
        
        password_entry = ctk.CTkEntry(login_window, placeholder_text="Password", show="*")
        password_entry.pack(pady=10)
        
        def verify():
            username = username_entry.get()
            password = password_entry.get()
            
            temp = db_query(f"SELECT password FROM customers where username = '{username}';")
            if temp and temp[0][0] == password:
                self.current_user = username
                account_data = db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")
                self.account_number = account_data[0][0]
                login_window.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        
        login_btn = ctk.CTkButton(login_window, text="Login", command=verify)
        login_btn.pack(pady=20)
    
    def show_dashboard(self):
        self.clear_window()
        
        dashboard_frame = ctk.CTkFrame(self.window)
        dashboard_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        welcome_text = f"Welcome {self.current_user.capitalize()}"
        ctk.CTkLabel(dashboard_frame, text=welcome_text, font=("Arial", 24)).pack(pady=20)
        
        # Add account number display
        account_text = f"Account Number: {self.account_number}"
        ctk.CTkLabel(dashboard_frame, text=account_text, font=("Arial", 16)).pack(pady=5)
        
        # Balance display
        def update_balance_label():
            bobj = Bank(self.current_user, self.account_number)
            temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.current_user}';")
            balance_label.configure(text=f"Current Balance: ₹{temp[0][0]}")
        
        balance_label = ctk.CTkLabel(dashboard_frame, text="", font=("Arial", 18))
        balance_label.pack(pady=10)
        update_balance_label()
        
        # Deposit function
        def show_deposit():
            deposit_window = ctk.CTkToplevel(self.window)
            deposit_window.title("Deposit Money")
            deposit_window.geometry("300x200")
            
            amount_entry = ctk.CTkEntry(deposit_window, placeholder_text="Enter Amount")
            amount_entry.pack(pady=20)
            
            def process_deposit():
                try:
                    amount = int(amount_entry.get())
                    if amount <= 0:
                        messagebox.showerror("Error", "Please enter a positive amount")
                        return
                        
                    bobj = Bank(self.current_user, self.account_number)
                    if bobj.deposit(amount):
                        update_balance_label()
                        deposit_window.destroy()
                        messagebox.showinfo("Success", f"Successfully deposited ₹{amount}")
                    else:
                        messagebox.showerror("Error", "Failed to deposit amount")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount")
            
            ctk.CTkButton(deposit_window, text="Deposit", command=process_deposit).pack(pady=10)
        
        # Withdraw function
        def show_withdraw():
            withdraw_window = ctk.CTkToplevel(self.window)
            withdraw_window.title("Withdraw Money")
            withdraw_window.geometry("300x200")
            
            amount_entry = ctk.CTkEntry(withdraw_window, placeholder_text="Enter Amount")
            amount_entry.pack(pady=20)
            
            def process_withdraw():
                try:
                    amount = int(amount_entry.get())
                    bobj = Bank(self.current_user, self.account_number)
                    bobj.withdraw(amount)
                    update_balance_label()
                    withdraw_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount")
            
            ctk.CTkButton(withdraw_window, text="Withdraw", command=process_withdraw).pack(pady=10)
        
        # Transfer function
        def show_transfer():
            transfer_window = ctk.CTkToplevel(self.window)
            transfer_window.title("Transfer Money")
            transfer_window.geometry("300x300")
            
            receiver_entry = ctk.CTkEntry(transfer_window, placeholder_text="Receiver Account Number")
            receiver_entry.pack(pady=20)
            
            amount_entry = ctk.CTkEntry(transfer_window, placeholder_text="Enter Amount")
            amount_entry.pack(pady=20)
            
            def process_transfer():
                try:
                    receiver = int(receiver_entry.get())
                    amount = int(amount_entry.get())
                    
                    if amount <= 0:
                        messagebox.showerror("Error", "Please enter a positive amount")
                        return
                        
                    if receiver == self.account_number:
                        messagebox.showerror("Error", "Cannot transfer to your own account")
                        return
                        
                    bobj = Bank(self.current_user, self.account_number)
                    if bobj.fundtransfer(receiver, amount):
                        update_balance_label()
                        transfer_window.destroy()
                        messagebox.showinfo("Success", f"Successfully transferred ₹{amount} to account {receiver}")
                    else:
                        messagebox.showerror("Error", "Transfer failed. Please check account number and balance.")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid details")
            
            ctk.CTkButton(transfer_window, text="Transfer", command=process_transfer).pack(pady=10)

        # Dashboard buttons
        ctk.CTkButton(dashboard_frame, text="Deposit", command=show_deposit).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Withdraw", command=show_withdraw).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Transfer", command=show_transfer).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Logout", command=self.show_main_screen).pack(pady=10)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = BankApp()
    app.run()
