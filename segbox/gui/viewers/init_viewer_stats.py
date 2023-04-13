from loguru import logger

from segbox.gui.viewers.viewer_stats import ViewerStats


class InitViewerStats:
    def __init__(self):
        logger.info(f'Init {self.__class__.__name__}')

        # Init viewer stats for main viewer windows
        self.viewer_1 = ViewerStats()
        self.viewer_2 = ViewerStats()
        self.viewer_3 = ViewerStats()
        self.viewer_4 = ViewerStats()
        self.viewer_5 = ViewerStats()
        self.viewer_6 = ViewerStats()
        self.viewer_7 = ViewerStats()
        self.viewer_8 = ViewerStats()
