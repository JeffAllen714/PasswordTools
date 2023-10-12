"""
DictionarySafe
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
README: This was tested on MACOS and has not been verified to work on windows!!!

## Description ##
DictionarySafe is a simple yet powerful Python application that generates secure passwords...
using a unique method based on the Fibonacci sequence. The application utilizes Tkinter for the GUI.
Ment to work locally and have minimal modules for extra privacy and secure passwords.

### Features ###
- Generate strong and pseudo-random passwords using the Fibonacci sequence.
- Utilizes a local dictionary file for word selection.
- Ensures a mix of uppercase, lowercase, digits, and special characters in generated passwords.

## How to Use ##
1. Run the script.
2. Click the "Generate Password" button to generate a new secure password.
3. Optionally click the "Copy Password" button to copy the generated password to the clipboard
* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""


import tkinter as tk
import time


def fibonacci_pseudo_random(seed=None):
    # Use the current time as a seed if none is provided
    if seed is None:
        seed = int(time.time() * 1000)

    # Initialize the Fibonacci sequence
    fib = [0, 1]

    # Generate the next Fibonacci numbers
    for _ in range(100):  # You can adjust the range as needed
        fib.append(fib[-1] + fib[-2])

    # Use the seed to get a pseudo-random index
    index = seed % len(fib)

    return fib[index]


def fibonacci_choice(items, seed=None):
    random_index = fibonacci_pseudo_random(seed) % len(items)
    return items[random_index]


class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")

        # Button to generate password
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=20)

        # Button to copy the generated password to the clipboard
        self.copy_button = tk.Button(master, text="Copy Password", command=self.copy2Clipboard)
        self.copy_button.pack(pady=10)
        self.copy_button.pack_forget()  # Hide the button initially

        # Label to display generated password
        self.password_label = tk.Label(master, text="Generated Password will appear here.")
        self.password_label.pack(pady=10)

    def generate_password(self):
        # Define characters for digits and punctuation
        digits = "0123456789"
        punctuation = "!#$%&()*+,-./:;<=>?@[\]^_`{|}~"

        # Read words from the local dictionary file
        dictionary_words = set(line.strip() for line in open("/usr/share/dict/words"))

        # Use the Fibonacci-based logic to select words pseudo-randomly
        selected_words = [fibonacci_choice(list(dictionary_words)) for _ in range(3)]

        # Capitalize each selected word
        selected_words = [word.capitalize() for word in selected_words]

        # Concatenate the selected words without spaces
        password = ''.join(selected_words)

        # Ensure the password is at least 16 characters in length
        while len(password) < 16:
            new_word = fibonacci_choice(list(dictionary_words)).capitalize()
            password += new_word

        # Limit the password to a maximum of 24 characters
        password = password[:24]

        # Add a random digit
        password += fibonacci_choice(list(digits))

        # Add a random special character
        password += fibonacci_choice(list(punctuation))

        # Display the generated password
        self.password_label.config(text=f"Generated Password: {password}")

        # Show the "Copy Password" button
        self.copy_button.pack()

    def copy2Clipboard(self):
        # Get the generated password
        generated_password = self.password_label.cget("text")[20:]

        # Copy the password to the clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(generated_password)
        self.master.update()

        # Change button text immediately
        self.copy_button.config(text="Password Copied!")

        # After a delay, reset the button text
        self.master.after(2000, lambda: self.copy_button.config(text="Copy Password"))

    def reset_copy_button_text(self):
        self.copy_button.config(text="Copy Password")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
