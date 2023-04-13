import numpy as np
from loguru import logger
from PyQt5 import QtGui, QtWidgets


class ViewerUpdater(QtWidgets.QMainWindow):
    """Updates the viewers (qlabel) by setting the pixmap with data from the viewerstats"""

    def __init__(self, mw, core):
        super().__init__()
        self.mw = mw
        self.core = core

    @staticmethod
    def get_pixmap(viewer_stats):
        """Get pixmap from viewer stats"""
        return viewer_stats.pixmap_viewer

    @staticmethod
    def most_frequent(indexes):
        """Get most frequent index"""
        return max(set(indexes), key=indexes.count)

    @logger.catch
    def refresh_viewers(self):
        """Refresh all viewers"""
        if self.core.viewer_stats.viewer_1.linking:
            viewers_img_index = []
            if self.core.viewer_stats.viewer_1.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_1.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_1.img_index)

            if self.core.viewer_stats.viewer_2.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_2.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_2.img_index)

            if self.core.viewer_stats.viewer_3.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_3.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_3.img_index)

            if self.core.viewer_stats.viewer_4.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_4.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_4.img_index)

            if self.core.viewer_stats.viewer_5.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_5.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_5.img_index)

            if self.core.viewer_stats.viewer_6.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_6.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_6.img_index)

            if self.core.viewer_stats.viewer_7.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_7.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_7.img_index)

            if self.core.viewer_stats.viewer_8.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_8.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_8.img_index)

            try:
                most_frequent_index = self.most_frequent(viewers_img_index)
                viewers_img_index = [x for x in viewers_img_index if x != most_frequent_index][0]
                self.core.viewer_stats.viewer_1.img_index = viewers_img_index
                self.core.viewer_stats.viewer_2.img_index = viewers_img_index
                self.core.viewer_stats.viewer_3.img_index = viewers_img_index
                self.core.viewer_stats.viewer_4.img_index = viewers_img_index
                self.core.viewer_stats.viewer_5.img_index = viewers_img_index
                self.core.viewer_stats.viewer_6.img_index = viewers_img_index
                self.core.viewer_stats.viewer_7.img_index = viewers_img_index
                self.core.viewer_stats.viewer_8.img_index = viewers_img_index
            except:
                pass

        if self.core.viewer_stats.viewer_1.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_1)
        if self.core.viewer_stats.viewer_2.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_2)
        if self.core.viewer_stats.viewer_3.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_3)
        if self.core.viewer_stats.viewer_4.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_4)
        if self.core.viewer_stats.viewer_5.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_5)
        if self.core.viewer_stats.viewer_6.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_6)
        if self.core.viewer_stats.viewer_7.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_7)
        if self.core.viewer_stats.viewer_8.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_8)

    @logger.catch
    def refresh(self, viewer_stats):
        """Sets the modified pixel to the qlabel"""
        if not all(np.shape(viewer_stats.img_data)):
            viewer_stats.img_data = np.zeros((10, 10, 10), dtype=int)

        # img_base = self.opacity_adjuster(viewer_stats)
        # img_base = self.zoom_function(viewer_stats, img_base)
        # img_base = QtGui.QPixmap(img_base)
        # viewer_stats.qlabel_viewer.setPixmap(img_base)

        if viewer_stats.activated and viewer_stats.docked_widget is not None:
            viewer_stats.docked_widget.set_slice_number()
        elif not viewer_stats.activated and viewer_stats.docked_widget is not None:
            viewer_stats.docked_widget.set_slice_number(text='')
