# as borg pattern
import os


class Stats:
    """Borg pattern implementation for sharing data between classes"""

    _shared_state = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state

        self.store = {}
        for i in range(0, 6):
            self.store[f'img_{i}'] = {'name': None, 'path': None, 'ori': None, 'arr': None, 'extension': None}
            self.store[f'mask_{i}'] = {'pos': [], 'neg': [], 'data': None}
            self.store['img_dim'] = None

    def reset(self) -> None:
        for i in range(0, 6):
            if self.store[f'img_{i}']['path']:
                print(self.store[f'img_{i}']['path'])
                file_path = self.store[f'img_{i}']['path']
                os.remove(file_path)
            self.store[f'img_{i}'] = {'name': None, 'path': None, 'ori': None, 'arr': None, 'extension': None}
            self.store[f'mask_{i}'] = {'pos': [], 'neg': [], 'data': None}
            self.store['img_dim'] = None
