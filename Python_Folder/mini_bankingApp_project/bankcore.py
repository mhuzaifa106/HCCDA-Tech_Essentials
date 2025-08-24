# # banking_app/bankcore.py

# # Branch ID fixed
# branch_id = 2057  

# # Storage for users {customer_id: {"name": str, "password": str}}
# users_info = {}  

# # Counter to generate unique user numbers
# user_number = 0  


# def create_account(name, password):
#     """
#     Create a new customer account.
#     Format: customer_id = <branch_id>-<user_number>
#     """
#     global user_number
#     user_number += 1
#     customer_id = f"{branch_id}-{user_number}"
#     users_info[customer_id] = {"name": name, "password": password}

#     print("\nAccount created successfully!")
#     print(f"Your Customer ID: {customer_id}")
#     return customer_id


# def login(customer_id, password):
#     """
#     Validate login credentials.
#     """
#     if customer_id in users_info and users_info[customer_id]["password"] == password:
#         print(f"\nLogin successful! Welcome, {users_info[customer_id]['name']}.")
#         return True
#     else:
#         print("\nInvalid login. Please try again.")
#         return False



























# bankcore.py

users_info = {}  # {cust_id: {"name": str, "user_id": str, "password": str}}

branch_id = "BR257"
user_number = 1  # increment for each account created


def create_account(name, user_id, psd):
    """Creates a new bank account and returns customer ID"""
    global user_number
    cust_id = f"{branch_id}_{user_number}"
    users_info[cust_id] = {
        "name": name,
        "user_id": user_id,
        "password": psd
    }
    user_number += 1
    print(f"\nAccount created successfully! Your Customer ID is: {cust_id}")
    return cust_id


def login(cust_id, psd):
    """Validates login credentials"""
    if cust_id in users_info and users_info[cust_id]["password"] == psd:
        print(f"\nWelcome back, {users_info[cust_id]['name']}!")
        return True
    else:
        print("\nInvalid Customer ID or Password!")
        return False
