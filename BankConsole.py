USERS = {
    "admin": "admin123",
    "user2": "pass2",
    "user1": "pass1",
}


def print_message(message):
    print(message)


def login():
    print("Please enter username and password separated by space")
    username, password = input().split(" ")
    if username in USERS and USERS[username] == password:
        print("Login successful")
        return username
    else:
        print("Invalid username or password")
        return None


def main():
    print_message("Welcome to our bank")
    username = login()
    print_message(f"Welcome {username}")


if __name__ == "__main__":
    main()
