from enum import IntEnum


class AccessLevel(IntEnum):
    user = 0
    admin = 5
    default = user
