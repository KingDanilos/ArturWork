from ShipField import ShipField



def verify_value(actual, expected):
    if actual == expected:
        print("OK")
    else:
        print("ERROR")


my_field = ShipField()

print("set_ship_size()")
my_field.set_ship_size(1)

verify_value(my_field.ship_size, 1)

my_field.set_ship_size(0)
my_field.set_ship_size(6)

verify_value(my_field.ship_size, 1)

my_field.set_ship_size([])
my_field.set_ship_size("")
my_field.set_ship_size(None)
my_field.set_ship_size(True)
my_field.set_ship_size(False)
verify_value(my_field.ship_size, 1)

my_field.set_ship_size("2")
verify_value(my_field.ship_size, 2)
print()

print("set_ship_direction()")
my_field.set_ship_direction(1)
verify_value(my_field.ship_direction, 1)

my_field.set_ship_direction(-1)
my_field.set_ship_direction(6)
verify_value(my_field.ship_direction, 1)

my_field.set_ship_direction([])
my_field.set_ship_direction("")
my_field.set_ship_direction(None)
my_field.set_ship_direction(True)
my_field.set_ship_direction(False)
verify_value(my_field.ship_direction, 1)

my_field.set_ship_direction("0")
verify_value(my_field.ship_direction, 0)
print()

print('toggle_field_mode()')
verify_value(my_field.field_mode, 0)

my_field.toggle_field_mode()
verify_value(my_field.field_mode, 1)

my_field.toggle_field_mode()
verify_value(my_field.field_mode, 0)
print()

print("set_ship()")
verify_value(my_field.field[0], " ")

my_field.set_ship_size(1,)
my_field.set_ship_direction(0)
my_field.set_ship(0, 0)

verify_value(my_field.field[0], "1")
print()

my_field.set_ship_size(4)
my_field.set_ship_direction(0)
my_field.set_ship(5, 5)
my_field.print_field()