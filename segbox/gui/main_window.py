from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
import qimage2ndarray
from segbox.core import DataHandler
from segbox.gui.header import Header
import os


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application"""

    def __init__(self, app):
        super().__init__()

        self.num = [0]
        self.data_handler = DataHandler()
        self.header = Header(self, app)
        self.init_layout()

    def init_layout(self):
        """Initialize the main window"""
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        v_box = QtWidgets.QVBoxLayout()
        self.h_box = QtWidgets.QHBoxLayout()
        self.h_box.setAlignment(QtCore.Qt.AlignLeft)

        self.init_buttons()

        self.h_box.addWidget(self.btn_add)

        v_box.addLayout(self.h_box)
        v_box.addWidget(self.pix)
        self.widget.setLayout(v_box)

    def init_buttons(self):
        """Initialize buttons"""
        self.pix = QtWidgets.QLabel('No file selected')
        self.pix.setAlignment(QtCore.Qt.AlignCenter)
        self.pix.mousePressEvent = self.get_mouse_postion

        self.btn_add = QtWidgets.QPushButton('Load files ...')
        self.btn_add.setObjectName(f'btn_add_{self.num[-1]}')

        self.btn_add.setFixedWidth(100)

        self.btn_add.clicked.connect(self.add_frame)

    def open_file_dialog(self):
        """Open file dialog and add selected files to list"""
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.nii *.nii.gz)')
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if len(filenames) == 1:
                self.data_handler(filenames[0])
                img_arr = self.data_handler.get_array()

                q_img = qimage2ndarray.array2qimage(img_arr)
                q_pix = QtGui.QPixmap.fromImage(q_img)
                q_pix = self.resize_image(q_pix)

                self.pix.setPixmap(q_pix)

    def resize_image(self, q_pix):
        """Resize image to fit in the window"""
        return q_pix.scaled(int(self.header.width * 0.6), int(self.header.height * 0.6), QtCore.Qt.KeepAspectRatio)

    @Slot()
    def add_frame(self):
        self.num.append(self.num[-1] + 1)
        print(self.num)
        btn_add = QtWidgets.QPushButton('Load file...', self)
        btn_remove = QtWidgets.QPushButton('Remove', self)
        btn_add.setObjectName(f'btn_add_{self.num[-1]}')
        btn_remove.setObjectName(f'btn_remove_{self.num[-1]}')
        btn_add.clicked.connect(self.add_frame)
        btn_remove.clicked.connect(self.remove_frame)
        self.h_box.addWidget(btn_add)
        self.h_box.addWidget(btn_remove)

    @Slot()
    def remove_frame(self):
        print(self.num)
        if len(self.num) >= 2:
            num = self.num[-1]

            btn_add = self.findChild(QtWidgets.QPushButton, f'btn_add_{num}')
            btn_remove = self.findChild(QtWidgets.QPushButton, f'btn_remove_{num}')
            if btn_add:
                self.h_box.removeWidget(btn_add)
                btn_add.deleteLater()
            if btn_remove:
                self.h_box.removeWidget(btn_remove)
                btn_remove.deleteLater()
            self.num.pop()

    def get_mouse_postion(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)

