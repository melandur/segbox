from loguru import logger
from PyQt5 import QtCore, QtWidgets


class ViewerQLabel(QtWidgets.QLabel):
    """Viewer main window"""

    def __init__(self, viewer_stats, cb_update_viewers, cb_scroll):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False)
        # self.setStyleSheet('QLabel {background : black;}')
        self.setMinimumSize(100, 100)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        self.viewer_stats = viewer_stats
        self.cb_update_viewers = cb_update_viewers
        self.cb_scroll = cb_scroll

    @QtCore.pyqtSlot()
    def zoom(self, delta, pos):
        self.viewer_stats.zoom_factor -= delta
        self.viewer_stats.zoom_pos = (pos.x(), pos.y())

    @QtCore.pyqtSlot()
    def resizeEvent(self, event):
        self.cb_update_viewers()
        event.accept()

    @logger.catch()
    @QtCore.pyqtSlot()
    def wheelEvent(self, event) -> None:
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        delta = event.angleDelta()
        delta = int(QtCore.QPoint.y(delta) / 120)
        if delta == 0:
            pass
        else:
            if modifiers == QtCore.Qt.ShiftModifier:
                if self.viewer_stats.img_opacity is not None and self.viewer_stats.img_data is not None:
                    min_scroll_value = 0
                    max_scroll_value = 100
                    delta *= 10
                    if max_scroll_value >= self.viewer_stats.img_opacity + delta >= min_scroll_value:
                        self.viewer_stats.img_opacity += delta
                        self.cb_update_viewers()
            else:
                if self.viewer_stats.img_index is not None and self.viewer_stats.img_data is not None:
                    if (
                        self.viewer_stats.img_index_max
                        > self.viewer_stats.img_index - delta
                        >= self.viewer_stats.img_index_min
                    ):
                        self.viewer_stats.img_index -= delta
                        self.cb_scroll()
                        self.cb_update_viewers()
        event.accept()


class CustomQDockWidget(QtWidgets.QDockWidget):
    """Dock widgets are used for structuring the main window"""

    def __init__(self, viewer_stats, cb_update_viewers, cb_drag_and_drop, cb_qlabel_viewer):
        super().__init__()
        self.viewer_stats = viewer_stats
        self.cb_update_viewers = cb_update_viewers
        self.cb_drag_and_drop = cb_drag_and_drop
        self.cb_qlabel_viewer = cb_qlabel_viewer

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)  # prevents closing and undocking

        self.setFloating(False)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)

        # Title bar settings
        self.title_label = QtWidgets.QLabel('', self)
        self.slice_number = QtWidgets.QLabel('', self)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.slice_number)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        widget.setLayout(layout)
        layout.setSpacing(0)
        self.setTitleBarWidget(widget)

    @QtCore.pyqtSlot()
    def set_title(self, title):
        self.title_label.setText(title)

    @QtCore.pyqtSlot()
    def set_slice_number(self, text=None):
        if text is not None:
            self.slice_number.setText(str(text))
        else:
            self.slice_number.setText(f'{self.viewer_stats.img_index + 1}/{self.viewer_stats.img_index_max}')

    @QtCore.pyqtSlot()
    def set_title_float_widget(self):
        if self.viewer_stats.title:
            self.viewer_stats.float_widget.setWindowTitle(self.viewer_stats.title)
        else:
            self.viewer_stats.float_widget.setWindowTitle('')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            first_url = event.mimeData().urls()[0]
            data_path = str(first_url.toLocalFile())
            self.cb_drag_and_drop(data_path)
            self.cb_update_viewers()
        else:
            event.ignore()


# class CustomQStackedWidgetSlim(QtWidgets.QStackedWidget):
#     """Reduced version, used for the smart segmentation editor"""
#
#     def __init__(self, viewer_stats, cb_update_viewer):
#         super().__init__()
#         self.viewer_stats = viewer_stats
#         self.cb_update_viewer = cb_update_viewer
#
#         self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#         self.setAcceptDrops(True)


# class CustomQStackedWidget(QtWidgets.QStackedWidget):
#     """Are used when the dock widget are undocked"""
#
#     def __init__(self, viewer_stats, cb_update_viewers, cb_drag_and_drop):
#         super().__init__()
#         self.cb_update_viewers = cb_update_viewers
#         self.viewer_stats = viewer_stats
#         self.cb_drag_and_drop = cb_drag_and_drop
#
#         self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#         self.setAcceptDrops(True)
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls:
#             event.accept()
#         else:
#             event.ignore()
#
#     def dragMoveEvent(self, event):
#         if event.mimeData().hasUrls:
#             event.accept()
#         else:
#             event.ignore()
#
#     def dropEvent(self, event):
#         if event.mimeData().hasUrls:
#             event.accept()
#             first_url = event.mimeData().urls()[0]
#             data_path = str(first_url.toLocalFile())
#             self.cb_drag_and_drop(data_path)
#             self.cb_update_viewers()
#         else:
#             event.ignore()
#
#     @QtCore.Slot()
#     def closeEvent(self, event):
#         self.viewer_stats.docked_widget.setFloating(False)
#         self.viewer_stats.docked_widget.show()
#         self.viewer_stats.docked_widget.setWidget(self.viewer_stats.qlabel_viewer)
#         self.viewer_stats.float_widget.hide()


# class CustomSidePanelQTabWidget(QtWidgets.QTabWidget):
#     """For structuring each mri modality in a own tab"""
#
#     def __init__(self):
#         super().__init__()
#         self.tab_layout = QtWidgets.QGridLayout()
#         self.setLayout(self.tab_layout)
#         self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
#         self.setFocusPolicy(QtCore.Qt.NoFocus)


# class CustomSidePanelQTableWidget(QtWidgets.QTableWidget):
#     """Table widget to structuring meta data"""
#
#     def __init__(self):
#         super().__init__()
#         self.verticalHeader().setVisible(False)
#         self.horizontalHeader().setVisible(False)
#         self.setColumnCount(2)
#         self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
#         # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
#         self.setFocusPolicy(QtCore.Qt.NoFocus)
