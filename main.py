import sys
from ctypes import windll
from os import path as ospath
from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
from ui_main import Ui_main as MyUi
import logic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.ui = MyUi()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.window)
        self.menuSetup()

        self.navi = logic.Navigation()
        self.drawer = logic.Drawing(self.ui.center)
        # self.ui.center.addWidget(self.drawer, 0, 1, 0, 1)

        self.ui.ObjName.textChanged.connect(lambda : self.ui.ObjName.text())
        # self.ui.photolbl.installEventFilter(self)
        self.ui.center.installEventFilter(self)
        self.btnssetup()  # connections setup

    def eventFilter(self, source, event):
        if source is self.ui.center and event.type() == QtCore.QEvent.Resize:
            self.ui.photolbl.resize(source.size())
            print(self.ui.photolbl.size())
            if len(self.navi.folder) > 0:  # if img is loaded
                self.ui.photolbl.setPixmap(self.navi.imageResize(self.ui.photolbl.size()))
                self.drawer.layerResize(self.ui.photolbl.size())
            self.ui.photolbl.show()  # idk if needed?
        return super(MainWindow, self).eventFilter(source, event)

    def btnssetup(self):
        self.ui.PgBackBtn.clicked.connect(partial(self.btnsnavigation, False))
        self.ui.PgNextBtn.clicked.connect(partial(self.btnsnavigation, True))
        # bottom bar
        self.ui.ResetBtn.clicked.connect(partial(self.drawer.destroy, False))
        self.ui.NewObjBtn.clicked.connect(partial(self.btnsnewobject))
        self.ui.ResetBtn.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        self.ui.NewObjBtn.setShortcut(QtGui.QKeySequence('Ctrl+N'))
        # self.ui.UndoBtn.clicked.connect(partial(self.drawer.undoStroke,))
        # self.ui.EraseBtn.clicked.connect(partial())
        self.ui.SaveBtn.clicked.connect(partial(self.saving))
        self.ui.SaveBtn.setShortcut(QtGui.QKeySequence('Ctrl+S'))

    def btnsnewobject(self):
        self.drawer.destroy(False)
        self.ui.ObjName.setText('')

    def btnsnavigation(self, direction):
        toDiscard = self.navi.load_pic(self.ui.photolbl, self.drawer.hasWork, direction)
        if toDiscard:
            self.drawer.destroy(True)

    def selectdirectory(self):
        if self.navi.load_folder(self.drawer.hasWork):
            self.navi.load_pic(self.ui.photolbl, False, 0)
            self.drawer.readyarea = True  # only then activate drawer area

    def saving(self):
        if len(self.ui.ObjName.text()) > 0:
            print(self.ui.ObjName.text())
            imgtitle = self.navi.foldername + '_pg'+ str(self.navi.page) + '_' + self.ui.ObjName.text() + '.png'
            path = ospath.join(self.navi.path, imgtitle).replace('\\','/')
            self.drawer.savePixels(path)

        else:
            self.drawer.saveConfirmation(False)

    def menuSetup(self):
        bar = self.menuBar()

        filemenu = bar.addMenu('File')
        loadAction = QtWidgets.QAction('Load Folder', self)
        loadAction.triggered.connect(self.selectdirectory)
        loadAction.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        loadAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)

        exitAction = QtWidgets.QAction('Exit', self)
        exitAction.triggered.connect(self.close)

        filemenu.addAction(loadAction)
        filemenu.addAction(exitAction)

if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # for Windows
    myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # from ctypes

    # Create and show the window
    window = MainWindow()
    window.setWindowTitle("Activity Reference")
    window.setWindowIcon(QtGui.QIcon('gui/Icon.ico'))

    window.show()

    sys.exit(app.exec_())
