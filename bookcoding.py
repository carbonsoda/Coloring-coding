import sys, ctypes
import logic, drawing, ui_main
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = ui_main.UiMain()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.window)

        self.navi = logic.Navigation()
        self.drawer = drawing.Drawing(self.ui.center)

        self.ui.ObjName.textChanged.connect(lambda: self.ui.ObjName.text())
        self.btnssetup()  # connections setup

        self.ui.colorbtns.buttonClicked.connect(
            partial(
                self.colorsclicked,
                self.ui.colorbtns.checkedButton()
            )
        )

    def colorsclicked(self, _, btn):
        btnID = self.ui.colorbtns.id(btn)
        colors = {
            1: (QtCore.Qt.red, 'red'),
            2: (QtCore.Qt.yellow, 'yellow'),
            3: (QtGui.QColor('#ffa02f'), 'rgb(255, 160, 47)'),
            4: (QtCore.Qt.green, 'green'),
            5: (QtCore.Qt.cyan, 'cyan'),
            6: (QtCore.Qt.magenta, 'magenta'),
            7: (QtCore.Qt.black, 'black'),
            8: (QtCore.Qt.white, 'white')
        }
        self.drawer.setNewColor(colors[btnID][0])
        self.ui.colorlbl.setStyleSheet('background-color: ' + colors[btnID][1])

    def btnssetup(self):
        # menubar
        self.ui.loadAction.triggered.connect(partial(self.selectdirectory, False))
        self.ui.load2ndAction.triggered.connect(partial(self.selectdirectory, True))
        self.ui.exitAction.triggered.connect(self.close)

        # top bar
        self.ui.PgBackBtn.clicked.connect(partial(self.btnsnavigation, 2))
        self.ui.PgNextBtn.clicked.connect(partial(self.btnsnavigation, 1))

        # bottom bar
        self.ui.ResetBtn.clicked.connect(partial(self.btnsdestroy, False))
        self.ui.NewObjBtn.clicked.connect(partial(self.btnsdestroy, True))
        self.ui.UndoBtn.clicked.connect(partial(self.drawer.undoStroke))
        self.ui.SaveBtn.clicked.connect(partial(self.saving))

    def btnsdestroy(self, new):
        self.drawer.mydestroy()
        if new:
            self.ui.ObjName.setText('')

    def btnsnavigation(self, direction):
        toDiscard = self.navi.load_pic(
            self.ui.photolbl, self.ui.centerSize,
            self.drawer.hasWork, direction
        )
        if toDiscard:
            self.drawer.mydestroy(True)
    def selectdirectory(self):
        self.navi.imgfolder.clear()
        self.drawer.mydestroy()
        if self.drawer.readyarea:  # if the drawing area is already activated
            self.ui.photolbl.clear()
        if self.navi.load_folder():
            self.navi.load_pic(self.ui.photolbl, self.ui.centerSize, False)
            self.ui.photolbl.setBaseSize(self.navi.picsize)
            self.drawer.image = self.drawer.layerCreate(self.navi.picsize)
            self.drawer.readyarea = True  # only then activate drawer area

    def saving(self):
        if len(self.ui.ObjName.text()) > 0:
            imgpath = self.navi.makesavepath(self.ui.ObjName.text())
            self.drawer.savePixels(imgpath)
        else:
            self.drawer.saveConfirmation(False)

if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # for Windows
    myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # from ctypes
    app.setWindowIcon(QtGui.QIcon('gui/Icon.ico'))

    # Create and show main window
    window = MainWindow()
    window.setWindowTitle('Activity Reference')
    window.show()

    sys.exit(app.exec_())
