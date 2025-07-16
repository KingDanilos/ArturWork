from enum import Enum


class ShipMode(Enum):
    PUT = "PUT"
    SHOOT = "SHOOT"
    INACTIVE = "INACTIVE"

    @staticmethod
    def from_string(raw_value):
        if raw_value:
            value = raw_value.upper()
            if value in ShipMode.__members__:
                return ShipMode[value]
        return ShipMode.INACTIVE
