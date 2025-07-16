from enum import Enum

class GameMode(Enum):
    MENU = 'MENU'
    PLAN = 'PLAN'
    BATTLE = 'BATTLE'
    END = 'END'

    @staticmethod
    def from_string(raw_value):
        if raw_value:
            value = raw_value.upper()
            if value in GameMode.__members__:
                return GameMode[value]
        return GameMode.MENU