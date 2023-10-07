"""
SecurePasswordGen
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *

## Description ##
SecurePasswordGen (You Guessed It) generates a secure password for you!

## Features ##

- Generates a secure password. Includes Numbers, Letters and Special Characters.
- Currently set at 15 character length.
- A Timestamp is also printed along with the password for reference.

## How to Use ##

1. Run the script.
2. Recieve a randomly generated secure password!

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""


import datetime
import random
import string


class PasswordGenerator:
    """
    A class for generating random passwords and displaying the timestamp.

    Attributes:
    - length (int): The length of the generated password.
    - password (str): The generated random password.
    - timestamp (datetime): The date and time when the password was generated.

    Methods:
    - generate_password(): Generates a random password.
    - display_password(): Displays the generated password.
    - display_timestamp(): Displays the timestamp of when the password was generated.
    """

    def __init__(self, length=15):
        # Initializes a PasswordGenerator object.
        self.length = length
        self.password = self.generatePassword()
        self.timestamp = datetime.datetime.now()

    def generatePassword(self):
        # Generates a random password
        return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation)
                       for _ in range(self.length))

    def displayPassword(self):
        # Displays the generated password.
        print("Your new random password has been generated:")
        print(self.password)

    def displayTimestamp(self):
        print("Date and Time:", self.timestamp)


password_generator = PasswordGenerator(length=15)
password_generator.displayPassword()
password_generator.displayTimestamp()