import mysql.connector
from datetime import datetime
import hashlib


class TransactionSystem:
    def __init__(self):
        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pass#2710",     
            database="TRANSACTIONS"
        )
        self.cur = self.conn.cursor()

       
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tr_details(
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100),
                UPI_ID VARCHAR(100),
                AMT DECIMAL(10,2),
                Date DATETIME,
                Status VARCHAR(50)
            )
        """)
        self.conn.commit()

       
        self.__upi_data = {}   

   
    def enter_details(self):
        name = input("Enter your Name: ")
        upi = input("Enter your UPI ID: ")

        
        if upi not in self.__upi_data:
            pin = input("Set your UPI PIN: ")
            hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
            self.__upi_data[upi] = [name, hashed_pin]
            print("UPI ID Registered Successfully!\n")

        amt = float(input("Enter Amount: "))
        date = datetime.now()
        status = "Pending"

       
        self.cur.execute("""
            INSERT INTO tr_details (Name, UPI_ID, AMT, Date, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, upi, amt, date, status))
        self.conn.commit()
        print("Transaction is Pending.\n")

        
        proceed = input("Do you want to proceed to pay now? (y/n): ").lower()
        if proceed == "y":
            self.make_payment(upi, amt, name)
        else:
            print("You may pay later.\n")

   
    def make_payment(self, upi=None, amt=None, name=None):
        if not upi:
            upi = input("Enter your UPI ID: ")
        if not amt:
            amt = float(input("Enter Amount: "))
        if not name:
            name = input("Enter your Name: ")
        date = datetime.now()

        
        if self.verify_password(upi):
            print("PIN Verified. Payment Successful!\n")
            status = "Success"
        else:
            print("Wrong PIN. Payment Failed!\n")
            status = "Failed"

        
        self.cur.execute("""
            INSERT INTO tr_details (Name, UPI_ID, AMT, Date, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, upi, amt, date, status))
        self.conn.commit()

    
    def view_transactions(self,):
        upi = input("Enter your UPI ID to view transactions: ")
        if upi not in self.__upi_data:
            print("UPI not registered. Please register first.\n")
            return

        if not self.__verify_password(upi):
            print("PIN verification failed. Cannot view transactions.\n")
            return

    
        self.__cur.execute("SELECT * FROM tr_details WHERE UPI_ID = %s", (upi,))
        data = self.__cur.fetchall()

        if not data:
            print("\nNo transactions found for this UPI.\n")
        else:
            print(f"\n------ TRANSACTIONS HISTORY for {upi} ------")
            for row in data:
                print(f"ID: {row[0]} | Name: {row[1]} | UPI: {row[2]} | Amount: {row[3]} | Date: {row[4]} | Status: {row[5]}")
            print("------------------------------------\n")


    def verify_password(self, upi):
    
        if upi not in self.__upi_data:
            print("UPI not registered.")
            return False

        pin = input("Enter your UPI PIN: ")
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        return hashed_pin == self.__upi_data[upi][1]



def main():
    ts = TransactionSystem()

    while True:
        print("------ TRANSACTION ------")
        print("1. Enter Details")
        print("2. Make Payment")
        print("3. View Transactions History")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            ts.enter_details()
        elif choice == "2":
            ts.make_payment()
        elif choice == "3":
            ts.view_transactions()
        elif choice == "4":
            print("Exiting Program...")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
