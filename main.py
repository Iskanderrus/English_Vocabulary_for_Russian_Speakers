from tkinter import *
import pandas
import random
from PIL import ImageTk, Image
import os
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/data.csv")

to_learn = data.to_dict(orient="records")
current_card = dict()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text=f"{current_card['English']}", fill="white")
    canvas.itemconfig(card_word, text=current_card["Meaning"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    global data
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)


def reset_data():
    global data, to_learn, current_card
    try:
        messagebox.askokcancel(title="Do you really want to reset?", message="This action will delete all your learned "
                                                                             "cards.")
    except FileNotFoundError:
        pass
    else:
        data = pandas.read_csv("data/data.csv")
        os.remove("data/words_to_learn.csv")
        to_learn = data.to_dict(orient="records")
        current_card = dict()
        next_card()


window = Tk()
window.title("English Vocabulary Master")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 158, text="Title", font=("Arial", 30, "italic"))
card_word = canvas.create_text(400, 263, text="WORD", font=("Arial", 22, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png", width=100, height=99)
unknown_button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=next_card)
unknown_button.grid(row=2, column=0)

check_image = PhotoImage(file="images/right.png", width=100, height=99)
known_button = Button(image=check_image, highlightthickness=0, borderwidth=0, command=is_known)
known_button.grid(row=2, column=1)

image = Image.open("images/reset.png")
image = image.resize((70, 70), Image.ANTIALIAS)
reset_image = ImageTk.PhotoImage(image)
reset_button = Button(image=reset_image, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, command=reset_data)
reset_button.grid(row=0, column=2)

image = Image.open("images/exit.png")
image = image.resize((70, 70), Image.ANTIALIAS)
exit_image = ImageTk.PhotoImage(image)
exit_button = Button(image=exit_image, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, command=window.destroy)
exit_button.grid(row=0, column=3)

next_card()

window.mainloop()
