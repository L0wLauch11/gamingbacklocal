from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile

import paths


if __name__ == "__main__":
    ui_file = QFile(paths.MAIN_WINDOW)
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    
    # app needs to be initialized after loader
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    window = loader.load(ui_file, None)
    window.show()
    
    app.processEvents()
    app.exec()