import os

import nibabel as nib
import numpy as np
from PIL import Image
from loguru import logger

from collections import OrderedDict
from qimage2ndarray import array2qimage

from segbox.core.configs.static_params import (
    SUPPORTED_DICOM_FILE_TYPES,
    SUPPORTED_MED_IMAGE_FILE_TYPES,
    SUPPORTED_IMAGE_FILE_TYPES,
)


class DataReader:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.file_name = None
        self.file_extension = None
        self.latest_visited_folder = None

    def __call__(self, file_path, sender_index) -> None:
        self.file_path = file_path
        self.sender_index = sender_index

        file = os.path.basename(file_path)
        folder = os.path.dirname(file_path)
        self.file_name = file.split('.')[0]
        self.file_extension = '.'.join(file.split('.')[1:])

        self._load_file()
        self.latest_visited_folder = folder

    def _load_file(self) -> None:
        logger.info(f'Loading image file -> {self.file_path}')
        self.data_handler[f'{self.sender_index}'] = OrderedDict()
        self.data_handler[f'{self.sender_index}'][f'{self.file_name}_extension'] = self.file_extension
        if self.file_extension.lower() in SUPPORTED_IMAGE_FILE_TYPES:
            img = Image.open(self.file_path)
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_img'] = img
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_array'] = np.asarray(img)
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_qimg'] = array2qimage(np.asarray(img))

        elif self.file_extension.lower() in SUPPORTED_DICOM_FILE_TYPES + SUPPORTED_MED_IMAGE_FILE_TYPES:
            img = nib.load(self.file_path)
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_img'] = img
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_array'] = img.get_fdata()
            self.data_handler[f'{self.sender_index}'][f'{self.file_name}_ori_qimg'] = array2qimage(img.get_fdata())

        else:
            raise ValueError(f'Unsupported file format -> {self.file_extension}')

    def get_qimgs(self):
        arrays = OrderedDict()
        for _, values in self.data_handler.items():
            for key, value in values.items():
                if key.endswith('_ori_qimg'):
                    arrays[key] = value
        return arrays

    def pop(self):
        last_key = list(self.data_handler.keys())[-1]
        self.data_handler.pop(last_key)
