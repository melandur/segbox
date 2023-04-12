from PySide6 import QtGui, QtWidgets, QtCore


class Header(QtWidgets.QMainWindow):
    """Defines Software header with title name and icon"""

    def __init__(self, mw, app):
        super().__init__()
        mw.setWindowTitle('SegBox')

        screen = app.primaryScreen()
        self.width = int(QtCore.QRect.width(screen.availableGeometry()))
        self.height = int(QtCore.QRect.height(screen.availableGeometry()))
        mw.setGeometry(self.width / 6, self.height / 8, self.width / 1.7, self.height / 1.3)  # define main window size

        # self.icon = QtGui.QIcon(APP_ICON)
        # mw.setWindowIcon(self.icon)