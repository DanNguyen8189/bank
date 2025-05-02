#https://www.w3resource.com/python-exercises/oop/python-oop-exercise-11.php

import heapq 
class Bank:
    # Initialize the bank with an empty dictionary to store customer accounts and balances
    def __init__(self):
        self.customers = {}

    # Create a new account with a given account number and an optional initial balance (default to 0)
    def create_account(self, account_number, initial_balance, timestamp):
        #self.customers[account_number] = initial_balance
        bankAccount = BankAccount(account_number, initial_balance, timestamp)
        self.customers[account_number] = bankAccount

    # Make a deposit to the account with the given account number
    def make_deposit(self, account_number, amount, timestamp):
        return self.customers[account_number].deposit(amount, timestamp)

    # Make a withdrawal from the account with the given account number
    def make_withdrawal(self, account_number, amount, timestamp):
        return self.customers[account_number].withdraw(amount, timestamp)

    # Check and print the balance of the account with the given account number
    def check_balance(self, account_number):
        if account_number not in self.customers.keys():
            print("Account number does not exist")
            return
        return self.customers[account_number].check_balance()

    def top_accounts(self):
        accounts = []
        heapq.heapify(accounts)
        for account in self.customers.keys():
            customer = self.customers[account]
            heapq.heappush(accounts, (-1 * len(customer.transaction_history), customer.account_number))
        accounts_list = [item[1] for item in accounts]
        print(accounts)
        return accounts_list[:min(len(accounts_list), 10)]

    def merge_accounts(self, account_number0, account_number1, timestamp):
        account0 = self.customers[account_number0]
        account1 = self.customers[account_number1]
        account0_history = account0.transaction_history
        account1_history = account1.transaction_history
        new_transaction_history = []

        pointer0 = 0
        pointer1 = 0

        while pointer0 < len(account0_history) and pointer1 < len(account1_history):
            if account0_history[pointer0][3] < account1_history[pointer1][3]:
                new_transaction_history.append(account0_history[pointer0])
                pointer0 += 1
            else:
                new_transaction_history.append(account1_history[pointer1])
                pointer1 += 1

        if pointer0 < len(account0_history):
            new_transaction_history += account0_history[pointer0:]
        elif pointer1 < len(account1_history):
            new_transaction_history += account1_history[pointer1:]

        new_account_number = account0.account_number + account1.account_number
        new_account = BankAccount(
            new_account_number,
            account0.balance + account1.balance,
            timestamp
            )
        new_transaction_history.append(("Merge", 0, new_account.balance, timestamp))
        new_account.transaction_history = new_transaction_history
        self.customers[new_account_number] = new_account
        return new_transaction_history




class BankAccount:
    def __init__(self, account_number, initial_balance, timestamp):
        self.balance = initial_balance
        self.account_number = account_number
        self.transaction_history = [(("Create", initial_balance, initial_balance, timestamp))]

    def deposit(self, amount, timestamp):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(("Deposit", amount, self.balance, timestamp))
            #self.transaction_history.append(f"Deposited: +{amount}, Balance: {self.balance}")
            return True
        else:
            print("Invalid transcation: deposits must be greater then 0")
            return False

    def withdraw(self, amount, timestamp):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(("Withdrawal", -1*amount, self.balance, timestamp))
            #self.transaction_history.append(f"Withdrawn: -{amount}, Balance: {self.balance}")
            print("Withdrawal successful.")
            return True
        else:
            print("Insufficient funds or invalid amount.")
            return False

    def check_balance(self):
        return self.balance


# Example usage
# Create an instance of the Bank class
bank = Bank()

#transaction counter to keep track of order
timestamp = 0

# Create customer accounts and perform account operations
acno1= "SB-123"
damt1 = 1000
print("New a/c No.: ",acno1,"Deposit Amount:",damt1)
bank.create_account(acno1, damt1, timestamp)
print(bank.check_balance(acno1))
timestamp += 1

acno2= "SB-124"
damt2 = 1500
print("New a/c No.: ",acno2,"Deposit Amount:",damt2)
bank.create_account(acno2, damt2, timestamp)
timestamp += 1

wamt1 = 600
print("\nDeposit Rs.",wamt1,"to A/c No.",acno1)
bank.make_deposit(acno1, wamt1, timestamp)
timestamp += 1

print("\nDeposit Rs.",wamt1,"to A/c No.",acno2)
bank.make_deposit(acno2, wamt1, timestamp)
timestamp += 1

wamt2 = 350
print("Withdraw Rs.",wamt2,"From A/c No.",acno2)
bank.make_withdrawal(acno2, wamt2, timestamp)
timestamp += 1

print("A/c. No.",acno1)
bank.check_balance(acno1)

print("A/c. No.",acno2)
bank.check_balance(acno2)

wamt3 = 1200
print("Withdraw Rs.",wamt3,"From A/c No.",acno2)
bank.make_withdrawal(acno2, wamt3, timestamp)
timestamp += 1

acno3 = "SB-134"
print("A/c. No.",acno3)
bank.check_balance(acno3)  # Non-existent account number 

#print(bank.top_accounts())

print(bank.merge_accounts(acno1, acno2, timestamp))
timestamp += 1
