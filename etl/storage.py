import abc
import datetime
from typing import Any, Dict


class BaseStorage(abc.ABC):
    """
    Abstract state storage.

    Allows you to save and receive the state.
    The way the state is stored may vary depending
    on the final implementation. For example, you can store information
    in a database or in a distributed file storage.
    """
    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]):
        """Save the state to the storage."""
    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Get the state from the repository."""


class State:

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        self.storage.set(key, f'{value}')

    def get_state(self, key: str) -> Any:
        time = self.storage.get(key)
        if time is None:
            self.storage.set(key, str(datetime.datetime.min))
        return time.decode("utf-8")
