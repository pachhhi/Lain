from enum import Enum, auto

class Intent(Enum):
    GREETING = auto()
    CHAT = auto()
    MEMORY = auto()
    PROJECT = auto()