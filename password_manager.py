import hashlib
from cryptography.fernet import Fernet
import os.path

KEY_FILE = "encryption_key.txt"
PASSWORD_FILE = "password_set.txt"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as file:
        file.write(key)

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            return file.read()
    else:
        generate_key()
        return load_key()

def encrypt_password(password):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(key, encrypted_password):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password)
    return decrypted_password.decode()

def save_password(url, username, password):
    encrypted_password = encrypt_password(password)
    with open('passwords.txt', 'a') as file:
        file.write("{\n")
        file.write(f"url=\"{url}\"\n")
        file.write(f"username=\"{username}\"\n")
        file.write(f"password=\"{encrypted_password.decode()}\"\n")
        file.write("}\n")
        file.write("\n")

def load_password(key):
    passwords = []
    with open('passwords.txt', 'r') as file:
        data = file.read().split("{\n")
        for item in data[1:]:
            item_data = item.strip().split("\n")
            url = item_data[0].split("\"")[1]
            username = item_data[1].split("\"")[1]
            encrypted_password = item_data[2].split("\"")[1]
            passwords.append((url, username, encrypted_password))
    return passwords

def set_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, 'w') as file:
        file.write(hashed_password)

def check_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, 'r') as file:
        stored_password = file.read().strip()
    return hashed_password == stored_password

def ask_password():
    while True:
        password = input("Set the password: ")
        confirm_password = input("Confirm the password: ")
        if password == confirm_password:
            set_password(password)
            print("Password set successfully!")
            break
        else:
            print("Passwords do not match. Please try again.")

def main():
    if not os.path.exists(PASSWORD_FILE):
        ask_password()
    else:
        while True:
            password = input("Enter the password: ")
            if check_password(password):
                break
            else:
                print("Invalid password. Please try again.")

    while True:
        print("Options:")
        print("1. Save password")
        print("2. Load password")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            url = input("Enter URL: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            save_password(url, username, password)
            print("Password saved successfully!")

        elif choice == '2':
            key = input("Enter encryption key: ")
            passwords = load_password(key.encode())
            if passwords:
                print("Saved passwords:")
                for i, (url, username, encrypted_password) in enumerate(passwords, start=1):
                    print(f"{i}. URL: {url}, Username: {username}")
                index = int(input("Enter the index of the password to decrypt: ")) - 1
                if index >= 0 and index < len(passwords):
                    _, _, encrypted_password = passwords[index]
                    decrypted_password = decrypt_password(key.encode(), encrypted_password.encode())
                    print(f"Decrypted password: {decrypted_password}")
                else:
                    print("Invalid index!")
            else:
                print("No passwords found!")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
