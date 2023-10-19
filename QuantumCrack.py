"""
QuantumCrack
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
README: This program was not made using any kind of quantum techniques or technology.
These estimations are highly speculative...however it's still interesting to see its potential.

## Description ##
"Your password may be safe today, but what about tomorrow?"
QuantumCrack is a Python tool that evaluates the strength of your password! (using the Zxcvbn library)
The program will display the estimated time to crack by normal means, and quantum means
Note: The estimate of the quantum time to crack is based on the following formula...
Estimated Quantum time to crack =  crackTime / (2**40)

## Features ##
- Estimates the time it would take to crack a password based on various factors.
- This is a more secure alternative to checking a passwords strength on a website!!!
- Provides an estimated time to crack by standard means
- Provides an estimated time to crack by quantum means

## How to Use ##
1. Run the script.
2. Enter your password when prompted.
3. Perform self OP-SEC evaluation...
* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

import tkinter as tk
import zxcvbn

class QuantumCrack:
    def __init__(self, password):
        self.password = password

    def format_time(self, seconds):
        intervals = [
            ('century', 60 * 60 * 24 * 365 * 100),
            ('year', 60 * 60 * 24 * 365),
            ('month', 60 * 60 * 24 * 30),
            ('week', 60 * 60 * 24 * 7),
            ('day', 60 * 60 * 24),
            ('hour', 60 * 60),
            ('minute', 60),
            ('second', 1)
        ]

        result = []
        for name, count in intervals:
            value = seconds // count
            if value > 0:
                result.append(f"{value} {name}{'s' if value > 1 else ''}")
            seconds %= count

        return ', '.join(result)

    def time_to_crack(self):
        result = zxcvbn.zxcvbn(self.password)
        crack_time_seconds = result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']
        return crack_time_seconds

    def estimate_quantum_time(self, classical_time, quantum_time):
        return classical_time / (2 ** quantum_time)

class QuantumCrackApp:
    def __init__(self, master):
        self.master = master
        master.title("QuantumCrack Password Evaluator")

        # Entry field for the password
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=10)

        # Button to trigger password strength check
        check_button = tk.Button(master, text="Check", command=self.check_password_strength)
        check_button.pack(pady=10)

        # Textbox to display password strength results
        self.strength_textbox = tk.Text(master, height=5, width=50)
        self.strength_textbox.pack(pady=10)

    def check_password_strength(self):
        # Get the password from the entry field
        user_password = self.password_entry.get()

        try:
            if not user_password:
                self.strength_textbox.delete(1.0, tk.END)
                self.strength_textbox.insert(tk.END, "Error: Please enter a password.")
                return

            quantum_crack = QuantumCrack(user_password)

            # Estimate the time to crack the password classically
            classical_crack_time = quantum_crack.time_to_crack()

            if classical_crack_time < 1:
                classical_strength_result = "Estimated Classical Time to Crack: Immediately"
            else:
                classical_strength_result = f"Estimated Classical Time to Crack:\n {quantum_crack.format_time(classical_crack_time)}"

            # Assume a hypothetical quantum speedup, for example, 40 (this is highly speculative)
            quantum_factor_of_40 = 40

            # Estimate the time to crack the password quantumly
            quantum_crack_time = quantum_crack.estimate_quantum_time(classical_crack_time, quantum_factor_of_40)

            # Build the results string
            results = classical_strength_result + "\n"

            if quantum_crack_time > 1:  # Adjust the threshold as needed
                results += f"Estimated Quantum Time to Crack:\n {quantum_crack.format_time(quantum_crack_time)}"
            else:
                results += "\nEstimated Quantum Time to Crack: Immediately"

            # Display the results in the text box
            self.strength_textbox.delete(1.0, tk.END)
            self.strength_textbox.insert(tk.END, results)

        except Exception as e:
            self.strength_textbox.delete(1.0, tk.END)
            self.strength_textbox.insert(tk.END, f"Error: {e}")

# Create and run the Tkinter app
root = tk.Tk()
app = QuantumCrackApp(root)
root.mainloop()
