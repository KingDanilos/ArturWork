import json
import os
import time
import random
from tkinter import *
from tkinter import filedialog
from ShipView import ShipView
from ShipMode import ShipMode
from ShipField import ShipField
from GameMode import GameMode
from ShipDirection import ShipDirection

active_view = {}

def create_view(window):
    field = ShipField()
    buttons = []
    view = ShipView(field, buttons)
    for r in range(0, field.field_size):
        for c in range(0, field.field_size):
            btn = Button(window, text='', width=5, height=2)
            btn.bind('<Button-1>', lambda e, x=r, y=c: left_button_click(view, x, y))
            btn.bind('<Button-3>', lambda e: right_button_click(view))
            btn.bind('<Enter>', lambda e, x=r, y=c: button_enter(view, x, y))
            buttons.append(btn)

    colorize(view)
    return view

def show_view(view, col_offset=0, row_offset=0):
    field_size = view.ship_field.field_size

    for r in range(0, field_size):
        for c in range(0, field_size):
            btn = view.buttons[r * field_size +c]
            btn.grid(column=c + col_offset, row=r + row_offset)

def hide_view(view):
    for button in view.buttons:
        button.grid_forget()


def colorize(view):
    field = view.ship_field
    for i in range(len(field.field)):
        bg = "white"
        if field.field[i] == "1":
            bg = 'pink'
        if field.field[i] == "\\":
            bg = 'grey'
        if field.field[i] == "0":
            bg = 'black'
        if field.field[i] == "p":
            bg = 'blue'
        if field.field[i] == "r":
            bg = 'red'
        if "+" in field.field[i]:
            bg = 'orange'

        view.buttons[i].configure(bg=bg)

    refresh_remaining_ships_label(view)


def keypress_handler(e):
    global active_view
    if e.keysym.isnumeric():
        active_view.ship_field.set_ship_size(e.keysym)


def left_button_click(view, row, col):
    view.ship_field.action(row, col)
    colorize(view)


def right_button_click(view):
    view.ship_field.toggle_ship_direction()
    colorize(view)


def button_enter(view, row, col):
    global active_view
    active_view = view
    if view == my_view:
        enemy_view.ship_field.clear_marker()
        my_view.ship_field.target(row, col)
    elif view == enemy_view:
        my_view.ship_field.clear_marker()
        enemy_view.ship_field.target(row, col)

    colorize(my_view)
    colorize(enemy_view)


def savebutton_click(view):
    file_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w") as f:
            json.dump({"shipField": view.ship_field}, f, default=ShipField.convert_to_json)


def loadbutton_click(view):
    file_path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
    if os.path.isfile(file_path):
        with open(file_path) as lines:
            view.ship_field.from_json(json.load(lines)['shipField'])

    colorize(view)


def endbutton_click(view):
    global game_mode

    # Spielfeld zurücksetzen
    view.ship_field.field = [' ' for _ in range(ShipField.field_size * ShipField.field_size)]
    view.ship_field.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    view.ship_field.ship_size = 4
    view.ship_field.field_mode = ShipMode.INACTIVE
    view.ship_field.ship_direction = ShipDirection.VERTICAL

    # Zurück ins Menü
    game_mode = GameMode.MENU
    update_game_mode()


def randomize_ships_in_right_view(view):
    view.ship_field.randomize_ships()
    colorize(view)


def refresh_remaining_ships_label(view):
    text = ''
    for i in range(1, 5):
        count = view.ship_field.ships.count(i)
        if count > 0:
            text += f'{"[]" * i}: {count}, '
    view.remaining_ships_text.set(text[:-2])


def next_game_mode():
    global game_mode

    if game_mode == GameMode.MENU:
        game_mode = GameMode.PLAN
    elif game_mode == GameMode.PLAN:
        game_mode = GameMode.BATTLE
    elif game_mode == GameMode.BATTLE:
        game_mode = GameMode.END

    update_game_mode()


