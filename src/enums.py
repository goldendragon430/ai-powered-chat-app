from enum import StrEnum, auto


class ModelNameEnum(StrEnum):
    GPT3_5 = auto()
    GPT4 = auto()


class RoleEnum(StrEnum):
    SYSTEM = auto()
    AI = auto()
    HUMAN = auto()
