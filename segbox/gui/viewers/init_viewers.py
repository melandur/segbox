from PyQt5 import QtCore, QtWidgets

from segbox.core.utils import dirname, isdir, isfile
from segbox.gui.dialogs import pop_up_window
from segbox.gui.viewers.custom_view import (
    CustomQDockWidget,
    ViewerQLabel,
)


class InitViewers:
    """Initialize the viewers"""

    def __init__(self, mw, core, mw_viewers_updater):
        self.mw = mw
        self.core = core
        self.mw_viewers_updater = mw_viewers_updater
        self.case_path_presenter = None

        number_of_viewers = 4

        """Init 4 viewers"""
        if number_of_viewers == 4:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)

            # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            """Defines the order and orientation of 4 main viewers"""
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_3.docked_widget,
                self.core.viewer_stats.viewer_4.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

            """Init 6 viewers"""
        elif number_of_viewers == 6:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)

            # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            # Viewer 5
            self.core.viewer_stats.viewer_5.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_5,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_5.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_5,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_5.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_5.docked_widget.setWidget(self.core.viewer_stats.viewer_5.qlabel_viewer)

            # Viewer 6
            self.core.viewer_stats.viewer_6.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_6,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_6.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_6,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_6.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_6.docked_widget.setWidget(self.core.viewer_stats.viewer_6.qlabel_viewer)

            """Defines the order and orientation of 6 main viewers"""
            self.mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.core.viewer_stats.left_panel_widget)

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_2.docked_widget,
                self.core.viewer_stats.viewer_3.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_5.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_6.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_4.docked_widget,
                self.core.viewer_stats.viewer_5.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_5.docked_widget,
                self.core.viewer_stats.viewer_6.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

            """Init 8 viewer"""
        elif number_of_viewers == 8:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)

            # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            # Viewer 5
            self.core.viewer_stats.viewer_5.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_5,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_5.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_5,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_5.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_5.docked_widget.setWidget(self.core.viewer_stats.viewer_5.qlabel_viewer)

            # Viewer 6
            self.core.viewer_stats.viewer_6.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_6,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_6.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_6,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_6.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_6.docked_widget.setWidget(self.core.viewer_stats.viewer_6.qlabel_viewer)

            # Viewer 7
            self.core.viewer_stats.viewer_7.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_7,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_7.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_7,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_7.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_7.docked_widget.setWidget(self.core.viewer_stats.viewer_7.qlabel_viewer)

            # Viewer 8
            self.core.viewer_stats.viewer_8.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_8,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_8.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_8,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_8.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_8.docked_widget.setWidget(self.core.viewer_stats.viewer_8.qlabel_viewer)

            """Defines the order and orientation of 8 main viewers"""
            self.mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.core.viewer_stats.left_panel_widget)

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_2.docked_widget,
                self.core.viewer_stats.viewer_3.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_3.docked_widget,
                self.core.viewer_stats.viewer_4.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_5.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_6.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_7.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_8.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_5.docked_widget,
                self.core.viewer_stats.viewer_6.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_6.docked_widget,
                self.core.viewer_stats.viewer_7.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_7.docked_widget,
                self.core.viewer_stats.viewer_8.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

    def callback_drag_and_drop_with_viewer_update(self, data_path):
        """Allows drag and drop of a file or folder"""
        folder_path = None
        if isfile(data_path):
            folder_path = dirname(data_path)
        elif isdir(data_path):
            folder_path = data_path

        if folder_path:
            case_paths = self.core.folder_analyzer(folder_path)
            if len(case_paths.keys()) == 1:  # Assures that only one case is loaded
                self.case_path_presenter = CasePresenterWidget(case_paths, self.single_mode_callback)
                self.case_path_presenter.show()
                self.core.path_master.set_last_visited_folder(dirname(folder_path))
            else:
                text = 'The selected path contains to many options. \n Please try to be more specific'
                pop_up_window(text=text, entity='Information', errors='', details='')

    def single_mode_callback(self, case_paths):
        """Read and update viewer"""
        case_name = str(*case_paths)
        self.core.data_reader(case_name, case_paths)
        self.core.data_handler.copy_ephemeral_to_lasting_store()
        self.core.sync_viewers_stats.sync('native')
        self.mw_viewers_updater.refresh_viewers()

    def init_empty(self):
        """Init empty viewers, which will be loaded later on"""
