from PySide6 import QtCore, QtWidgets


class Toolbar(QtWidgets.QMainWindow):
    """Toolbar interface, which holds the buttons for single mode"""

    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self.toolbar = QtWidgets.QToolBar('Toolbar', mw)
        self.toolbar.setMovable(False)

        mw.btn_add = QtWidgets.QPushButton('Load files ...')
        mw.btn_add.setObjectName(f'btn_add_{mw.num[-1]}')
        mw.btn_add.clicked.connect(mw.open_file_dialog)

        spacer = QtWidgets.QWidget()
        spacer.setStyleSheet('background: None;')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.add_frame = QtWidgets.QPushButton('+')
        self.add_frame.clicked.connect(mw.add_frame)

        self.remove_frame = QtWidgets.QPushButton('-')
        self.remove_frame.clicked.connect(mw.remove_frame)

        mw.btn_add.setFixedWidth(100)
        self.add_frame.setFixedWidth(30)
        self.remove_frame.setFixedWidth(30)

        self.toolbar.addWidget(mw.btn_add)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.add_frame)
        self.toolbar.addWidget(self.remove_frame)

        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        mw.addToolBar(self.toolbar)
