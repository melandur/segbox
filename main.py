import sys
from PySide6 import QtWidgets
from segbox.gui.main_window import MainWindow
import qdarktheme

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # qdarktheme.setup_theme("auto")
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())
