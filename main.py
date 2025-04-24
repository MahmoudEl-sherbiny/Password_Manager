from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    # use insert method to put a value in entry
    password_entry.insert(0, password)
    # to copy the  password into clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def insert():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave and fields empty!")
    else:
        try:
            with open("Data.json", "r") as data_file:
                # Reading old data
                try:
                    # This fetch if there is a file but don't contain anything
                    data = json.load(data_file)
                except json.decoder.JSONDecodeError:
                    data = {}
        except FileNotFoundError:
            # target If the user open app at first time and no file called Data.json
            with open("Data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating old data
            data.update(new_data)

            with open("Data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Error", message="Please Write data inside website cell")
    else:
        try:
            with open("Data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
           messagebox.showinfo(title="Error", message="File Not Found for now")
        except json.decoder.JSONDecodeError:
            # If you have file but you don't have anything
            messagebox.showinfo(title="Error", message="There is No Data File Found Please add data ")
        else:
            if website in data:
                user = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Username: {user}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No Details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manger")
window.config(pady=50, padx=50)

# create your board by canvas
board = Canvas(width=200, height=200)
# put your image inside object from class PhotoImage
logo = PhotoImage(file="logo.png")
# use .create_image from canvas class to put image inside board
board.create_image(100, 100,image=logo)
board.grid(row=0, column=1)

# create labels --> Website: , Email/Username: , Password:
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)


username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Create Entries --> 2 text with width 35 and 1 text with 21
website_entry = Entry(width=31)
website_entry.grid(row=1, column=1)
website_entry.focus()


username_entry = Entry(width=51)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "Alii_Moaz@gmail.com")

password_entry = Entry(width=31)
password_entry.grid(row=3, column=1)

# Create buttons 1st for Generate Password 2nd for Add 3rd for Search
generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(row=3, column=2, padx=4, pady=5)

add = Button(text="Add", width=43, command=insert)
add.grid(row=4, column=1, columnspan=2)

search = Button(text="Search", width=15, command=find_password)
search.grid(row=1, column=2, padx=4, pady=5)



window.mainloop()
