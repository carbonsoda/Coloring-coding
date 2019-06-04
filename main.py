import sys
from PySide2 import QtWidgets, QtGui
from functools import partial
import ctypes
from ui_main import Ui_main as MyUi
import logic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.ui = MyUi()
        self.ui.setupUi(self)
        self.setMenuBar(self.ui.menubar)

        self.navi = logic.Navigation()
        # self.drawer = logic.Drawing(self.ui.centerArea)
        self.drawer = logic.Drawing(self.ui.centerArea)
        self.ui.centerBox.addWidget(self.drawer, 0, 1, 0, 1)

        # self.ui.ObjName.textChanged.connect(self.naming)
        self.ui.ObjName.textChanged.connect(lambda : self.ui.ObjName.text())
        self.btnssetup()  # connections setup

    def btnssetup(self):
        self.ui.PgBackBtn.clicked.connect(partial(self.btnsnavigation, False))
        self.ui.PgNextBtn.clicked.connect(partial(self.btnsnavigation, True))
        self.ui.PgBackBtn.setShortcut(QtGui.QKeySequence.MoveToPreviousChar)
        self.ui.PgNextBtn.setShortcut(QtGui.QKeySequence.MoveToNextChar)

        # temp load button
        self.ui.loadbtn.clicked.connect(partial(self.selectdirectory))

        # bottom bar
        self.btnstools()

        self.ui.SaveBtn.clicked.connect(partial(self.saving))
        self.ui.SaveBtn.setShortcut(QtGui.QKeySequence.MoveToNextLine)

    def btnsnavigation(self, direction):
        self.navi.load_pic(self.ui.photolbl, self.drawer.hasWork, direction)
        self.drawer.destroy(True, )

    def btnstools(self):
        self.ui.ResetBtn.clicked.connect(partial(self.drawer.destroy, False))
        self.ui.NewObjBtn.clicked.connect(partial(self.drawer.destroy, True))
        self.ui.NewObjBtn.clicked.connect(partial(lambda : self.ui.ObjName.setText('')))

        # self.ui.UndoBtn.clicked.connect(partial())
        # self.ui.RedoBtn.clicked.connect(partial())

    def selectdirectory(self):
        if self.navi.load_folder(self.drawer.hasWork):
            self.navi.load_pic(self.ui.photolbl, True, 0)
            self.drawer.readyarea = True  # only then activate drawer area

    def saving(self):
        if len(self.ui.ObjName.text()) > 0:
            print(self.ui.ObjName.text())
            path = self.navi.filenametemplate + str(self.navi.index) + "_" + self.ui.ObjName.text() + ".png"
            self.drawer.savePixels(path)

        else:
            self.drawer.saveConfirmation(False)


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Create and show the window
    window = MainWindow()
    window.setWindowTitle("Activity Reference")
    window.setWindowIcon(QtGui.QIcon('gui/Icon.ico'))

    window.show()

    sys.exit(app.exec_())
