import os

from PyQt5 import QtCore, QtWidgets


class Toolbar(QtWidgets.QMainWindow):
    """Toolbar interface, which holds the buttons for single mode"""

    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self.toolbar = QtWidgets.QToolBar('Toolbar', mw)
        self.toolbar.setMovable(False)

        mw.btn_add = QtWidgets.QPushButton('Load files ...')
        mw.btn_add.setObjectName(f'btn_add_')
        mw.btn_add.clicked.connect(self.folder_load_dialog)

        spacer = QtWidgets.QWidget()
        spacer.setStyleSheet('background: None;')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.add_frame = QtWidgets.QPushButton('+')
        # self.add_frame.clicked.connect(mw.add_frame)

        self.remove_frame = QtWidgets.QPushButton('-')
        # self.remove_frame.clicked.connect(mw.remove_frame)

        mw.btn_add.setFixedWidth(100)
        self.add_frame.setFixedWidth(30)
        self.remove_frame.setFixedWidth(30)

        self.toolbar.addWidget(mw.btn_add)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.add_frame)
        self.toolbar.addWidget(self.remove_frame)

        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        mw.addToolBar(self.toolbar)

    def folder_load_dialog(self):
        """Opens dialog window on last visited folder, stores updated last visited folder"""
        sender = self.sender()
        sender_index = sender.objectName().split('_')[-1]
        dialog = QtWidgets.QFileDialog()
        dialog.setDirectory(os.path.expanduser('~'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.nii *.nii.gz)')
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.resize(QtCore.QSize(800, 600))
        dialog.move(QtWidgets.QDesktopWidget().availableGeometry().center() - dialog.frameGeometry().center())
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                return True, filenames[0]
            return False, None
        return False, None


# From here on the icons are on the right side of the toolbar
# spacer = QtWidgets.QWidget()
# spacer.setStyleSheet('background: None;')
# spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
# self.toolbar.addWidget(spacer)
