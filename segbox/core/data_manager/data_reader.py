import copy
import typing as t

import SimpleITK as sitk
from loguru import logger

from segbox.core.utils import basename, dirname, isdir, isfile


class DataReader:
    """Reads files from paths and assigns them to the data handler"""

    def __init__(self, data_handler: t.Any) -> None:
        self.data_handler = data_handler

    def __call__(self, case_name: str, case_paths: dict) -> None:
        logger.info(f'Run {self.__class__.__name__}')
        for modality, file_path in case_paths[case_name].items():
            self.read_data(file_path, modality)

    def read_data(self, path: str, modality_tag: str) -> None:
        """Check if image or dicom reader is needed"""
        if isfile(path):
            self.image_reader(path, modality_tag)
            logger.trace(f'Found {modality_tag} image file: {path}')
        if isdir(path):
            self.dicom_sequence_reader(path, modality_tag)
            logger.trace(f'Found {modality_tag} dicom file: {path}')

    def image_reader(self, path: str, modality_tag: str) -> None:
        """Reads data and meta data of image files"""
        self.data_handler.case_name = basename(dirname(path))
        reader = sitk.ImageFileReader()
        reader.SetFileName(path)
        reader.SetNumberOfThreads(8)
        reader.LoadPrivateTagsOn()
        reader.ReadImageInformation()

        if modality_tag != 'seg_mask':
            meta_data_dict = {}
            for key in reader.GetMetaDataKeys():
                if 'ITK_' in key:  # Don't know yet where this ITK_ tag comes from
                    continue
                meta_data_dict.update({key: reader.GetMetaData(key)})
            self.data_handler[f'{modality_tag}_ephemeral_meta'] = meta_data_dict

            img = reader.Execute()
            img = sitk.Cast(img, sitk.sitkFloat32)
            for key, value in meta_data_dict.items():
                img.SetMetaData(key, value)

            # Get original image direction of the cosine matrix and reorient the current image to LPS
            img_original_orientation = sitk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(
                img.GetDirection()
            )
            self.data_handler[f'{modality_tag}_ephemeral_image_orientation'] = img_original_orientation
            orient_filter = sitk.DICOMOrientImageFilter()
            orient_filter.SetDesiredCoordinateOrientation('LPS')
            img = orient_filter.Execute(img)
            self.data_handler[f'{modality_tag}_ephemeral_sitk'] = img
            self.data_handler.persistent[f'{modality_tag}_sitk'] = copy.deepcopy(img)
            self.data_handler[f'{modality_tag}_ephemeral_ndarray'] = sitk.GetArrayFromImage(img)
        else:
            seg = reader.Execute()
            seg = sitk.Cast(seg, sitk.sitkFloat32)
            orient_filter = sitk.DICOMOrientImageFilter()
            orient_filter.SetDesiredCoordinateOrientation('LPS')
            seg = orient_filter.Execute(seg)
            self.data_handler.persistent['seg_mask_sitk'] = copy.deepcopy(seg)

    def dicom_sequence_reader(self, path: str, modality_tag: str) -> None:
        """Reads data and meta data of dicom sequences"""
        if modality_tag != 'seg_mask':
            self.data_handler.case_name = basename(path)

            reader = sitk.ImageSeriesReader()
            series_ids = reader.GetGDCMSeriesIDs(path)
            dicom_names = reader.GetGDCMSeriesFileNames(path, series_ids[0])
            reader.SetFileNames(dicom_names)

            meta_data = sitk.ReadImage(dicom_names[0])
            meta_data_dict = {}
            logger.trace('read meta data')
            for key in meta_data.GetMetaDataKeys():
                if 'ITK_' in key:  # Don't know yet where this ITK_ tag comes from
                    continue
                logger.trace(f'{key} {meta_data.GetMetaData(key)}')
                meta_data_dict.update({key: meta_data.GetMetaData(key)})
            self.data_handler[f'{modality_tag}_ephemeral_meta'] = meta_data_dict
            # Get original image direction of the cosine matrix and reorient the current image to LPS
            img = reader.Execute()
            img = sitk.Cast(img, sitk.sitkFloat32)
            img_original_orientation = sitk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(
                img.GetDirection()
            )
            self.data_handler[f'{modality_tag}_ephemeral_image_orientation'] = img_original_orientation
            orient_filter = sitk.DICOMOrientImageFilter()
            orient_filter.SetDesiredCoordinateOrientation('LPS')
            img = orient_filter.Execute(img)
            self.data_handler[f'{modality_tag}_ephemeral_sitk'] = img
            self.data_handler[f'{modality_tag}_ephemeral_ndarray'] = sitk.GetArrayFromImage(img)
