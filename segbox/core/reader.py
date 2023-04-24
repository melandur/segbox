import os
from PIL import Image
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread

from segbox.core.stats import Stats


class Reader(Stats):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._shared_state.update(kwargs)

    def __call__(self, static_files) -> None or str:
        self.static_files = static_files
        files = os.listdir(static_files)

        if len(files) > 6:
            self.reset()
            return 'Only 6 images are supported'

        for index, file in enumerate(files):
            file_name = file.split('.')[0]
            file_extension = '.'.join(file.split('.')[1:])
            file_path = os.path.join(static_files, file)
            self._load_file(index, file_name, file_extension, file_path)

        # error = self._check_image_dimensions()
        # if error:
        #     self.reset()
        #     return error

    def _load_file(self, index, file_name, file_extension, file_path) -> None:
        """Loads image and mask files into memory"""

        self.store[f'img_{index}']['name'] = file_name
        self.store[f'img_{index}']['path'] = file_path
        self.store[f'img_{index}'][f'extension'] = file_extension

        if file_extension.lower() in ('png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'):
            img = Image.open(file_path)
            self.store[f'img_{index}']['ori'] = img
            arr_data = np.asarray(img)
            self.store[f'img_{index}']['arr'] = arr_data
            self.store['img_dim'] = '2d'
            # self.extract_2d(arr_data, file_name)

        elif file_extension.lower() in ('nii', 'nii.gz'):
            img = nib.load(file_path)
            img = nib.as_closest_canonical(img)
            self.store[f'img_{index}']['ori'] = img
            arr_data = img.get_fdata()
            self.store[f'img_{index}']['arr'] = arr_data
            self.extract_3d(arr_data, file_name)
            self.store['img_dim'] = '3d'
        else:
            raise ValueError(f'Unsupported file format -> {file_extension}')

    def pop(self):
        last_key = list(self.store.keys())[-1]
        self.store.pop(last_key)

    # def _check_image_dimensions(self):
    #     dims = []
    #     for image in self.store:
    #         if 'img' in image:
    #             print(self.store[image]['arr'])
    #             if self.store[image]['arr'] is not None:
    #                 dims.append(self.store[image]['arr'].shape)
    #     if len(set(dims)) != 1:
    #         message = f'Images have different dimensions -> {dims}'
    #         return message

    def extract_2d(self, arr_data, file_name):
        file_path = os.path.join(self.static_files, 'img', file_name)
        os.makedirs(file_path, exist_ok=True)
        plt.imsave(os.path.join(file_path, f'{file_name}.png'), arr_data, cmap='gray')

    def extract_3d(self, arr_data, file_name):
        """Extracts 3D images from 4D images"""
        if arr_data is not None:
            if len(arr_data.shape) == 3:
                for slice in range(arr_data.shape[2]):
                    arr_slice = arr_data[:, :, slice].astype(np.float32)
                    # print(arr_slice.shape)
                    # im = Image.fromarray(arr_slice)

                    new_file_path = os.path.join(self.static_files, f'{file_name}_{slice}.png')
                    # print(new_file_path)

                    plt.imsave(new_file_path, arr_slice, cmap='gray')
                    # im.save(new_file_path)

                    # self.store[image]['arr'] = self.store[image]['arr'][:, :, :, 0]


if __name__ == '__main__':
    reader = Reader()
    reader('/home/melandur/Code/segbox/segbox/static/data')
