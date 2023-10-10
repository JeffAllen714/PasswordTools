"""
lyricSafe
GitHub: [JeffAllen714](https://github.com/JeffAllen714)

* * * * * * * * * * * * * * * * * * * * * * * * * * * *

## Description ##
lyricSafe is a password generator application that produces secure passwords, based on song lyrics!

## Features ##

- Generate strong and secure passwords, with lyrics!
- Built in WebScraper to pull lyrics right from websites like Genius.com, Lyrics.com, etc.
- The WebScraper pulls the info into a CSV file, but you're welcome to use your own CSV file instead.
- Each password is tested for resilience against brute force attacks. (Tested with zxcvbn library)
- GUI Application with a built in Web Scraper and Password Generator.
- Easily copy the generated password to you clipboard.

## How to Use ##

1. Run the script. (A GUI will pop up)
2. Provide a website to be scraped. (Optional)
3. Provide a CSV file. (If you scraped a website, then the CSV will be provided for you)
4. Receive a randomly generated secure password based from song lyrics!

* * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

import csv
import random
import string
import zxcvbn
import requests
import tkinter as tk
from bs4 import BeautifulSoup


def generatePassword(lyrics):
    # Generates the new password for the user and ensures a high level of security
    # Check if lyrics are not empty...
    if not lyrics:
        return None

    # Concatenate all lyrics into a single string
    lyricsText = ' '.join(lyrics)

    # Create a list of randomized words from the lyrics
    randomWords = random.sample(lyricsText.split(), 3)

    # Capitalize the first letter of each word
    newPassword = ' '.join(word.capitalize() for word in randomWords)

    # Limit the newPassword to a maximum of 24 characters
    newPassword = newPassword[:24]

    # Add a random digit
    newPassword += random.choice(string.digits)

    # Add a random special character
    newPassword += random.choice(string.punctuation)

    result = zxcvbn.zxcvbn(newPassword)
    if result['score'] == 4: # very unguessable: strong protection from offline slow-hash scenario. (guesses >= 10^10)
        return newPassword
    else:
        return None


def look4DictWords(lyrics):
    # Checks to see if any of the words in the CSV file are dictionary words or "Human-Readable"
    dictionaryWords = set(line.strip() for line in open("/usr/share/dict/words"))
    return any(word.lower() in dictionaryWords for word in lyrics.split())


class LyricSafe:
    """
    ## Class Description ##
    LyricSafe class represents a password generator application that produces secure passwords based on song lyrics.

    Attributes:
        lyrics_file (str): The path to the CSV file containing song titles and lyrics.
        default_file_path (str): The default file path used when a specific path is not provided.
        generated_password (str): The generated password based on song lyrics.

    Methods:
        readLyrics(): Reads and extracts lyrics from the CSV file.
        getPassword(): Generates a secure password based on song lyrics and dictionary words.
        gatherPassword(): Gathers a secure password based on song lyrics and dictionary words.
        readGameTitles(): Reads and extracts game titles from the CSV file.
    """
    def __init__(self, lyrics_file, default_file_path):
        self.lyrics_file = lyrics_file if lyrics_file else default_file_path
        self.generated_password = ""

    def readLyrics(self):
        try:
            with open(self.lyrics_file, 'r') as csv_file:
                reader = csv.reader(csv_file)
                # TODO: logic to correctly extract both title and lyrics
                #  Consider changing the names to be more universal (Columns, Rows)
                data = list(reader)
                titles = [row[0] for row in data]
                lyrics = [row[1] for row in data]
                return ' '.join(lyrics)
        except Exception as e:
            print(f'An error occurred while reading lyrics from CSV: {e}')
            return None

    def getPassword(self):
        game_titles = self.readGameTitles()

        if game_titles and look4DictWords(' '.join(game_titles)):
            generated_password = generatePassword(game_titles)
            while generated_password is None:
                generated_password = generatePassword(game_titles)

            self.generated_password = generated_password
            return self.generated_password
        else:
            print("Warning: The CSV file doesn't contain any 'human-readable' content. Do you want to continue?")
            # You might want to handle the user's choice here
            return None

    def gatherPassword(self):
        game_titles = self.readGameTitles()

        if game_titles and look4DictWords(' '.join(game_titles)):
            generated_password = generatePassword(game_titles)
            while generated_password is None:
                generated_password = generatePassword(game_titles)

            self.generated_password = generated_password
            return self.generated_password
        else:
            print("Error: The CSV file doesn't contain any 'human-readable' content.")
            # You might want to handle the user's choice here
            return None

    def readGameTitles(self):
        # TODO: This is a hack to run a test CSV file that I had (Its a list of best selling video games)...
        #  ...The theme for this program is lyrics, but i would like to be able to do this with any CSV...
        #  RENAME AND MAKE THE LOGIC UNIVERSAL
        try:
            with open(self.lyrics_file, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                game_titles = [row['Name'] for row in reader]
                return game_titles
        except Exception as e:
            print(f'An error occurred while reading game titles from CSV: {e}')


# # GUI # #
class PasswordGeneratorApp:
    """
    ## Class Description ##
    NOTE: This class is supplementary to the lyricSafe class
    PasswordGeneratorApp class represents the GUI application for the LyricSafe password generator.

    Attributes:
        master: The main Tkinter window.
        lyric_safe: An instance of the LyricSafe class.

    Methods:
        scrape_website(): Triggers web scraping based on the provided URL.
        generate_password(): Generates a password based on the provided URL or CSV file path.
        copy2Clipboard(): Copies the generated password to the clipboard.
        reset_copy_button_text(): Resets the copy button text after a delay.
    """
    def __init__(self, master):
        self.master = master
        master.title("lyricSafe Password Generator")

        default_csv_path = ''  # Empty default CSV file path
        self.lyric_safe = LyricSafe('', default_csv_path)

        # Label for URL entry
        url_label = tk.Label(master, text="Enter the URL to scrape:")
        url_label.pack(pady=5)

        # Entry field for the URL
        self.url_entry = tk.Entry(master)
        self.url_entry.pack(pady=10)

        # Label for CSV file path entry
        csv_path_label = tk.Label(master, text="Enter the CSV file path:")
        csv_path_label.pack(pady=5)

        # Entry field for the CSV file path
        self.csv_path_entry = tk.Entry(master)
        self.csv_path_entry.insert(0, default_csv_path)  # Default CSV file path
        self.csv_path_entry.pack(pady=10)

        # Button to trigger scraping
        scrape_button = tk.Button(master, text="Scrape", command=self.scrape_website)
        scrape_button.pack(pady=10)

        # Button to copy the generated password to the clipboard
        self.copy_button = tk.Button(master, text="Copy Password", command=self.copy2Clipboard)
        self.copy_button.pack(pady=10)
        self.copy_button.pack_forget()  # Hide the button initially

        # Button to generate password
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=20)

        # Label to display generated password
        self.password_label = tk.Label(master, text="Generated Password will appear here.")
        self.password_label.pack(pady=10)

    def scrape_website(self):
        # Get the URL from the entry field
        URL = self.url_entry.get()

        try:
            if not URL:
                self.password_label.config(text="Error: Please enter a valid URL.")
                return

            # Try scraping the provided URL
            RESPONSE = requests.get(URL)
            if RESPONSE.status_code == 200:
                # Extract the relevant part of the URL for the CSV file name
                csv_filename = URL.split('/')[-1].replace('-', '_') + '.csv'
                csv_filepath = csv_filename
                soup = BeautifulSoup(RESPONSE.text, 'html.parser')
                songTitles = [title.text for title in soup.select('.header_with_cover_art-primary_info-title')]
                songLyrics = [lyrics.text for lyrics in soup.select('.lyrics')]
                data = list(zip(songTitles, songLyrics))
                with open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(['Title', 'Lyrics'])
                    csv_writer.writerows(data)

                # Update the CSV file entry with the generated filename
                self.csv_path_entry.delete(0, tk.END)
                self.csv_path_entry.insert(0, csv_filename)

                # Clear any previous error messages
                self.password_label.config(text="")
            else:
                print('Failed to retrieve the webpage. Status code:', RESPONSE.status_code)
        except requests.exceptions.MissingSchema:
            suggested_url = f"https://{URL}"
            self.password_label.config(text=f"Error: You must provide the whole URL. Did you mean \"{suggested_url}\"?")
        except Exception as e:
            print(f"Error: {e}")

    def generate_password(self):
        # Get the URL and CSV file path from the entry fields
        url = self.url_entry.get()
        csv_path = self.csv_path_entry.get()

        try:
            if url:
                # Use the generated CSV file path
                self.lyric_safe = LyricSafe(url, url)
            else:
                # Use the provided CSV file path
                self.lyric_safe = LyricSafe(csv_path, csv_path)

            # Check if the CSV file exists and is not empty
            if not self.lyric_safe.readGameTitles():
                self.password_label.config(text="Error: CSV file is empty or does not exist.")
                return

            generated_password = self.lyric_safe.gatherPassword()
            if generated_password:
                # Remove spaces from the generated password
                generated_password = generated_password.replace(' ', '')
                self.password_label.config(text=f"Generated Password: {generated_password}")

                # Show the "Copy Password" button
                self.copy_button.pack()

            else:
                self.password_label.config(text="Error: Unable to generate a password.")
        # Print the exception error and continue
        except Exception as e:
            self.password_label.config(text=f"Error: {e}")

    def copy2Clipboard(self):
        # Provides the user with a copy button to copy the password with ease.
        generated_password = self.password_label.cget("text")
        if generated_password.startswith("Generated Password: "):
            generated_password = generated_password[20:]

        self.master.clipboard_clear()
        self.master.clipboard_append(generated_password)
        self.master.update()

        # Change button text after a delay.
        self.copy_button.config(text="Password Copied!")
        self.master.after(2000, self.reset_copy_button_text)

    def reset_copy_button_text(self):
        self.copy_button.config(text="Copy Password")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
