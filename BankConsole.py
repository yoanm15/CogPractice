from datetime import date


class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password


class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount
        self.date = date.today()


class Account:
    def __init__(self, account_id, user_id, account_type):
        self.account_id = account_id
        self.user_id = user_id
        self.account_type = account_type
        self.balance = 0
        self.transactions = []

    def deposit(self, amount, txn_id):
        if amount <= 0:
            print("Deposit amount must be positive")
            return False
        self.balance += amount
        self.transactions.append(Transaction(txn_id, self.account_id, "DEPOSIT", amount))
        return True

    def withdraw(self, amount, txn_id):
        if amount <= 0:
            print("Withdraw amount must be positive")
            return False
        if amount > self.balance:
            print("Insufficient balance")
            return False
        self.balance -= amount
        self.transactions.append(Transaction(txn_id, self.account_id, "WITHDRAW", amount))
        return True


class Bank:
    def __init__(self):
        self.users = {
            "admin": User(1, "admin", "admin@bank.com", "admin123"),
            "user1": User(2, "user1", "user1@bank.com", "pass1"),
            "user2": User(3, "user2", "user2@bank.com", "pass2"),
        }
        self.accounts = {}
        self.next_account_id = 1
        self.next_txn_id = 1

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def create_account(self, user_id, account_type):
        account = Account(self.next_account_id, user_id, account_type)
        self.accounts[account.account_id] = account
        self.next_account_id += 1
        return account

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        if not account:
            print("Account not found")
            return False
        success = account.deposit(amount, self.next_txn_id)
        if success:
            self.next_txn_id += 1
        return success

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        if not account:
            print("Account not found")
            return False
        success = account.withdraw(amount, self.next_txn_id)
        if success:
            self.next_txn_id += 1
        return success

    def get_transactions(self, account_id):
        account = self.get_account(account_id)
        if not account:
            print("Account not found")
            return []
        return account.transactions


def login_prompt(bank):
    print("Please enter username and password separated by space")
    username, password = input().split(" ")
    user = bank.login(username, password)
    if user:
        print(f"Login successful. Welcome {user.name}")
    else:
        print("Invalid username or password")
    return user


def create_account_prompt(bank, user):
    account_type = input("Enter account type (SAVINGS/CHECKING): ")
    account = bank.create_account(user.user_id, account_type)
    print(f"Account created. Account ID: {account.account_id}")


def view_account_prompt(bank):
    account_id = int(input("Enter account ID: "))
    account = bank.get_account(account_id)
    if account:
        print(f"Account ID: {account.account_id}")
        print(f"Account Type: {account.account_type}")
        print(f"Balance: {account.balance}")
    else:
        print("Account not found")


def deposit_prompt(bank):
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter deposit amount: "))
    if bank.deposit(account_id, amount):
        print("Deposit successful")


def withdraw_prompt(bank):
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter withdraw amount: "))
    if bank.withdraw(account_id, amount):
        print("Withdraw successful")


def view_transactions_prompt(bank):
    account_id = int(input("Enter account ID: "))
    transactions = bank.get_transactions(account_id)
    if not transactions:
        print("No transactions found")
        return
    for txn in transactions:
        print(f"{txn.txn_id} | {txn.txn_type} | {txn.amount} | {txn.date}")


def print_menu():
    print()
    print("1. Create account")
    print("2. View account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. View transactions")
    print("6. Exit")


def main():
    bank = Bank()
    print("Welcome to our bank")

    user = None
    while user is None:
        user = login_prompt(bank)

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            create_account_prompt(bank, user)
        elif choice == "2":
            view_account_prompt(bank)
        elif choice == "3":
            deposit_prompt(bank)
        elif choice == "4":
            withdraw_prompt(bank)
        elif choice == "5":
            view_transactions_prompt(bank)
        elif choice == "6":
            print("Goodbye")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
