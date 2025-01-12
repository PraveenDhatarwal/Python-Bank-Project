# Bank Services
from database import *
import datetime


class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    def create_transaction_table(self):
        try:
            query = f"""CREATE TABLE IF NOT EXISTS {self.__username}_transaction (
                timedate VARCHAR(30),
                account_number INTEGER,
                remarks VARCHAR(30),
                amount INTEGER
            )"""
            db_query(query, commit=True)
        except Exception as e:
            print(f"Error creating transaction table: {e}")

    def balanceequiry(self):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        print(f"{self.__username} Balance is {temp[0][0]}")

    def deposit(self, amount):
        try:
            temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
            if temp and len(temp) > 0:  # Check if result exists
                current_balance = temp[0][0]
                new_balance = current_balance + amount
                update_success = db_query(
                    f"UPDATE customers SET balance = {new_balance} WHERE username = '{self.__username}';", 
                    commit=True
                )
                
                if update_success:
                    # Add transaction record
                    transaction_success = db_query(
                        f"""INSERT INTO {self.__username}_transaction 
                        VALUES ('{datetime.datetime.now()}', '{self.__account_number}', 'Amount Deposit', '{amount}')""",
                        commit=True
                    )
                    
                    if transaction_success:
                        print(f"Successfully deposited {amount}")
                        return True
            
            print("Failed to deposit: Account not found or database error")
            return False
            
        except Exception as e:
            print(f"Error in deposit: {e}")
            return False

    def withdraw(self, amount):
        try:
            temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
            if temp and len(temp) > 0:  # Check if result exists
                current_balance = temp[0][0]
                if amount <= current_balance:
                    new_balance = current_balance - amount
                    update_success = db_query(
                        f"UPDATE customers SET balance = {new_balance} WHERE username = '{self.__username}';",
                        commit=True
                    )
                    
                    if update_success:
                        # Add transaction record
                        transaction_success = db_query(
                            f"""INSERT INTO {self.__username}_transaction 
                            VALUES ('{datetime.datetime.now()}', '{self.__account_number}', 'Amount Withdraw', '{amount}')""",
                            commit=True
                        )
                        
                        if transaction_success:
                            print(f"Successfully withdrew {amount}")
                            return True
                else:
                    print("Insufficient balance")
                    return False
            
            print("Failed to withdraw: Account not found or database error")
            return False
            
        except Exception as e:
            print(f"Error in withdrawal: {e}")
            return False

    def fundtransfer(self, receive, amount):
        try:
            # Verify receiver exists
            receiver_exists = db_query(f"SELECT username FROM customers WHERE account_number = {receive};")
            if not receiver_exists:
                print("Receiver account not found")
                return False

            # Get balances
            sender_balance = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
            if not sender_balance or sender_balance[0][0] < amount:
                print("Insufficient balance")
                return False

            # Update sender balance
            new_sender_balance = sender_balance[0][0] - amount
            sender_update = db_query(
                f"UPDATE customers SET balance = {new_sender_balance} WHERE username = '{self.__username}';",
                commit=True
            )

            # Update receiver balance
            receiver_update = db_query(
                f"UPDATE customers SET balance = balance + {amount} WHERE account_number = {receive};",
                commit=True
            )

            if sender_update and receiver_update:
                # Record transactions for both parties
                receiver_username = receiver_exists[0][0]
                
                # Sender transaction record
                db_query(
                    f"""INSERT INTO {self.__username}_transaction 
                    VALUES ('{datetime.datetime.now()}', {receive}, 'Transfer Sent', {amount})""",
                    commit=True
                )
                
                # Receiver transaction record
                db_query(
                    f"""INSERT INTO {receiver_username}_transaction 
                    VALUES ('{datetime.datetime.now()}', {self.__account_number}, 'Transfer Received', {amount})""",
                    commit=True
                )
                
                print(f"Successfully transferred {amount} to account {receive}")
                return True

            return False

        except Exception as e:
            print(f"Error in fund transfer: {e}")
            return False
