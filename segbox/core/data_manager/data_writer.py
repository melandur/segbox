import typing as t

import SimpleITK as sitk
from loguru import logger

from segbox.core.utils import makedirs, path_join, set_coordinate_orientation


class DataWriter:
    """Writes data from lasting store to local space"""

    def __init__(self, data_handler: t.Any, config_file: dict, case_name: str) -> None:
        self.data_handler = data_handler
        self.config_file = config_file
        self.case_name = case_name
        self.params = config_file['data_writer']['params']
        self.lasting_store = self.data_handler.get_lasting_store()

    def __call__(self) -> None:
        logger.info(f'Run {self.__class__.__name__}')
        self._export_config_file()
        self._export_original()
        self._export_registration()
        self._export_skull_strip()
        self._export_segmentation()
        self._export_pyradiomics()
        self._export_mac_donald()

    def _create_folder_struct(
        self, key: str, folder_name: str, subfolder_name: str, set_file_name: str or None = None
    ) -> (str, str):
        """Creates export folder path for the writer methods. returns the paths and used methods"""
        if set_file_name:
            export_path = path_join(
                self.params['export_folder'], self.case_name, folder_name, subfolder_name, set_file_name
            )
        else:
            export_path = path_join(self.params['export_folder'], self.case_name, folder_name, subfolder_name)
        makedirs(export_path, exist_ok=True)
        modality = key.split('_')[0]
        return export_path, modality

    def _write_image(
        self,
        key: str,
        folder_name: str,
        subfolder_name: str,
        file_name: str or None = None,
        reorient: bool = False,
    ) -> None:
        """Write image data local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        if file_name is None:
            file_name = f'{self.case_name}_{modality}{self.params["export_file_extension"]}'
        else:
            file_name = f'{self.case_name}_{modality}_{file_name}{self.params["export_file_extension"]}'
        file_path = path_join(export_path, file_name)
        logger.trace(f'export {key} -> {file_path}')
        img = self.lasting_store[key]
        if reorient:
            orientation = self.data_handler.get_from_lasting_store(f'{modality}_native_image_orientation')
            img = set_coordinate_orientation(img, orientation)
        sitk.WriteImage(img, file_path)

    def _write_segmentation(
        self,
        key: str,
        folder_name: str,
        subfolder_name: str,
        mask_name: str,
        use_modalities: bool = True,
        reorient: bool = False,
    ) -> None:
        """Write image data local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        if use_modalities:
            file_name = f'{self.case_name}_{modality}_{mask_name}{self.params["export_file_extension"]}'
        else:
            file_name = f'{self.case_name}_{mask_name}{self.params["export_file_extension"]}'
        file_path = path_join(export_path, file_name)
        logger.trace(f'export {key} -> {file_path}')
        img = self.lasting_store[key]
        if reorient:
            orientation = self.data_handler.get_from_lasting_store('t1_native_image_orientation')
            img = set_coordinate_orientation(img, orientation)
        sitk.WriteImage(img, file_path)

    def _write_transformation(self, key: str, folder_name: str, subfolder_name: str) -> None:
        """Write transformation data  to local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        file_path = path_join(export_path, f'{self.case_name}_{modality}.tfm')
        logger.trace(f'export {key} -> {export_path}')
        sitk.WriteTransform(self.lasting_store[key], file_path)

    def _write_json_file(self, key: str, folder_name: str, subfolder_name: str, file_name: str) -> None:
        """Write json file to local storage"""
        export_path, _ = self._create_folder_struct(key, folder_name, subfolder_name)
        file_path = path_join(export_path, f'{file_name}.json')
        logger.trace(f'export {key} -> {export_path}')
        dump_json(self.lasting_store[key], file_path)

    def _export_config_file(self) -> None:
        """Export config file"""
        if self.config_file['data_writer']['save_config_file']:  # config file
            configs_path = path_join(self.params['export_folder'], self.case_name, 'configs')
            makedirs(configs_path, exist_ok=True)
            file_path = path_join(configs_path, 'config_file.json')
            logger.trace(f'export config_file -> {file_path}')
            dump_json(self.config_file, file_path)

    def _export_original(self) -> None:
        """Export original images"""
        config = self.config_file['data_writer']
        for key, value in self.lasting_store.items():  # image data
            if isinstance(value, sitk.Image):
                if '_native_' in key and 'brain' not in key and 'seg_mask' not in key and config['save_native_images']:
                    self._write_image(key, 'native', 'original_data', reorient=True)

    def _export_registration(self) -> None:
        """Export registration images"""
        config = self.config_file['registration']
        for key, value in self.lasting_store.items():  # image data
            if isinstance(value, sitk.Image):
                if '_registration_inverse_' in key and config['transform_to_native_space']:
                    self._write_image(key, 'native', 'inverse_transformed_data', reorient=True)

                elif '_registration_' in key:
                    self._write_image(key, 'atlas', 'registration')

            if isinstance(value, sitk.Transform):  # image transformation
                if '_transformation' in key:
                    self._write_transformation(key, 'native', 'transformation')

    def _export_skull_strip(self) -> None:
        """Export skull strip images"""
        config = self.config_file['skull_strip']
        for key, value in self.lasting_store.items():  # image data
            if isinstance(value, sitk.Image):
                if '_skull_strip_' in key:
                    if self.config_file['registration']['active']:
                        self._write_image(key, 'atlas', 'skull_strip', 'skull_strip')
                    else:
                        self._write_image(key, 'native', 'skull_strip', 'skull_strip', reorient=True)

                if 'brain_mask_atlas' in key and config['brain_mask']['save_atlas_space']:
                    if self.config_file['registration']['active']:
                        self._write_segmentation(key, 'atlas', 'skull_strip', 'brain_mask', False)
                    else:
                        self._write_segmentation(key, 'native', 'skull_strip', 'brain_mask', False, reorient=True)

                if 'brain_mask_native' in key and config['brain_mask']['save_native_space']:
                    self._write_segmentation(key, 'native', 'skull_strip', 'brain_mask', True, reorient=True)

    def _export_segmentation(self) -> None:
        """Export segmentation images"""
        config = self.config_file['segmentation']
        for key, value in self.lasting_store.items():  # image data
            if isinstance(value, sitk.Image):
                if 'seg_mask_native' in key and config['seg_mask']['save_native_space']:
                    self._write_segmentation(key, 'native', 'segmentation', 'seg_mask', True, reorient=True)

                if 'seg_mask_atlas' in key and config['seg_mask']['save_atlas_space']:
                    if self.config_file['registration']['active']:
                        self._write_segmentation(key, 'atlas', 'segmentation', 'seg_mask', False)
                    else:
                        self._write_segmentation(key, 'native', 'segmentation', 'seg_mask', False, reorient=True)

            if isinstance(value, dict) and 'seg_mask_measure_volumes' in key:
                folder_name = 'native'
                if self.config_file['registration']['active']:
                    folder_name = 'atlas'
                self._write_json_file(
                    key=key,
                    folder_name=folder_name,
                    subfolder_name='segmentation',
                    file_name='measured_volumes_in_mm3',
                )

    def _export_pyradiomics(self) -> None:
        """Export pyradiomics results"""
        for key, value in self.lasting_store.items():  # json file
            if 'pyradiomics' in key and value is not None:
                export_path, _ = self._create_folder_struct('', 'analytics', 'pyradiomics')
                if isinstance(value, dict):
                    self._write_json_file(
                        key=key,
                        folder_name='analytics',
                        subfolder_name='pyradiomics',
                        file_name=key.replace('_feature', ''),
                    )
                    feature = self.data_handler.get_from_lasting_store(key)
                    file_path = path_join(export_path, f'{key.replace("_feature", "")}.csv')
                    radiomicx_export_helper.export_csv(feature, file_path)

    def _export_mac_donald(self) -> None:
        """Export mac donald results, the base image gets rescaled and drawn by the helper function"""
        config = self.config_file['mac_donald']
        for key, value in self.lasting_store.items():  # json file
            if 'mac_donald' in key and value is not None:
                export_path, _ = self._create_folder_struct('', 'analytics', 'mac_donald')
                if isinstance(value, dict):
                    self._write_json_file(
                        key=key,
                        folder_name='analytics',
                        subfolder_name='mac_donald',
                        file_name='mac_donald',
                    )

                export_helper = MacDonald2DExportHelper(
                    self.data_handler.get_from_lasting_store('mac_donald_base_image'),
                    self.data_handler.get_from_lasting_store('mac_donald_longest_line'),
                    self.data_handler.get_from_lasting_store('mac_donald_longest_cross_line'),
                    self.data_handler.get_from_lasting_store('mac_donald_border_mask'),
                    config['params']['angle_tolerance'],
                )

                export_helper.save(folder_path=export_path, file_name='focus_1', crop_threshold=2)
                export_helper.save(folder_path=export_path, file_name='focus_2', crop_threshold=20)
                export_helper.save(folder_path=export_path, file_name='full_size', crop_threshold=None)
