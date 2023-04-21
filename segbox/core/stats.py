# as borg pattern


class Stats:
    """Borg pattern implementation for sharing data between classes"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

        self.store = {}
        for i in range(0, 6):
            self.store[f'img_{i}'] = {'name': None, 'origin_path': None, 'arr_path': None}
            self.store[f'mask_{i}'] = {'pos': [], 'neg': [], 'data': None}

