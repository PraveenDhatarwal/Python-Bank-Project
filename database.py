#Database Management Banking
import mysql.connector as sql

def get_db_connection():
    return sql.connect(
        host="localhost",
        user="root",
        passwd="9876543210",
        database="bank",
        autocommit=True  # Enable autocommit
    )

mydb = get_db_connection()
cursor = mydb.cursor(buffered=True)  # Use buffered cursor

def db_query(query, commit=False):
    try:
        cursor.execute(query)
        if commit:
            mydb.commit()
        if query.lower().startswith('select'):
            result = cursor.fetchall()
            if not result:  # If no results found
                return []   # Return empty list instead of None
            return result
        return True  # For non-SELECT queries
    except sql.Error as err:
        print(f"Database error: {err}")
        if commit:
            mydb.rollback()
        return [] if query.lower().startswith('select') else False

def createcustomertable():
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers
            (username VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL,
            name varchar(20) NOT NULL,
            age INTEGER NOT NULL,
            city VARCHAR(20) NOT NULL,
            balance INTEGER NOT NULL,
            account_number INTEGER NOT NULL,
            status BOOLEAN NOT NULL)
        ''')
        mydb.commit()
    except sql.Error as err:
        print(f"Error creating table: {err}")
        mydb.rollback()

if __name__ == "__main__":
    createcustomertable()