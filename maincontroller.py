import sys
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
from ui_main import Ui_main as MyUi
import logic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.ui = MyUi()
        self.ui.setupUi(self)
        self.setMenuBar(self.ui.menubar)
        #QtWidgets.QMainWindow.__init__(self)
        # self.setupUi(self)

        self.navi = logic.Navigation()

        self.drawer = logic.Drawing(self.ui.centerArea)
        self.ui.centerBox.addWidget(self.drawer, 0, 1, 0, 1)

        self.btnssetup()  # connections setup


    def btnssetup(self):
        # top bar
        self.ui.PgBackBtn.clicked.connect(partial(self.navi.load_pic, self.ui.photolbl, False))
        self.ui.PgBackBtn.clicked.connect(partial(self.drawer.destroy, True))
        self.ui.PgBackBtn.setShortcut(QtGui.QKeySequence.MoveToPreviousChar)

        self.ui.PgNextBtn.clicked.connect(partial(self.navi.load_pic, self.ui.photolbl, True))
        self.ui.PgNextBtn.clicked.connect(partial(self.drawer.destroy, True))
        self.ui.PgNextBtn.setShortcut(QtGui.QKeySequence.MoveToNextChar)
        # temp load button
        self.ui.loadbtn.clicked.connect(partial(self.selectdirectory))

        # bottom bar
        self.ui.SaveBtn.setShortcut(QtGui.QKeySequence.MoveToNextLine)

    def selectdirectory(self):
        self.navi.load_folder()

        if len(self.navi.folder) > 0:
            self.navi.load_pic(self.ui.photolbl, 0)
            # self.ui.window.resize(self.photolbl.width() + 20, self.photolbl.height() + 100)
            # self.window.resize(self.photolbl.width() + 20, self.photolbl.height() + 100)
        else:
            self.selectdirectory()


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Create and show the window
    window = MainWindow()
    # window.resize(window.ui.DrawPnl.width() + 20,window.ui.DrawPnl.height() + 20)
    window.setWindowTitle("Activity Reference")
    # window.resize(window.width, window.height)

    window.show()

    sys.exit(app.exec_())
