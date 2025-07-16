from enum import Enum


class ShipDirection(Enum):
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def from_string(raw_value):
        if raw_value:
            value = raw_value.upper()
            if value in ShipDirection.__members__:
                return ShipDirection[value]
        return ShipDirection.UNKNOWN
