from PySide6 import QtCore, QtWidgets


from segbox.gui.header import Header
from pathlib import Path
import os


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application"""

    def __init__(self, app):
        super().__init__()

        self.mw_header = Header(self, app)

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        v_box = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        h_box.setAlignment(QtCore.Qt.AlignLeft)

        # variables
        self.file_list = QtWidgets.QListWidget(self)

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
        # v_box.addStretch()
        v_box.addWidget(self.file_list)

        self.widget.setLayout(v_box)

    # def

    def open_file_dialog(self):
        """Open file dialog and add selected files to list"""
        dialog = QtWidgets.QFileDialog(self)
        # get user directory
        dialog.setDirectory(os.path.expanduser('~'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter('Images (*.png *.jpg, *.jpeg, *.bmp, *.tif, *.tiff)')
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.file_list.addItems([str(Path(filename)) for filename in filenames])