def update_game_mode():
    global game_mode

    if game_mode == GameMode.MENU:
        window.geometry('400x280')
        my_view.ship_field.set_field_mode(ShipMode.INACTIVE)
        enemy_view.ship_field.set_field_mode(ShipMode.INACTIVE)

        lbl_lower_enemy_horizontal.grid_forget()
        lbl_lower_horizontal.grid_forget()

        savebutton.grid_forget()
        loadbutton.grid_forget()
        endbutton.grid_forget()
        randomize_button.grid_forget()
        randomize_button_enemy.grid_forget()

        start_button.grid(column=start_column_enemy_field, row=load_button_row, columnspan=4)
        load_game_button.grid(column=start_column_enemy_field, row=load_button_row + 1, columnspan=4)
        exit_button.grid(column=start_column_enemy_field, row=load_button_row + 2, columnspan=4)

        hide_view(my_view)
        hide_view(enemy_view)

    elif game_mode == GameMode.PLAN:
        window.geometry('1020x640')
        my_view.ship_field.set_field_mode(ShipMode.PUT)
        enemy_view.ship_field.set_field_mode(ShipMode.INACTIVE)

        enemy_view.ship_field.randomize_ships() #Beim starten werden zufällig beim Gegner die Schiffe aufgestellt. Kann man auch abstellen, wenn es nicht benötigt wird 

        lbl_lower_enemy_horizontal.grid(column=start_column_my_field, row=row_horizontal_separator, columnspan=10)
        lbl_lower_horizontal.grid(column=start_column_enemy_field, row=row_horizontal_separator, columnspan=10)

        savebutton.grid(column=start_column_my_field, row=load_button_row, columnspan=4)
        loadbutton.grid(column=start_column_my_field + 6, row=load_button_row, columnspan=4)

        start_button.grid(column=start_column_my_field, row=load_button_row + 1, columnspan=4)
        endbutton.grid(column=start_column_my_field + 6, row=load_button_row + 1, columnspan=4)

        randomize_button.grid(column=start_column_my_field, row=load_button_row + 2, columnspan=10, pady=10)
        randomize_button_enemy.grid(column=start_column_enemy_field, row=load_button_row + 1, columnspan=10)

        load_game_button.grid_forget()
        exit_button.grid_forget()

        show_view(my_view, start_column_my_field, start_row_my_field)
        show_view(enemy_view, start_column_enemy_field, start_row_enemy_field)

    elif game_mode == GameMode.BATTLE:
        window.geometry('1020x640')
        my_view.ship_field.set_field_mode(ShipMode.INACTIVE)
        enemy_view.ship_field.set_field_mode(ShipMode.SHOOT)

        lbl_lower_enemy_horizontal.grid_forget()
        lbl_lower_horizontal.grid_forget()

        savebutton.grid_forget()
        loadbutton.grid_forget()
        endbutton.grid_forget()

        start_button.grid_forget()
        load_game_button.grid_forget()
        exit_button.grid_forget()
        randomize_button.grid_forget()
        randomize_button_enemy.grid_forget()

        show_view(my_view, start_column_my_field, start_row_my_field)
        show_view(enemy_view, start_column_enemy_field, start_row_enemy_field)

    elif game_mode == GameMode.END:
        window.geometry('400x280')
        my_view.ship_field.set_field_mode(ShipMode.INACTIVE)
        enemy_view.ship_field.set_field_mode(ShipMode.INACTIVE)

        lbl_lower_enemy_horizontal.grid_forget()
        lbl_lower_horizontal.grid_forget()

        savebutton.grid_forget()
        loadbutton.grid_forget()
        exit_button.grid_forget()

        start_button.grid_forget()
        load_game_button.grid_forget()
        exit_button.grid_forget()
        randomize_button.grid_forget()
        randomize_button_enemy.grid_forget()

        hide_view(my_view)
        hide_view(enemy_view)

    lbl_left_vertical.grid(column=start_column_my_field - 1, row=start_row_my_field)
    lbl_center_vertical.grid(column=col_vertical_separator, row=start_row_my_field)
    lbl_upper_horizontal.grid(column=start_column_my_field, row=start_row_my_field - 1)


window = Tk()
window.title("Ship Craft!")
window.bind_all('<KeyPress>', keypress_handler)

start_column_my_field = 1
start_row_my_field = 1

start_column_enemy_field = start_column_my_field + ShipField.field_size + 1
start_row_enemy_field = start_row_my_field

col_vertical_separator = start_column_my_field + ShipField.field_size
row_horizontal_separator = start_row_my_field + ShipField.field_size

load_button_row = start_row_my_field + ShipField.field_size + 1

my_view = create_view(window)
enemy_view = create_view(window)
active_view = my_view

lbl_left_vertical = Label(window, text='', width=5, height=2)
lbl_center_vertical = Label(window, text='', width=5, height=2)
lbl_upper_horizontal = Label(window, text='', width=5, height=2)


lbl_lower_horizontal = Label(window, text='', width=50, height=2, textvariable=my_view.remaining_ships_text)
lbl_lower_enemy_horizontal = Label(window, text='', width=50, height=2, textvariable=enemy_view.remaining_ships_text)


savebutton = Button(window, text='SAVE', width=20, height=2, command=lambda: savebutton_click(my_view))
loadbutton = Button(window, text='LOAD', width=20, height=2, command=lambda: loadbutton_click(my_view))
endbutton = Button(window, text='END', width=20, height=2, command=lambda: endbutton_click(my_view))


start_button = Button(window, text='START', width=20, height=2, command=next_game_mode)
load_game_button = Button(window, text='LOAD', width=20, height=2)
exit_button = Button(window, text='EXIT', width=20, height=2)
randomize_button = Button(window, text='RANDOMIZE', width=20, height=2, command=lambda: randomize_ships_in_right_view(my_view))
randomize_button_enemy = Button(window, text='RANDOMIZE', width=20, height=2, command=lambda: randomize_ships_in_right_view(enemy_view))


game_mode = GameMode.MENU
update_game_mode()

window.mainloop()