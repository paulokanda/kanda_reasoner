"""Support missing-docstring insertion workflows."""

class UserBox:
    def __init__(self, user_id: int, display_name: str, *, active: bool = True):
        self.user_id = user_id
        self.display_name = display_name
        self.active = active

    @property
    def label(self) -> str:
        return f"{self.user_id}:{self.display_name}"

    def rename(self, new_name: str) -> None:
        self.display_name = new_name

    def deactivate(self) -> None:
        self.active = False
