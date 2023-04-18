import typing as t
from collections import OrderedDict

from loguru import logger


class DataHandler:
    def __init__(self):
        self._store = OrderedDict()
        self._case_name = None
        logger.info(f'Init {self.__class__.__name__}')

    def __getitem__(self, key: str) -> t.Any:
        """Returns the value of a given key from the ephemeral input"""
        return self._store.get(key, None)

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Sets value for a given key  from the ephemeral output"""
        self._store[key] = value

    @property
    def case_name(self) -> str:
        """Returns case name"""
        return self._case_name

    @case_name.setter
    def case_name(self, value: t.Any) -> None:
        """Sets case name"""
        self._case_name = value
