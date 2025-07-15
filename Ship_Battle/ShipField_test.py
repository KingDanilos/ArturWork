from unittest import TestCase
from ShipField import ShipField
from ShootResult import ShootResult
from ShipDirection import ShipDirection
from ShipMode import ShipMode


class TestShipField(TestCase):

    def test_set_ship_size(self):
        ship_field = ShipField()  # Заводим объект типа ShipField

        ship_field.set_ship_size(1)
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(2)
        self.assertEqual(ship_field.ship_size, 2)
        ship_field.set_ship_size(3)
        self.assertEqual(ship_field.ship_size, 3)
        ship_field.set_ship_size(4)
        self.assertEqual(ship_field.ship_size, 4)

    def test_set_ship_size_outofrange(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        ship_field.set_ship_size(1)

        ship_field.set_ship_size(-1)
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(0)
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(6)
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(100)
        self.assertEqual(ship_field.ship_size, 1)

    def test_set_ship_size_wrongtype(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        ship_field.set_ship_size(1)

        ship_field.set_ship_size([])
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size('')
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(None)
        self.assertEqual(ship_field.ship_size, 1)
        ship_field.set_ship_size(False)
        self.assertEqual(ship_field.ship_size, 1)

    def test_toggle_field_mode(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        self.assertEqual(ship_field.field_mode, ShipMode.PUT)  # Проверяем, что изначальное значение field_mode равно 0

        ship_field.toggle_field_mode()  # Вызываем метод, который тестируем
        self.assertEqual(ship_field.field_mode, ShipMode.SHOOT)  # Проверяем, что field_mode принял желаемое значение

        ship_field.toggle_field_mode()  # Вызываем метод, который тестируем
        self.assertEqual(ship_field.field_mode, ShipMode.PUT)  # Проверяем, что field_mode принял желаемое значение

    def test_action(self):
        self.fail()

    def test_target(self):
        self.fail()

    def test_clear_marker(self):
        ship_field = ShipField()
        ship_field.field[0] = 'p'
        ship_field.field[ship_field.field_size - 1] = 'p'
        ship_field.field[ship_field.field_size - 4] = 'r'
        ship_field.clear_marker()

        self.assertNotIn('p', ship_field.field)
        self.assertNotIn('r', ship_field.field)

    def test_shoot_empty(self):
        ship_field = ShipField()

        self.assertEqual(ship_field.field[0].strip(), '')
        result = ship_field.shoot(0, 0)

        self.assertEqual(ship_field.field[0].strip(), '0')
        self.assertEqual(result, ShootResult.EMPTY)

    def test_shoot_ship(self):
        ship_field = ShipField()

        ship_field.field[0] = '1'
        result = ship_field.shoot(0, 0)

        self.assertEqual(ship_field.field[0].strip(), '\\')
        self.assertEqual(result, ShootResult.DAMAGED)

    def test_shoot_unknown(self):
        ship_field = ShipField()

        ship_field.field[0] = 'x'
        result = ship_field.shoot(0, 0)

        self.assertEqual(ship_field.field[0].strip(), 'x')
        self.assertEqual(result, ShootResult.UNDEFINED)

    def test_shoot_outofrange(self):
        ship_field = ShipField()
        old_field_string = str.join(' ', ship_field.field)

        result = ship_field.shoot(-1, -1)
        self.assertEqual(result, ShootResult.UNDEFINED)

        result = ship_field.shoot(-1, 0)
        self.assertEqual(result, ShootResult.UNDEFINED)

        result = ship_field.shoot(1000, 1000)
        self.assertEqual(result, ShootResult.UNDEFINED)

        result = ship_field.shoot(0, 1000)
        self.assertEqual(result, ShootResult.UNDEFINED)

        new_field_string = str.join(' ', ship_field.field)
        self.assertEqual(new_field_string, old_field_string)

    def test_check_possible_false(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_size(4)
        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)

        # action действие
        ship_field.set_ship(5, 3)

        # assertion проверка занятых
        self.assertEqual(ship_field.check_possible(5, 3), False)
        self.assertEqual(ship_field.check_possible(5, 4), False)
        self.assertEqual(ship_field.check_possible(5, 5), False)
        self.assertEqual(ship_field.check_possible(5, 6), False)

        # проверка строки ниже
        self.assertEqual(ship_field.check_possible(6, 3), False)
        self.assertEqual(ship_field.check_possible(6, 4), False)
        self.assertEqual(ship_field.check_possible(6, 5), False)
        self.assertEqual(ship_field.check_possible(6, 6), False)

        # проверка строки выше
        self.assertEqual(ship_field.check_possible(4, 3), False)
        self.assertEqual(ship_field.check_possible(4, 4), False)
        self.assertEqual(ship_field.check_possible(4, 5), False)
        self.assertEqual(ship_field.check_possible(4, 6), False)

    def test_check_possible_true(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_size(4)
        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)

        # action действие
        ship_field.set_ship(5, 3)

        # проверка свободных ниже на 2 строки
        self.assertEqual(ship_field.check_possible(7, 3), True)
        self.assertEqual(ship_field.check_possible(7, 4), True)
        self.assertEqual(ship_field.check_possible(7, 5), True)
        self.assertEqual(ship_field.check_possible(7, 6), True)

        # проверка свободных выше на 2 строки
        self.assertEqual(ship_field.check_possible(3, 3), True)
        self.assertEqual(ship_field.check_possible(3, 4), True)
        self.assertEqual(ship_field.check_possible(3, 5), True)
        self.assertEqual(ship_field.check_possible(3, 6), True)

    def test_check_blocked(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_size(4)
        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)
        # action действие
        ship_field.set_ship(5, 3)
        # assertion проверка занятых
        self.assertEqual(ship_field.check_blocked(5, 3), False)
        self.assertEqual(ship_field.check_blocked(5, 4), False)
        self.assertEqual(ship_field.check_blocked(5, 5), False)
        self.assertEqual(ship_field.check_blocked(5, 6), False)
        #проверка строки ниже
        self.assertEqual(ship_field.check_blocked(6, 3), False)
        self.assertEqual(ship_field.check_blocked(6, 4), False)
        self.assertEqual(ship_field.check_blocked(6, 5), False)
        self.assertEqual(ship_field.check_blocked(6, 7), False)
        #проверка свободных ниже на 2 строки
        self.assertEqual(ship_field.check_blocked(7, 3), True)
        self.assertEqual(ship_field.check_blocked(7, 4), True)
        self.assertEqual(ship_field.check_blocked(7, 5), True)
        self.assertEqual(ship_field.check_blocked(7, 6), True)

    def test_set_ship_direction(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        ship_field.set_ship_direction(ShipDirection.VERTICAL)
        self.assertEqual(ship_field.ship_direction, ShipDirection.VERTICAL)

        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)
        self.assertEqual(ship_field.ship_direction, ShipDirection.HORIZONTAL)

    def test_set_ship_direction_outofrange(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        ship_field.set_ship_direction(1)

        ship_field.set_ship_direction(-1)
        ship_field.set_ship_direction(2)
        self.assertEqual(ship_field.ship_direction, ShipDirection.VERTICAL)

    def test_set_ship_direction_wrongtype(self):
        ship_field = ShipField()  # Заводим объект типа ShipField
        ship_field.set_ship_direction(1)

        ship_field.set_ship_direction(None)
        ship_field.set_ship_direction([2])
        ship_field.set_ship_direction({})
        self.assertEqual(ship_field.ship_direction, ShipDirection.VERTICAL)

    def test_toggle_ship_direction(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)
        # action действие
        ship_field.toggle_ship_direction()
        # assertion проверка
        self.assertEqual(ship_field.ship_direction, ShipDirection.VERTICAL)

        ship_field.toggle_ship_direction()
        self.assertEqual(ship_field.ship_direction, ShipDirection.HORIZONTAL)

    def test_set_ship(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_size(4)
        ship_field.set_ship_direction(ShipDirection.HORIZONTAL)
        # action действие
        ship_field.set_ship(5, 3)
        # assertion проверка
        self.assertEqual(ship_field.field[53].strip(), '1')
        self.assertEqual(ship_field.field[54].strip(), '1')
        self.assertEqual(ship_field.field[55].strip(), '1')
        self.assertEqual(ship_field.field[56].strip(), '1')

    def test_set_ship_size4_vertical_outofrange(self):
        # arrangement установка
        ship_field = ShipField()
        ship_field.set_ship_size(4)
        ship_field.set_ship_direction(ShipDirection.VERTICAL)
        old_field_string = str.join(" ", ship_field.field)
        # action действие
        ship_field.set_ship(7, 3)
        # assertion проверка
        new_field_string = str.join(" ", ship_field.field)
        self.assertEqual(new_field_string, old_field_string)