from loguru import logger
from PyQt5 import QtCore

from segbox.core.data_manager import DataHandler, DataReader
from segbox.core.user import UserSpecsDetector
from segbox.gui.viewers import InitViewerStats, SyncViewerStats


class InitCore:
    """Initializes core classes before the gui"""

    def __init__(self, app: QtCore.QCoreApplication):
        self.app = app
        logger.info('Init Backend')

        self.data_handler = DataHandler()
        self.data_reader = DataReader(self.data_handler)

        self.config_file_handler = None
        self.user_specifications = None
        self.folder_analyzer = None
        self.viewer_stats = None
        self.meta_data_updater = None
        self.sync_viewers_stats = None

        self.cb_update_core()

    def cb_update_core(self):
        """Update core, which assures that the current user settings are used, no restart needed"""
        self.user_specifications = UserSpecsDetector(self.app)

        self.viewer_stats = InitViewerStats()
        self.sync_viewers_stats = SyncViewerStats(
            self.data_handler,
            self.config_file_handler,
            self.viewer_stats,
            self.meta_data_updater,
        )
