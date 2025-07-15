from tkinter import StringVar

class ShipView:

    def __init__(self, ship_field, buttons):
        self.ship_field = ship_field
        self.buttons = buttons
        self.remaining_ships_text = StringVar()