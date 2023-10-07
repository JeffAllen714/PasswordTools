"""
CheckPasswordStrength
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *

## Description ##
CheckPasswordStrength is a Python tool that evaluates the strength of your password! (using the Zxcvbn library)

## Features ##

- Estimates the time it would take to crack a password based on various factors.
- This is a more secure alternative to checking a passwords strength on a website!!!
- Provides an estimated time to crack
- Gives the password a Score from 1-5
    1. Very Weak (Immediate - 6 days)
    2. Weak (1 week - 4 weeks)
    3. Strong (1 month - 11 months)
    4. Very Strong (Years)
    5. Extremely Strong (Centuries)

## How to Use ##

1. Run the script.
2. Enter your password when prompted.
3. Panic when you find out how weak your password is.

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

import zxcvbn


def time2Crack(password):
    result = zxcvbn.zxcvbn(password)
    crackTime = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    return crackTime


# Get user input
userPassword = input("Enter your password: ")

# Estimate the time to crack the password
crackTime = time2Crack(userPassword)

print(f"Estimated time to crack your password: {crackTime}")

# Assign scores based on crack time
if "centuries" in crackTime:
    score = 5
    print("Your password is EXTREMELY strong! It won't be cracked in your lifetime!")
elif "years" in crackTime:
    score = 4
    print("Your password is VERY strong. It won't be cracked for several years.")
elif "months" in crackTime:
    score = 3
    print("Your password is strong. You're good for at least a month")
elif "weeks" in crackTime:
    score = 2
    print("Your password is relatively weak. Consider strengthening.")
else:
    score = 1
    print("Your password is very weak. Change it immediately!")

print(f"Password Strength Score: {score}")
