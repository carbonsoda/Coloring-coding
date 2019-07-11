import sys, ctypes, os
import logic, drawing, ui, loadsave
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, basepath =None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.basepath = basepath

        self.ui = ui.UiMain()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.window)

        self.navi = logic.Navigation()
        self.drawer = drawing.Drawing(basepath ,self.ui.center)
        self.IOlogic = loadsave.LoadSave()

        self.ui.ObjName.textChanged.connect(lambda: self.ui.ObjName.text())
        self.btnssetup()  # connections setup

    def colorsclicked(self, _, btn):
        btnID = self.ui.colorbtns.id(btn)
        colors = {
            1: (QtCore.Qt.red, "red"),
            2: (QtCore.Qt.yellow, "yellow"),
            3: (QtGui.QColor("#ffa02f"), "rgb(255, 160, 47)"),
            4: (QtCore.Qt.green, "green"),
            5: (QtCore.Qt.cyan, "cyan"),
            6: (QtCore.Qt.magenta, "magenta"),
            7: (QtCore.Qt.black, "black"),
            8: (QtCore.Qt.white, "white"),
        }
        self.drawer.setNewColor(colors[btnID][0])
        self.ui.colorlbl.setStyleSheet("background-color: " + colors[btnID][1])

    def btnssetup(self):
        # menubar
        self.ui.loadAction.triggered.connect(partial(self.selectdirectory))
        self.ui.load2ndAction.triggered.connect(partial(self.selectdirectory, True))
        self.ui.exitAction.triggered.connect(partial(self.saving, True))

        # top bar
        self.ui.PgBackBtn.clicked.connect(partial(self.btnsnavigation, 2))
        self.ui.PgNextBtn.clicked.connect(partial(self.btnsnavigation, 1))

        # bottom bar
        self.ui.ResetBtn.clicked.connect(partial(self.btnsdestroy, False))
        self.ui.NewObjBtn.clicked.connect(partial(self.btnsdestroy, True))
        self.ui.UndoBtn.clicked.connect(partial(self.drawer.undoStroke))
        self.ui.SaveBtn.clicked.connect(partial(self.saving))

        # colors
        self.ui.colorbtns.buttonClicked.connect(
            partial(self.colorsclicked, self.ui.colorbtns.checkedButton())
        )

    def btnsdestroy(self, new):
        self.drawer.mydestroy()
        if new:
            self.ui.ObjName.setText("")

    def btnsnavigation(self, direction):
        toDiscard = self.navi.load_pic(
            self.ui.photolbl, self.ui.centerSize, self.drawer.hasWork, direction
        )
        if toDiscard:
            page = str(self.navi.pgs[self.navi.page])
            self.ui.Pglbl.setText("Page:\n" + page)
            self.drawer.mydestroy(self.navi.picsize)

    def selectdirectory(self, isSecond=False):
        self.drawer.mydestroy()
        if self.drawer.readyarea:
            self.ui.photolbl.clear()

        # first time loading
        mode = 'Coded'  # primary
        if isSecond:
            mode = 'Coded' + os.sep + 'Secondary'

        if self.navi.loading(self.IOlogic.load_folder(mode)):
            self.navi.savepath = self.IOlogic.savepath
            self.navi.load_pic(self.ui.photolbl, self.ui.centerSize, False)
            page = str(self.navi.pgs[self.navi.page])
            self.ui.Pglbl.setText("Page:\n" + page)
            
            self.ui.photolbl.setBaseSize(self.navi.picsize)
            self.drawer.image = self.drawer.layerCreate(self.navi.picsize, self.ui.photolbl.geometry())
            self.drawer.readyarea = True

    def saving(self, finalsave=None):
        if finalsave:
            self.IOlogic.book[3] = self.IOlogic.pageobjs
            filename = self.navi.title + '_base.pickle'
            self.IOlogic.topickle(filename, self.IOlogic.book)
            sys.exit()

        elif len(self.ui.ObjName.text()) > 0:
            objname = self.ui.ObjName.text()
            imgpath = self.navi.makesavepath(objname)

            self.drawer.savePixels(imgpath)
            self.IOlogic.addobject(
                self.navi.page,
                objname,
                imgpath
            )
            self.btnsdestroy(True)
        else:
            self.drawer.saveConfirmation(False)


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    base_path = os.path.dirname(os.path.abspath(__file__))
    icon = os.path.join(base_path, 'gui/Icon.ico').replace('\\', '/')

    # for Windows
    myappid = u"mycompany.myproduct.subproduct.version"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        myappid
    )  # from ctypes
    app.setWindowIcon(QtGui.QIcon(icon))

    # Create and show main window
    window = MainWindow(base_path)
    window.setWindowTitle("Book Object Coding")
    window.show()

    sys.exit(app.exec_())
