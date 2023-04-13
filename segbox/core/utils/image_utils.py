from collections import OrderedDict

import numpy as np
import SimpleITK as sitk
from loguru import logger


def input_image_size_check(images=None):
    """Checks the input image size, crash avoidance"""
    if images:
        if not isinstance(images, list):
            raise TypeError('modalities is not a list')
    else:
        raise NotImplementedError

    for image in images:
        if image.GetSize() != (182, 218, 182):
            raise UserWarning(
                f'Expected data in MNI space with dims: (182, 218, 182)\n but '
                f'found: {image.GetSize()} (Register data first)'
            )


def extract_meta_data(image: sitk.Image) -> dict:
    """Extracts most important meta data from sitk objects"""
    return OrderedDict(
        {
            'origin': image.GetOrigin(),
            'spacing': image.GetSpacing(),
            'size': image.GetSize(),
            'direction': image.GetDirection(),
            'pixel_id_value': image.GetPixelIDValue(),
            'pixel_id': image.GetPixelID(),
            'pixel_id_as_string': image.GetPixelIDTypeAsString(),
        }
    )


def set_coordinate_orientation(image: sitk.Image, orientation: str) -> sitk.Image:
    """Set cosine orientation of itk image"""
    orient_filter = sitk.DICOMOrientImageFilter()
    orient_filter.SetDesiredCoordinateOrientation(orientation)
    return orient_filter.Execute(image)


def set_to_atlas_orientation(image: sitk.Image, atlas_path: str) -> sitk.Image:
    """Set cosine orientation of itk image to the atlas"""
    atlas = sitk.ReadImage(atlas_path)
    atlas_orientation = sitk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(atlas.GetDirection())
    orient_filter = sitk.DICOMOrientImageFilter()
    orient_filter.SetDesiredCoordinateOrientation(atlas_orientation)
    return orient_filter.Execute(image)


def check_dimensions(image, mask):
    """Check presence and spacing of images"""
    if image.GetDimension() != mask.GetDimension():
        text = f'Input dimensions mismatch:\nImages has {image.GetDimension()}\nSeg. mask has {mask.GetDimension()}'
        logger.warning(text)
        raise UserWarning(text)


def check_origin(image, mask):
    """Check presence and spacing of images"""
    diff = np.subtract(image.GetOrigin(), mask.GetOrigin())
    diff = diff[diff < 1e-2]
    if len(diff) != 3:
        text = f'Input image mismatch:\nImages has {image.GetOrigin()}\nSegmentation mask has {mask.GetOrigin()}'
        logger.warning(text)
        raise UserWarning(text)


if __name__ == '__main__':
    input_image_size_check([None])

    x = sitk.ReadImage(
        '/home/melandur/Data/Molab/molab_trainset_clean/cleaned/notgood/12OCT563662/12OCT563662_t1.nii.gz'
    )
    m = extract_meta_data(x)
    print(m)
