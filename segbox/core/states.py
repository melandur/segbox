import os
import time
from collections import defaultdict
import typing as t

import matplotlib.pyplot as plt


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded"""

    def __init__(self, *args, **kwargs):
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


class States:
    """Borg pattern implementation for sharing data between classes"""

    _shared_state = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state

        self._state = None

    def init(self):
        """Initialize the state"""

        self._state = NestedDefaultDict({
            'imgs': NestedDefaultDict({}),
            'imgs_slices': NestedDefaultDict({}),
            'masks': NestedDefaultDict({}),

            'gui': {
                'image_names': [],
                'image_count': 0,
                'image_slice': 0,
                'image_slices': 0,
                'image_dim': None,
                'image_dimension': None,

                'mask_mode': 1,
                'mask_number': 0,
                'mask_name': {
                    'mask_0': 'name_0',
                    'mask_1': 'name_1',
                    'mask_2': 'name_2',
                    'mask_3': 'name_3',
                },
                'mask_iterations': {
                    'mask_0': 0,
                    'mask_1': 0,
                    'mask_2': 0,
                    'mask_3': 0,
                },
                'max_mask_iterations': {
                    'mask_0': 0,
                    'mask_1': 0,
                    'mask_2': 0,
                    'mask_3': 0,
                },

                'radius': 0,
                'color': 'SkyBlue',
                'time_stamp': time.time(),
                'viewer_width': 0,

            },
        })

        for i in range(0, 6):
            self._state['imgs'][f'img_{i}'] = {
                'name': None,
                'local_path': None,
                'original': None,
                'array': None,
                'array_slices': None,
                'extension': None,
            }

    def set_gui(self, **kwargs) -> None:
        for key in kwargs:
            if key not in self._state['gui']:
                raise KeyError(f'Key {key} not found in gui')

        self._state['gui'].update(kwargs)

    def get_gui(self, key) -> t.Any:
        if key not in self._state['gui']:
            raise KeyError(f'Key {key} not found in gui')
        return self._state['gui'].get(key, None)

    def set_array_slice(self, img_number, sl_index, array_slice) -> None:
        self._state['imgs'][f'img_{img_number}'][f'sl_{sl_index}'] = array_slice

    def get_array_slice(self, img_number, sl_index) -> t.Any:
        return self._state['imgs'][f'img_{img_number}'][f'sl_{sl_index}']

    def set_img(self, img_number: int, **kwargs) -> None:
        for key in kwargs:
            if key not in self._state['imgs'][f'img_{img_number}']:
                raise KeyError(f'Key {key} not found in img_{img_number}')

        self._state['imgs'][f'img_{img_number}'].update(kwargs)
        self.set_gui(image_count=img_number + 1)

    def get_img(self, img_number: int, key: str) -> t.Any:
        if key not in self._state['imgs'][f'img_{img_number}']:
            raise KeyError(f'Key {key} not found in img_{img_number}')

        return self._state['imgs'][f'img_{img_number}'].get(key, None)

    def add_mask_iteration(self) -> None:
        slice_number = self.get_gui('image_slice')
        mask_number = self.get_gui('mask_number')
        mask_iteration, _ = self.get_mask_iteration()
        mask_iteration += 1
        self.set_mask_iteration(mask_iteration)

        if mask_iteration <= 1:
            self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}'] = {'points': [], 'labels': [], 'mask': None, 'logits': None}
        else:
            self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}'] = self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration-1}'][f'sl_{slice_number}']

    def get_mask_iteration(self, mask_number: int = None) -> tuple:
        if mask_number is None:
            mask_number = self.get_gui('mask_number')
        mask_iterations = self.get_gui('mask_iterations')
        max_mask_iterations = self.get_gui('max_mask_iterations')
        return mask_iterations[f'mask_{mask_number}'], max_mask_iterations[f'mask_{mask_number}']

    def set_mask_iteration(self, iteration) -> None:
        mask_number = self.get_gui('mask_number')
        self._state['gui']['mask_iterations'][f'mask_{mask_number}'] = iteration
        if iteration > self._state['gui']['max_mask_iterations'][f'mask_{mask_number}']:
            self._state['gui']['max_mask_iterations'][f'mask_{mask_number}'] = iteration

    def get_mask_name(self, mask_number: int = 0) -> str:
        return self._state['gui']['mask_name'][f'mask_{mask_number}']

    def set_mask_name(self, mask_number: int, name: str) -> None:
        self._state['gui']['mask_name'][f'mask_{mask_number}'] = name

    def get_mask(self, key: str) -> t.Any:
        mask_number = self.get_gui('mask_number')
        mask_iteration, _ = self.get_mask_iteration()
        slice_number = self.get_gui('image_slice')

        if key not in self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}']:
            raise KeyError(f'Key {key} not found in mask_{mask_number}')

        return self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}'].get(key, None)

    def set_mask(self, **kwargs) -> None:
        mask_number = self.get_gui('mask_number')
        mask_iteration, _ = self.get_mask_iteration()
        slice_number = self.get_gui('image_slice')

        for key in kwargs:
            if key not in self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}']:
                raise KeyError(f'Key {key} not found in mask_{mask_number}')

        self._state['masks'][f'mask_{mask_number}'][f'it_{mask_iteration}'][f'sl_{slice_number}'].update(kwargs)

    def add_image(self, index, path):
        self.set_img(index, local_path=path)
        self.set_img(index, name=os.path.basename(path).split('.')[0])
        self.set_img(index, extension='.'.join(path.split('.')[1:]))
        self.calculate_viewer_width()

    def calculate_viewer_width(self):
        """Get the specs for the viewers"""
        width = 0
        image_count = self.get_gui('image_count')
        if image_count:
            if image_count > 3:
                width = int(95 / 3)  # 95% of the screen
            else:
                width = int(95 / image_count)
        self.set_gui(viewer_width=width)

    def reset_mask(self):
        self.set_mask_iteration(-1)
        self.add_mask_iteration()

    def save_tmp_mask(self, mask_folder):
        mask = self.get_mask('mask')
        mask_number = self.get_gui('mask_number')
        slice_number = self.get_gui('image_slice')
        iteration, _ = self.get_mask_iteration()

        plt.imsave(
            os.path.join(mask_folder, f'mask_{mask_number}_it_{iteration}_sl_{slice_number}.png'),
            mask,
            cmap='gray'
        )


if __name__ == '__main__':
    s = States()
    s.set_gui(image_count=2)
    s.add_image(0, 'test')

    # def assign_masks(self, total, slices, iterations):
    #     for i in range(0, total):
    #         for j in range(0, slices):
    #             for k in range(0, iterations):
    #                 [f'mask_{i}']['slice_{j}'][''] = {'points': [], 'labels': [], 'mask': None, 'logits': None}
    #             #     'points': [],
    #             #     'labels': [],
    #             #     'mask': None,
    #             #     'logits': None
    #             # }

    # def get_stats(self) -> dict:
    #     return self.store
    #
    # def pop_mask(self) -> None:
    #     last_key = list(self.store.keys())[-1]
    #     self.store.pop(last_key)
    #
    # def reset(self) -> None:
    #     for i in range(0, 6):
    #         self.store[f'img_{i}'] = {'name': None, 'local_path': None, 'ori': None, 'arr': None, 'extension': None}
    #         self.store[f'mask_{i}'] = {'points': [], 'labels': [], 'mask': None, 'logits': None}
    #         self.store['dim'] = None
    #
    # def reset_mask(self, mask_number: int) -> None:
    #     self.store[f'mask_{mask_number}'] = {'points': [], 'labels': [], 'mask': None, 'logits': None}
    #
