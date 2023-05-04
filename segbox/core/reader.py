
import shutil
import os
from PIL import Image
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


from segbox.core.states import States


class Reader(States):
    def __init__(self, **kwargs) -> None:
        super().__init__()  # Borg pattern
        self._shared_state.update(kwargs)

    def __call__(self, data_folder) -> None or str:
        self.data_folder = data_folder

        for index, img_name in enumerate(self._state['imgs']):
            if self.get_img(index, 'local_path'):
                self._load_file(index)

        # for index, file in enumerate(files):
        #
        #     self._load_file(index, file_name, file_extension, file_path)

        # error = self._check_image_dimensions()
        # if error:
        #     self.reset()
        #     return error

    def _load_file(self, index) -> None:
        """Loads image and mask files into memory"""
        if self.get_img(index, 'extension').lower() in ('png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'):
            img = Image.open(self.get_img(index, 'local_path'))
            self.set_img(index, original=img)
            self.set_img(index, array=np.asarray(img))
            self._check_image_dimensions(index)
            shutil.copy(self.get_img(index, 'local_path'), os.path.join(self.data_folder, f'img_{index}_sl_0.png'))
        #
        # elif self.store[img_name]['extension'].lower() in ('nii', 'nii.gz'):
        #     img = nib.load(self.store[img_name]['local_path'])
        #     img = nib.as_closest_canonical(img)
        #     self.store[img_name]['ori'] = img
        #     self.store[img_name]['arr'] = img.get_fdata()
        #     self.extract_3d(img)

        else:
            raise ValueError(f'Unsupported file format -> {self.get_img(index, "extension")}')

    def _check_image_dimensions(self, index) -> None:
        """Checks if all images have the same dimensions"""
        if index == 0:
            self.set_gui(image_dimension=self.get_img(index, 'array').shape)
        else:
            test_shape = self.get_img(index, 'array').shape
            if self.get_gui('image_dimension') != test_shape:
                raise ValueError(f'Images have different dimensions -> {test_shape}')

    def extract_3d(self, arr_data):
        """Extracts 3D images from 4D images"""
        if arr_data is not None:
            if len(arr_data.shape) == 3:
                self._state.set_gui(image_slices=arr_data.shape[2])
                for slice in range(arr_data.shape[2]):
                    arr_slice = arr_data[:, :, slice].astype(np.float32)
                    new_file_path = os.path.join(self.data_folder, f'img_{index}_{slice}.png')
                    plt.imsave(new_file_path, arr_slice, cmap='gray')


if __name__ == '__main__':
    reader = Reader()
    reader('/home/melandur/Code/segbox/segbox/static/data')
