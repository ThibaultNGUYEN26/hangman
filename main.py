from tkinter import *
from random import choice

WIDTH = 800
HEIGHT = 600
FULLSCREEN_STATE = False
LIVES = 6

words_list = []
def random_word():
    with open("words.txt", "r") as f:
        for x in f:
            words_list.append(x.upper().strip())
    return choice(words_list)

def change_char_in_string(original_string, index, new_char):
    string_list = list(original_string)
    string_list[index] = new_char
    modified_string = ''.join(string_list)
    return modified_string

def reveal_letter(word, covered_letters, letter):
    covered_list = list(covered_letters)
    for i in range(len(word)):
        if word[i] == letter:
            covered_list[i * 2] = letter
    return ''.join(covered_list)

def on_key_press(event):
    global covered_letters, LIVES
    user_input = event.char.upper()
    if not user_input.isalpha():
        pass
    else:
        handle_guess(user_input)

def on_button_click(letter):
    handle_guess(letter)

def handle_guess(letter):
    global covered_letters, LIVES
    if letter in guessed_letters:
        return

    guessed_letters.add(letter)
    button = buttons_dict.get(letter)
    if letter in word:
        covered_letters = reveal_letter(word, covered_letters, letter)
        secret_label.config(text=covered_letters)
        print("Updated covered letters: " + covered_letters)
        if button:
            button.config(bg="green", state=DISABLED)
    else:
        print("NOP")
        LIVES -= 1
        draw_hangman(LIVES)
        if button:
            button.config(bg="red", state=DISABLED)
        if LIVES > 1:
            print(f"{LIVES} lives remaining")
        elif LIVES == 1:
            print(f"{LIVES} life remaining")
        else:
            print("YOU LOST.")
            for i, button in enumerate(buttons):
                button.config(bg="red", state=DISABLED)

def fullscreen_window(event):
    global FULLSCREEN_STATE
    FULLSCREEN_STATE = not FULLSCREEN_STATE
    root.attributes("-fullscreen", FULLSCREEN_STATE)

def resize_keyboard_frame(event=None):
    new_width = int(root.winfo_width() * 0.7)
    new_height = int(root.winfo_height() * 0.3)
    keyboard_frame.config(width=new_width, height=new_height)
    keyboard_frame.place_configure(relx=0.5, rely=0.8, anchor=CENTER)
    resize_secret_label()
    resize_buttons()

def resize_secret_label():
    word_length = len(word)
    max_font_size = int(root.winfo_width() / 20)
    min_font_size = 10

    font_size = max(min_font_size, min(max_font_size, root.winfo_width() // word_length))

    secret_label.config(font=("Futura", font_size, "bold"))
    secret_label.place_configure(relx=0.5, rely=0.5, anchor=CENTER)

def resize_buttons():
    button_width = keyboard_frame.winfo_width() // 10 - 15
    button_height = keyboard_frame.winfo_height() // 3 - 15

    x_offset_first_row = (keyboard_frame.winfo_width() - (10 * (button_width + 10) - 10)) // 2
    x_offset_second_row = (keyboard_frame.winfo_width() - (9 * (button_width + 10) - 10)) // 2
    x_offset_third_row = (keyboard_frame.winfo_width() - (7 * (button_width + 10) - 10)) // 2

    y_offset = (keyboard_frame.winfo_height() - (3 * (button_height + 10) - 10)) // 2
    
    font_size = int(button_height * 0.4)

    for i, button in enumerate(buttons):
        if i < 10:
            row, col, x_offset = 0, i, x_offset_first_row
        elif i < 19:
            row, col, x_offset = 1, i - 10, x_offset_second_row
        else:
            row, col, x_offset = 2, i - 19, x_offset_third_row
        button.place(x=col * (button_width + 10) + x_offset, y=row * (button_height + 10) + y_offset, width=button_width, height=button_height)
        button.config(font=("Futura", font_size))

def exit_window(*args):
    root.destroy()

def draw_hangman(lives_left):
    canvas.delete("all")

    canvas_width = int(root.winfo_width() // 3)
    canvas_height = int(root.winfo_height() // 3)

    canvas.place_configure(width=canvas_width, height=canvas_height)

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    base_y = canvas_height - int(canvas_height * 0.1)
    pole_height = int(canvas_height * 0.8)
    pole_x = int(canvas_width * 0.2)
    arm_length = int(canvas_width * 0.4)
    head_radius = int(min(canvas_width, canvas_height) * 0.05)

    canvas.create_line(pole_x + arm_length / 3, base_y, pole_x + arm_length / 2 + arm_length / 6, base_y, width=4)  # Base
    canvas.create_line(pole_x + arm_length / 2, base_y, pole_x + arm_length / 2, base_y - pole_height, width=4)  # Pole
    canvas.create_line(pole_x + arm_length / 2, base_y - pole_height, pole_x + arm_length, base_y - pole_height, width=4)  # Arm
    canvas.create_line(pole_x + arm_length, base_y - pole_height, pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1), width=4)  # Rope

    if lives_left < 6:
        canvas.create_oval(pole_x + arm_length - head_radius, base_y - pole_height + int(pole_height * 0.1), pole_x + arm_length + head_radius, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius, width=4)  # Head
    if lives_left < 5:
        canvas.create_line(pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius, pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.3), width=4)  # Body
    if lives_left < 4:
        canvas.create_line(pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.1), pole_x + arm_length - int(canvas_width * 0.05), base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.2), width=4)  # Left arm
    if lives_left < 3:
        canvas.create_line(pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.1), pole_x + arm_length + int(canvas_width * 0.05), base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.2), width=4)  # Right arm
    if lives_left < 2:
        canvas.create_line(pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.3), pole_x + arm_length - int(canvas_width * 0.05), base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.4), width=4)  # Left leg
    if lives_left < 1:
        canvas.create_line(pole_x + arm_length, base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.3), pole_x + arm_length + int(canvas_width * 0.05), base_y - pole_height + int(pole_height * 0.1) + 2 * head_radius + int(pole_height * 0.4), width=4)  # Right leg

root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Hangman")
root.minsize(int(WIDTH // 1.2), int(HEIGHT // 1.2))

word = random_word()
covered_letters = ' '.join('_' for _ in word)
secret_label = Label(root, text=covered_letters, font=("Futura", 20, "bold"))
secret_label.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas = Canvas(root, bg='white')
canvas.place(relx=0.5, rely=0.1, anchor=N, width=int(WIDTH // 3), height=int(HEIGHT // 3))
draw_hangman(LIVES)

print(f"{LIVES} lives remaining")
print(word)

keyboard_frame = Frame(root, bg='gray')
keyboard_frame.place(relx=0.5, rely=0.85, anchor=CENTER)

with open("keyboard_EN.txt", "r") as f:
    alphabet = f.readline().strip()
buttons = []
buttons_dict = {}
guessed_letters = set()

for letter in alphabet:
    button = Button(keyboard_frame, text=letter, command=lambda l=letter: on_button_click(l))
    buttons.append(button)
    buttons_dict[letter] = button

resize_buttons()

root.bind('<KeyPress>', on_key_press)
root.bind('<F11>', fullscreen_window)
root.bind('<Configure>', resize_keyboard_frame)
root.bind('<Escape>', exit_window)

canvas.bind("<Configure>", lambda event: draw_hangman(LIVES))

root.update_idletasks()
resize_keyboard_frame()

root.mainloop()
