from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class WebsocketDataTypes(str, Enum):
    AUTH = "AUTH"
    TEXT = "TEXT"
    JSON = "JSON"