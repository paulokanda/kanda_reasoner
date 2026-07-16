"""Support missing-docstring insertion workflows."""

def get_name(user_id: int) -> str:
    return str(user_id)

class Box:
    def __init__(self, value: int):
        self.value = value

    def set_value(self, value: int) -> None:
        self.value = value
