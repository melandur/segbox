from PyQt5 import QtWidgets

from segbox.gui.header import Header
from segbox.gui.toolbar import Toolbar
from segbox.gui.viewers import InitViewers, ViewerUpdater
from segbox.init_core import InitCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.core = InitCore(self.app)
        mw_viewers_updater = ViewerUpdater(self, self.core)
        self.mw_header = Header(self, self.core.user_specifications)
        self.mw_viewers = InitViewers(self, self.core, mw_viewers_updater)
        self.mw_toolbar = Toolbar(self)
