
from PIL import Image
import nibabel as nib
import numpy as np
from pathlib import Path


class DataHandler:

    def __init__(self):
        self.store = {}
        self.file_extension = None
        self.latest_visited_folder = None

    def __call__(self, file_path) -> None:
        self.file_path = file_path
        file_name = Path(file_path).stem
        print(file_name)
        file_extension = ''.join(Path(file_path).suffixes)

        self._load_file(file_extension)
        self.latest_visited_folder = Path(file_path).parent

    def _load_file(self, file_extension) -> None:
        if file_extension.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'):
            img = Image.open(self.file_path)
            self.store['ori'] = img
            self.store['array'] = np.asarray(img)

        elif file_extension.lower() in ('.nii', '.nii.gz'):
            img = nib.load(self.file_path)
            self.store['ori'] = img
            self.store['array'] = img.get_fdata()

        else:
            raise ValueError('File type not supported')

    def get_array(self):
        return self.store['array']


