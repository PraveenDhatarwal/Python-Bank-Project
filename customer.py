#Customer Details
from database import *
class Customer:

    def __init__(self, username, password, name, age, city, account_number):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = age
        self.__city = city
        self.__account_number = account_number

    def createuser(self):
        try:
            query = f"""INSERT INTO customers 
                VALUES ('{self.__username}', '{self.__password}', '{self.__name}', 
                '{self.__age}', '{self.__city}', 0, '{self.__account_number}', 1)"""
            db_query(query, commit=True)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False