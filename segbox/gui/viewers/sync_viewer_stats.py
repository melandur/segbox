import numpy as np
import SimpleITK as sitk
from loguru import logger


def sitk_to_ndarray_image_preprocessed(sitk_image):
    """Orient to LPS, Rescale intensities and convert to ndarray"""
    if sitk_image is not None:
        orient_filter = sitk.DICOMOrientImageFilter()
        orient_filter.SetDesiredCoordinateOrientation('LPS')
        sitk_image = orient_filter.Execute(sitk_image)
        sitk_image = sitk.RescaleIntensity(sitk_image)
        return sitk.GetArrayFromImage(sitk_image)
    return None


class SyncViewerStats:
    """Update viewer stats with the latest image data from the data handler"""

    def __init__(self, data_handler, config_file_handler, viewer_stats, meta_data_updater):
        self.data_handler = data_handler
        self.config_file_handler = config_file_handler
        self.viewer_stats = viewer_stats
        self.meta_data_updater = meta_data_updater
        # self.used_modality_names = copy.deepcopy(USED_MODALITY_NAMES)
        # if 'seg_mask' in USED_MODALITY_NAMES:
        #     self.used_modality_names.remove('seg_mask')
        logger.info('Init Data Base to Viewer Stats')

    @logger.catch
    def sync(self, state):
        """ "Update the viewer stats with the current ephemeral output"""
        if state != 'segmentation':
            self.meta_data_updater.show_meta_data(state)

        seg_mask_ndarray = self.data_handler.get_segmentation_mask(extension='ndarray')
        if state in ('registration', 'skull_strip'):
            seg_mask_ndarray = None

        if self.viewer_stats.viewer_1.qlabel_viewer is not None:
            modality_name = ''
            # if 0 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[0]
            self.viewer_stats.viewer_1.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_1.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_1.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_2.qlabel_viewer is not None:
            modality_name = ''
            # if 1 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[1]
            self.viewer_stats.viewer_2.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_2.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_2.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_3.qlabel_viewer is not None:
            modality_name = ''
            # if 2 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[2]
            self.viewer_stats.viewer_3.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_3.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_3.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_4.qlabel_viewer is not None:
            modality_name = ''
            # if 3 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[3]
            self.viewer_stats.viewer_4.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_4.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_4.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_5.qlabel_viewer is not None:
            modality_name = ''
            # if 4 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[4]
            self.viewer_stats.viewer_5.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_5.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_5.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_6.qlabel_viewer is not None:
            modality_name = ''
            # if 5 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[5]
            self.viewer_stats.viewer_6.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_6.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_6.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_7.qlabel_viewer is not None:
            modality_name = ''
            # if 6 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[6]
            self.viewer_stats.viewer_7.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_7.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_7.seg_data = seg_mask_ndarray

        if self.viewer_stats.viewer_8.qlabel_viewer is not None:
            modality_name = ''
            # if 7 < len(self.used_modality_names):
            #     modality_name = self.used_modality_names[7]
            self.viewer_stats.viewer_8.title = modality_name.capitalize()
            if state != 'segmentation' and modality_name != '':
                img = self.data_handler.get_from_lasting_store(f'{modality_name}_{state}_sitk')
                self.viewer_stats.viewer_8.load(
                    img_data=sitk_to_ndarray_image_preprocessed(img),
                    title=modality_name.capitalize(),
                    orientation='transverse',
                    linking=True,
                    activated=True,
                )
            self.viewer_stats.viewer_8.seg_data = seg_mask_ndarray

        viewers_img_index = []
        if self.viewer_stats.viewer_1.qlabel_viewer is not None:
            if self.viewer_stats.viewer_1.activated:
                viewers_img_index.append(self.viewer_stats.viewer_1.img_index)
        if self.viewer_stats.viewer_2.qlabel_viewer is not None:
            if self.viewer_stats.viewer_2.activated:
                viewers_img_index.append(self.viewer_stats.viewer_2.img_index)
        if self.viewer_stats.viewer_3.qlabel_viewer is not None:
            if self.viewer_stats.viewer_3.activated:
                viewers_img_index.append(self.viewer_stats.viewer_3.img_index)
        if self.viewer_stats.viewer_4.qlabel_viewer is not None:
            if self.viewer_stats.viewer_4.activated:
                viewers_img_index.append(self.viewer_stats.viewer_4.img_index)
        if self.viewer_stats.viewer_5.qlabel_viewer is not None:
            if self.viewer_stats.viewer_5.activated:
                viewers_img_index.append(self.viewer_stats.viewer_5.img_index)
        if self.viewer_stats.viewer_6.qlabel_viewer is not None:
            if self.viewer_stats.viewer_6.activated:
                viewers_img_index.append(self.viewer_stats.viewer_6.img_index)
        if self.viewer_stats.viewer_7.qlabel_viewer is not None:
            if self.viewer_stats.viewer_7.activated:
                viewers_img_index.append(self.viewer_stats.viewer_7.img_index)
        if self.viewer_stats.viewer_8.qlabel_viewer is not None:
            if self.viewer_stats.viewer_8.activated:
                viewers_img_index.append(self.viewer_stats.viewer_8.img_index)

        try:
            viewers_img_index = np.asarray(viewers_img_index)
            if viewers_img_index.size != 0:  # Check for zero size arrays
                min_index = np.min(viewers_img_index[np.nonzero(viewers_img_index)])
                self.viewer_stats.viewer_1.img_index = min_index
                self.viewer_stats.viewer_2.img_index = min_index
                self.viewer_stats.viewer_3.img_index = min_index
                self.viewer_stats.viewer_4.img_index = min_index
                self.viewer_stats.viewer_5.img_index = min_index
                self.viewer_stats.viewer_6.img_index = min_index
                self.viewer_stats.viewer_7.img_index = min_index
                self.viewer_stats.viewer_8.img_index = min_index
        except:
            logger.debug('Scroll error caused by sync min index')
