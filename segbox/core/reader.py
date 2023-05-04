
import shutil
import os
from PIL import Image
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import cv2


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

    def _load_file(self, index) -> None:
        """Loads image and mask files into memory"""
        if self.get_img(index, 'extension').lower() in ('png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'):
            self.set_gui(image_dim=2)
            img = Image.open(self.get_img(index, 'local_path'))
            self.set_img(index, original=img)
            arr_data = np.asarray(img)
            self.set_img(index, array=arr_data)
            self.set_array_slice(index, 0, arr_data)
            self._check_image_dimensions(arr_data)
            shutil.copy(self.get_img(index, 'local_path'), os.path.join(self.data_folder, f'img_{index}_sl_0.png'))

        elif self.get_img(index, 'extension').lower() in ('nii', 'nii.gz'):
            self.set_gui(image_dim=3)
            img = nib.load(self.get_img(index, 'local_path'))
            img = nib.as_closest_canonical(img)
            self.set_img(index, original=img)
            arr_data = img.get_fdata()
            self.set_img(index, array=arr_data)
            self._check_image_dimensions(arr_data)
            self.extract_3d(arr_data, index)

        else:
            raise ValueError(f'Unsupported file format -> {self.get_img(index, "extension")}')

    def _check_image_dimensions(self, arr_data) -> None:
        """Checks if all images have the same dimensions"""
        if self.get_gui('image_dimension') is None:
            self.set_gui(image_dimension=arr_data.shape)
        else:
            if self.get_gui('image_dimension') != arr_data.shape:
                raise ValueError(f'Images have different dimensions -> {arr_data.shape}')

    def extract_3d(self, arr_data, index):
        """Extracts 3D images from 4D images"""
        if arr_data is not None:
            if len(arr_data.shape) == 3:
                self.set_gui(image_slices=arr_data.shape[2])
                for slice in range(arr_data.shape[2]):
                    arr_slice = arr_data[:, :, slice].astype(np.float32)
                    new_file_path = os.path.join(self.data_folder, f'img_{index}_sl_{slice}.png')
                    norm_arr_slice = cv2.normalize(arr_slice, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    image = cv2.cvtColor(norm_arr_slice, cv2.COLOR_GRAY2RGB)
                    self.set_array_slice(index, slice, image)
                    plt.imsave(new_file_path, arr_slice, cmap='gray')


if __name__ == '__main__':
    reader = Reader()
    reader('/home/melandur/Code/segbox/segbox/static/data')
