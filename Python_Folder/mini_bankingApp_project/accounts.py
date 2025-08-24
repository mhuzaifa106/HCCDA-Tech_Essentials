# # banking_app/accounts.py

# balance_record = {}   # customer_id -> balance

# def check_balance(customer_id):
#     return balance_record.get(customer_id, 0)

# def deposit(customer_id, amount):
#     if customer_id not in balance_record:
#         balance_record[customer_id] = 0
#     balance_record[customer_id] += amount
#     print("\n", amount, "deposited successfully.")
#     print("New Balance:", balance_record[customer_id])
#     return balance_record[customer_id]

# def withdraw(customer_id, amount):
#     if customer_id not in balance_record:
#         balance_record[customer_id] = 0
#     if balance_record[customer_id] >= amount:
#         balance_record[customer_id] -= amount
#         print("\n", amount, "withdrawn successfully.")
#         print("New Balance:", balance_record[customer_id])
#     else:
#         print("\nInsufficient balance.")
#     return balance_record[customer_id]



























# accounts.py

balance_record = {}  # {cust_id: balance}


def check_balance(cust_id):
    """Displays the current balance for the customer"""
    balance = balance_record.get(cust_id, 0)
    print(f"\nYour current balance is: {balance}")
    return balance


def deposit(cust_id, amount):
    """Deposits money into the customer's account"""
    if amount <= 0:
        print("\nDeposit amount must be positive!")
        return
    balance_record[cust_id] = balance_record.get(cust_id, 0) + amount
    print(f"\nDeposited {amount}. New balance: {balance_record[cust_id]}")


def withdraw(cust_id, amount):
    """Withdraws money if sufficient funds are available"""
    if amount <= 0:
        print("\nWithdrawal amount must be positive!")
        return
    if balance_record.get(cust_id, 0) < amount:
        print("\nInsufficient funds!")
        return
    balance_record[cust_id] -= amount
    print(f"\nWithdrawn {amount}. New balance: {balance_record[cust_id]}")
