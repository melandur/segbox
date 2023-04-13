import os

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Slot

from segbox.core import DataHandler
from segbox.gui.header import Header
from segbox.gui.toolbar import Toolbar


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application"""

    def __init__(self, app):
        super().__init__()

        self.num = [0]
        self.data_handler = DataHandler()
        self.header = Header(self, app)
        self.toolbar = Toolbar(self)
        self.init_layout()

    def init_layout(self):
        """Initialize the main window"""
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.h_box = QtWidgets.QHBoxLayout()
        self.h_box.setAlignment(QtCore.Qt.AlignLeft)

        self.init_buttons()
        self.h_box.addWidget(self.label)
        self.widget.setLayout(self.h_box)

    def init_buttons(self):
        """Initialize buttons"""
        self.label = QtWidgets.QLabel('No file selected')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(f'label_{self.num[-1]}')
        self.label.mousePressEvent = self.get_mouse_postion
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def open_file_dialog(self):
        """Open file dialog and add selected files to list"""
        sender = self.sender()
        sender_index = sender.objectName().split('_')[-1]
        print(sender.objectName(), sender_index)
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.nii *.nii.gz)')
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                self.data_handler(filenames[0], sender_index)
                self.auto()

    def auto(self):
        q_imgs = self.data_handler.get_qimgs()
        count_imgs = len(q_imgs)

        label = self.findChild(QtWidgets.QLabel, 'label_0')
        size = label.size()
        width = int(size.width() / count_imgs)
        height = int(size.height() / count_imgs)

        for index, q_img in enumerate(q_imgs.values()):
            label = self.findChild(QtWidgets.QLabel, f'label_{index}')
            label.setObjectName(f'label_{index}')
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.mousePressEvent = self.get_mouse_postion
            q_img = q_img.scaled(width, height, QtCore.Qt.KeepAspectRatio)
            q_pixmap = QtGui.QPixmap.fromImage(q_img)
            label.setPixmap(q_pixmap)
            self.h_box.addWidget(label)

    @Slot()
    def add_frame(self):
        if self.findChild(QtWidgets.QLabel, f'label_{self.num[-1]}').text() != 'No file selected':
            self.num.append(self.num[-1] + 1)
            label = QtWidgets.QLabel('No file selected')
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName(f'label_{self.num[-1]}')
            label.mousePressEvent = self.get_mouse_postion
            self.h_box.addWidget(label)
            self.btn_add.setObjectName(f'btn_add_{self.num[-1]}')

    @Slot()
    def remove_frame(self):
        if len(self.num) > 1:
            num = self.num[-1]
            label = self.findChild(QtWidgets.QLabel, f'label_{num}')
            if label:
                self.h_box.removeWidget(label)
                label.deleteLater()
            self.num.pop()
            self.data_handler.pop()
            self.btn_add.setObjectName(f'btn_add_{self.num[-1]}')

    def get_mouse_postion(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)


