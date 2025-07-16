import copy
import random

from ShootResult import ShootResult
from ShipDirection import ShipDirection
from ShipMode import ShipMode


class ShipField:
    field_size = 10

    def __init__(self):
        self.field = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.field_mode = ShipMode.INACTIVE
        self.ship_size = 4
        self.ship_direction = ShipDirection.VERTICAL

    def from_json(self, obj):
        self.field = obj['field']
        self.ships = obj['ships']
        ShipField.field_size = obj['field_size']
        self.field_mode = ShipMode.from_string(obj['field_mode'])
        self.ship_size = obj['ship_size']
        self.ship_direction = ShipDirection.from_string(obj['ship_direction'])

    def __getitem__(self, item):
        if item is None:
            return None

        if type(item) is not int and item.isnumeric():
            item = int(item)

        if type(item) is int and 0 <= item < len(self.field):
            return self.field[item]

        return None

    def action(self, row, col):
        self.clear_marker()

        if self.field_mode == ShipMode.PUT:
            if self.check_ship(row, col):
                self.get_ship(row, col)

            elif self.ship_size in self.ships and self.check_possible(row, col):
                self.set_ship(row, col)

        elif self.field_mode == ShipMode.SHOOT:
            self.shoot(row, col)

    def target(self, row, col):
        self.clear_marker()

        if self.field_mode == ShipMode.PUT:
            if self.check_possible(row, col):
                if self.ship_direction == ShipDirection.VERTICAL:
                    for r in range(row, row + self.ship_size):
                        if self.ship_size in self.ships:
                            self.field[r * ShipField.field_size + col] = "p"
                        else:
                            self.field[r * ShipField.field_size + col] = "r"

                if self.ship_direction == ShipDirection.HORIZONTAL:
                    for c in range(col, col + self.ship_size):
                        if self.ship_size in self.ships:
                            self.field[row * ShipField.field_size + c] = "p"
                        else:
                            self.field[row * ShipField.field_size + c] = "r"
        elif self.field_mode == ShipMode.SHOOT:
            self.field[row * ShipField.field_size + col] += "+"

    def clear_marker(self):
        for i in range(0, len(self.field)):
            if self.field[i] == "p" or self.field[i] == "r":
                self.field[i] = ""

            if "+" in self.field[i]:
                self.field[i] = self.field[i].replace("+", "")

    def set_ship(self, row, col):
        if row < 0 or row > ShipField.field_size:
            return
        if col < 0 or col > ShipField.field_size:
            return
        index = row * ShipField.field_size + col
        if self.ship_direction == ShipDirection.VERTICAL:
            if ShipField.field_size - row < self.ship_size:
                return
            for r in range(row, row + self.ship_size):
                index = r * ShipField.field_size + col
                self.field[index] = "1"
        if self.ship_direction == ShipDirection.HORIZONTAL:
            if ShipField.field_size - col < self.ship_size:
                return
            for c in range(col, col + self.ship_size):
                index = row * ShipField.field_size + c
                self.field[index] = "1"

        if self.ship_size in self.ships:
            self.ships.remove(self.ship_size)
        self.print_field()

        if self.ship_size not in self.ships and len(self.ships) > 0:
            self.ship_size = max(self.ships)

    def get_ship(self, row, col):
        if row < 0 or row > ShipField.field_size:
            return
        if col < 0 or col > ShipField.field_size:
            return

        self.field[row * ShipField.field_size + col] = ""

        ship_size = 1
        ship_direction = ShipDirection.UNKNOWN

        # проверим вертикаль
        for r in range(row + 1, ShipField.field_size):
            if self.check_ship(r, col):
                ship_size += 1
                ship_direction = ShipDirection.VERTICAL
                self.field[r * ShipField.field_size + col] = ""
            else:
                break

        for r in range(row - 1, -1, -1):
            if self.check_ship(r, col):
                ship_size += 1
                ship_direction = ShipDirection.VERTICAL
                self.field[row * ShipField.field_size + col] = ""
            else:
                break

        if ship_direction == ShipDirection.UNKNOWN:

            # проверим горизонталь
            for c in range(col + 1, ShipField.field_size):
                if self.check_ship(row, c):
                    ship_size += 1
                    ship_direction = ShipDirection.HORIZONTAL
                    self.field[row * ShipField.field_size + c] = ""
                else:
                    break

            for c in range(col - 1, -1, -1):
                if self.check_ship(row, c):
                    ship_size += 1
                    ship_direction = ShipDirection.HORIZONTAL
                    self.field[row * ShipField.field_size + c] = ""
                else:
                    break
        self.set_ship_direction(ship_direction)
        self.set_ship_size(ship_size)
        self.ships.append(ship_size)

    def shoot(self, row, col):
        if row < 0 or row > ShipField.field_size - 1:
            return ShootResult.UNDEFINED
        if col < 0 or col > ShipField.field_size - 1:
            return ShootResult.UNDEFINED
        index = row * ShipField.field_size + col
        if (self.field[index]).strip() == "":
            self.field[index] = "0"
            return ShootResult.EMPTY
        elif (self.field[index]).strip() == "1":
            self.field[index] = "\\"
            return ShootResult.DAMAGED
        else:
            return ShootResult.UNDEFINED

    def check_ship(self, row, col):
        # функция должна возвражать тру, если в заданной клетке есть корабль
        # в противном случае фолс
        return self.field[row * ShipField.field_size + col].strip() == "1"

    def check_possible(self, row, col):
        # Функция должна возвращать True, если можно поставить сюда корабль,
        # в противном случае - False
        if self.ship_direction == ShipDirection.VERTICAL:
            # Здесь мы знаем, что корабль помещается на поле.
            if ShipField.field_size - row >= self.ship_size:
                # Теперь нужно проверить, не заблокировано ли какое-то из полей,
                for r in range(row, row + self.ship_size):
                    if not self.check_blocked(r, col):
                        return False
                return True

        if self.ship_direction == ShipDirection.HORIZONTAL:
            if ShipField.field_size - col >= self.ship_size:
                for c in range(col, col + self.ship_size):
                    if not self.check_blocked(row, c):
                        return False
                return True

        return False

    def check_blocked(self, row, col):
        # Функция возвращает True, если все клетки вокруг клетки с координатами row, col
        # либо находятся за пределами поля, либо в них нет корабля/они пустые
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < ShipField.field_size and 0 <= c < ShipField.field_size:
                    cell = (self.field[r * ShipField.field_size + c]).strip()
                    if cell != '' and cell != 'p':
                        return False
        return True

    def set_ship_size(self, value):
        if value is None:
            return

        if type(value) is str and value.isnumeric():
            value = int(value)

        if type(value) is int and 1 <= value <= 4:
            self.ship_size = value

    def set_ship_direction(self, value):
        if value is None:
            return

        if type(value) is not ShipDirection:
            return

        if value != ShipDirection.UNKNOWN:
            self.ship_direction = value

    def toggle_ship_direction(self):
        if self.ship_direction == ShipDirection.VERTICAL:
            self.ship_direction = ShipDirection.HORIZONTAL
        else:
            self.ship_direction = ShipDirection.VERTICAL

    def set_field_mode(self, value):
        if value is None:
            return

        if type(value) is not ShipMode:
            return

        self.field_mode = value


    def clear_field(self):
        self.field = [' ' for _ in range(self.field_size * self.field_size)]
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.ship_size = 4
        self.field_mode = ShipMode.PUT
        self.ship_direction = ShipDirection.VERTICAL

    def randomize_ships(self):
        self.clear_field()

        ships_to_place = self.ships.copy()
        placed_ships = []

        for size in ships_to_place:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, ShipField.field_size - 1)
                col = random.randint(0, ShipField.field_size - 1)
                direction = random.choice([ShipDirection.VERTICAL, ShipDirection.HORIZONTAL])

                self.set_ship_size(size)
                self.set_ship_direction(direction)

                if self.check_possible(row, col):
                    self.set_ship(row, col)
                    placed = True
                    placed_ships.append(size)
                attempts += 1

        print(f"Placed ships: {placed_ships}")


    def print_field(self):
        print(self.ships)
        for r in range(0, ShipField.field_size):
            blocked_string = ""
            ship_string = ""
            for c in range(0, ShipField.field_size):
                blocked_string += str(self.check_blocked(r, c))[0] + ", "
                ship_string += self.field[r * ShipField.field_size + c] + ', '
            print(ship_string[:-2])
            # print(blocked_string[:-2] + '          ' + ship_string[:-2])
        print("********************************************************************")

    @staticmethod
    def convert_to_json(obj):
        if isinstance(obj, ShipField):
            result = copy.deepcopy(obj.__dict__)
            result['field_mode'] = obj.field_mode.value
            result['ship_direction'] = obj.ship_direction.value
            result['field_size'] = ShipField.field_size
            return result
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
