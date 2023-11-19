import sqlite3
import random
from datetime import datetime
import send_emails
import pandas

class Transactions:
    def __init__ (self, acc_no, database_name = "database.db"):
        self.acc_no = acc_no
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS transactions (acc_no INTEGER, acc_holder TEXT, operation TEXT, amount DECIMAL, date TEXT, curr_bal DECIMAL)")
        self.conn.commit()

    def record_transaction (self, acc_holder_name, operation, amount, bal):
        self.cur.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", (self.acc_no, 66, operation, amount, datetime.now().strftime("%Y-%m-%d %H-%M-%S"), bal))
        self.conn.commit()

    def view_transactions (self, email, send_trans_hist = False):
        self.cur.execute("SELECT * FROM transactions WHERE acc_no = ?", (self.acc_no, ))
        transactions = self.cur.fetchall()
        if transactions:
            if send_trans_hist:
                transactions_df = pandas.DataFrame(columns=["Account No.", "Action", "Amount", "Date", "Available Balance"])
                for trans in transactions:
                    transactions_df = transactions_df.append({"Account No.": trans[0], "Action": trans[2], "Amount": trans[3], "Date": trans[4], "Available Balance": trans[5]}, ignore_index=True)
                
                transactions_df.to_excel(f"Transactions_{self.acc_no}.xlsx")
                
                send_emails.send_email(email, f"Transactions details of account number {self.acc_no}", "The transaction details are attached with the mail",filename= f"Transactions_{self.acc_no}.xlsx")

                return ["Your Transaction history has been sent to Your Registered email", True]
            
            else:
                return transactions

        else: 
            return ["No trasaction Found", False]

    def __del__(self):
        self.conn.close()

class Accounts:
    def __init__(self, database_name = "database.db"):
        self.acc_no = 0
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS accounts (acc_no INTEGER, acc_holder TEXT, adhar_no INTEGER, address TEXT, email TEXT, curr_bal DECIMAL, password TEXT, mob_no INTEGER)")
        self.conn.commit()

        self.otp = random.randint(0,99999)
        self.otp_message = f"You have requested for new account opening . The OTP for email verification is {self.otp}"
        self.cur.execute("SELECT * FROM accounts")
        all_accounts = self.cur.fetchall()
        #print(all_accounts)
        
    
    def login(self, acc_no, password):
        account = self.get_account(acc_no)
        #print (account)
        if account[1]:
            if password == account[0][0][-2]:
                self.acc_no = acc_no
                return [account, True]
            else:
                account = "Wrong password"
                return [account, False]
        else:
            return account

    def create_account(self, acc_data):
        self.acc_data = acc_data

        #To check if aadhar no. already exists
        self.cur.execute("SELECT * FROM accounts")
        all_accounts = self.cur.fetchall()

        if all_accounts:
            #print(acc_data)
            adhar_no_list = []
            for account in all_accounts:
                adhar_no_list.append(int(account[2]))

            if acc_data["aadhar_no"] in adhar_no_list:
                return False
            else:
                send_emails.send_email(acc_data["email"], "Email varification OTP", self.otp_message)
                return "OTP sent on your email address"
        else:
            send_emails.send_email(acc_data["email"], "Email varification OTP", self.otp_message)
            return "OTP sent on your email address"
    
    def check_balance(self):
        account = self.get_account(self.acc_no)[0]
        acc_num = account[0][0]
        self.cur.execute("SELECT * FROM accounts")
        all_accounts = self.cur.fetchall()

        for accounts in all_accounts:
            if acc_num in accounts:
                return accounts[5]

    def withdraw(self, amount):
        account = self.get_account(self.acc_no)[0]
        if amount == "":
            return ["Enter amount first", False]
        try:
            amount = float(amount)
            curr_bal = account[0][5]
            if amount > curr_bal:
                return ["Insufficient Balance", False]
            else:
                curr_bal = curr_bal - amount

                self.cur.execute("UPDATE accounts SET curr_bal = ? WHERE acc_no = ?", (curr_bal, account[0][0]))
                self.conn.commit()

                trans = Transactions(account[0][0])
                trans.record_transaction(account[0][1], "Debited", amount, curr_bal)

                message = f"Dear Customer, Your a/c {account[0][0]} has been debited with {amount} on {trans.view_transactions(account[0][4])[-1][4]}. Avl balance: {curr_bal}"
                send_emails.send_email(account[0][4], "Amount Debited", message)

                return ["Successfully Withdrawed", True]
        except ValueError:
            return ["Amount must be digits", False]

    def deposite(self, amount):
        account = self.get_account(self.acc_no)[0]
        if amount == "":
            return ["Enter amount first", False]
        try: 
            amount = float(amount)
            if amount < 0:
                return ["Enter amount correctly", False]

            curr_bal = account[0][5]
            curr_bal = curr_bal + amount

            self.cur.execute("UPDATE accounts SET curr_bal = ? WHERE acc_no = ?", (curr_bal, account[0][0]))
            self.conn.commit()

            trans = Transactions(account[0][0])
            trans.record_transaction(account[0][1], "Credited", amount, curr_bal)

            message = f"Dear Customer, Your a/c {account[0][0]} has been credited with {amount} on {trans.view_transactions(account[0][4])[-1][4]}. Avl balance: {curr_bal}"
            send_emails.send_email(account[0][4], "Amount Credited", message)

            return ["Deposited Successfully",True]

        except ValueError:
            return ["Enter amount correctly", False]

    def verify_otp(self,entered_otp, acc_data):
        if self.otp == entered_otp:
            self.cur.execute("SELECT * FROM accounts")
            all_accounts = self.cur.fetchall()
            if all_accounts == []:
                acc_no = 10000000001
            else:
                acc_no = all_accounts[-1][0] + 1

            self.cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (acc_no, self.acc_data["name"], self.acc_data["aadhar_no"], self.acc_data["address"], self.acc_data["email"], 0.0, self.acc_data["password"], self.acc_data["mob_no"]))
            self.conn.commit()
            name = acc_data["name"]
            send_emails.send_email(acc_data["email"], "Account Created Successfully!!!", f"Congratulations {name}, your account has been created successfylly. Your account Number is {acc_no}")
            return True

        else:
            return False

    def get_account(self, acc_no):
        try:
            acc_no = int(acc_no)
            self.cur.execute("SELECT * FROM accounts")
            all_accounts = self.cur.fetchall()

            if all_accounts:
                acc_no_list = []

                for account in all_accounts:
                    acc_no_list.append(int(account[0]))

                print (acc_no_list)

                if acc_no in acc_no_list:
                    self.cur.execute("SELECT * FROM accounts WHERE acc_no = ?", (acc_no, ))
                    account = self.cur.fetchall()

                    return [account,True]
                else:
                    account = "Wrong Account Number"
                    return [account, False]
            else:
                account = "Wrong Account Number"
                return [account, False]

        except ValueError:
                account = "Enter account number Correctly"
                return [account,False]

    def __del__(self):
        self.conn.close()