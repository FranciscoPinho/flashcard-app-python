from tkinter import *
import pandas
import os
import random

BACKGROUND_COLOR = "#B1DDC6"
current_word = None
flip_timer = None
# ---------------------------- CONVERT CSV TO DICT AND USE DICT ------------------------------- #
if os.path.isfile("data/words_to_learn.csv"):
    dataframe = pandas.read_csv("data/words_to_learn.csv")
else:
    dataframe = pandas.read_csv("data/french_words.csv")
words_dict = dataframe.to_dict(orient="records")


# ---------------------------- GENERATE AND FLIP CARDS ------------------------------- #

def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_word["English"], fill="white")


def generate_random_word():
    global current_word, flip_timer
    current_word = random.choice(words_dict)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_word["French"], fill="black")
    if flip_timer is not None:
        window.after_cancel(id=flip_timer)
    flip_timer = window.after(3000, flip_card)


def learn_word():
    words_dict.remove(current_word)
    data = pandas.DataFrame(words_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_random_word()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas_title = canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_random_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=learn_word)
right_button.grid(row=1, column=1)

generate_random_word()

window.mainloop()