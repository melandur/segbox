from PySide6 import QtCore, QtWidgets, QtGui
import qimage2ndarray
from segbox.core import DataHandler
from segbox.gui.header import Header
import os


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application"""

    def __init__(self, app):
        super().__init__()

        self.data_handler = DataHandler()

        self.header = Header(self, app)

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        v_box = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        h_box.setAlignment(QtCore.Qt.AlignLeft)

        # variables
        self.pix = QtWidgets.QLabel('No file selected')
        self.pix.setAlignment(QtCore.Qt.AlignCenter)
        self.pix.mousePressEvent = self.get_mouse_postion

        # file browser button
        file_browser_btn = QtWidgets.QPushButton('Load files ...')
        file_browser_btn1 = QtWidgets.QPushButton('Load files ...')

        file_browser_btn.setFixedWidth(150)
        file_browser_btn1.setFixedWidth(150)

        file_browser_btn.clicked.connect(self.open_file_dialog)

        # add widgets to layout
        h_box.addWidget(file_browser_btn)
        h_box.addWidget(file_browser_btn1)
        v_box.addLayout(h_box)
        v_box.addWidget(self.pix)
        self.widget.setLayout(v_box)

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

                # convert numpy array to QImage
                q_img = qimage2ndarray.array2qimage(img_arr)
                q_pix = QtGui.QPixmap.fromImage(q_img)
                q_pix = q_pix.scaled(
                    int(self.header.width * 0.6),
                    int(self.header.height * 0.6),
                    QtCore.Qt.KeepAspectRatio,
                )
                self.pix.setPixmap(q_pix)

    def get_mouse_postion(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)

