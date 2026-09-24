from tkinter import *
from tkinter import messagebox
import os
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
BG_COLOR = "#1a1a2e"
CARD_BG = "#16213e"
ACCENT = "#e94560"
ACCENT_HOVER = "#ff6b81"
TEXT_COLOR = "#eaeaea"
LABEL_COLOR = "#a0a0c0"
ENTRY_BG = "#0f3460"
ENTRY_FG = "#ffffff"
FONT_NAME = "Segoe UI"
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = username_entry.get()
    password = password_entry.get()

    new_data = {website:{"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you have not left any fields empty.")
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No data file found.')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No detail for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "logo.png")

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=30, bg=BG_COLOR)
window.resizable(False, False)

# Try to set a nice window icon / modern look
try:
    window.tk.call("tk", "scaling", 1.2)
except Exception:
    pass

# Main card frame
card = Frame(window, bg=CARD_BG, padx=30, pady=25)
card.grid(row=0, column=0)

# Logo
canvas = Canvas(card, width=200, height=200, bg=CARD_BG, highlightthickness=0)
logo_img = PhotoImage(file=logo_path)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 15))

# Title
title_label = Label(
    card,
    text="Password Manager",
    font=FONT_TITLE,
    fg=ACCENT,
    bg=CARD_BG
)
title_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

# Helper to create consistent styled labels
def make_label(text, row):
    lbl = Label(
        card,
        text=text,
        font=FONT_BOLD,
        fg=LABEL_COLOR,
        bg=CARD_BG,
        anchor="e"
    )
    lbl.grid(row=row, column=0, sticky="e", padx=(0, 12), pady=8)
    return lbl

# Helper to create consistent styled entries
def make_entry(width=32, row=None, column=1, columnspan=2):
    entry = Entry(
        card,
        width=width,
        font=FONT_NORMAL,
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#2a2a4a",
        highlightcolor=ACCENT
    )
    entry.grid(row=row, column=column, columnspan=columnspan, sticky="ew", pady=8, ipady=6)
    return entry

# Labels
make_label("Website:", 2)
make_label("Email / Username:", 3)
make_label("Password:", 4)

# Entries
website_entry = make_entry(width=21, row=2, column=1, columnspan=1)
website_entry.focus()

username_entry = make_entry(row=3)
username_entry.insert(0, "sourav@email.com")

password_entry = make_entry(width=21, row=4, column=1, columnspan=1)

# Styled buttons
def style_button(btn, primary=False):
    if primary:
        btn.config(
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            font=FONT_BOLD,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )
    else:
        btn.config(
            bg="#2a2a4a",
            fg=TEXT_COLOR,
            activebackground="#3a3a5a",
            activeforeground="white",
            font=FONT_NORMAL,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
search_button = Button(card, text="Search", command=find_password)
style_button(search_button)
search_button.grid(row=2, column=2, padx=(8, 0), sticky="ew")

generate_button = Button(card, text="Generate Password", command=generate_password)
style_button(generate_button)
generate_button.grid(row=4, column=2, padx=(8, 0), sticky="ew")

add_button = Button(card, text="Add", width=36, command=save)
style_button(add_button, primary=True)
add_button.grid(row=5, column=0, columnspan=3, pady=(20, 5), sticky="ew", ipady=4)

# Subtle footer
footer = Label(
    card,
    text="Passwords are saved locally to password.txt",
    font=("Segoe UI", 8),
    fg="#666680",
    bg=CARD_BG
)
footer.grid(row=6, column=0, columnspan=3, pady=(15, 0))

# Make columns expand nicely
card.columnconfigure(1, weight=1)

window.mainloop()
