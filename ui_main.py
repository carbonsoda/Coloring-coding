from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1179, 943)
        self.window = QtWidgets.QWidget(MainWindow)
        self.window.setMinimumSize(QtCore.QSize(1179, 943))

        # Aesthetics
        self.font = QtGui.QFont("Arial", 12)  # default size
        self.fontS = QtGui.QFont("Arial", 9)  # small
        self.fontL = QtGui.QFont("Arial", 14)  # large

        self.topsetup()
        self.centersetup()
        self.bottomsetup()

        self.windowlayout = QtWidgets.QGridLayout(self.window)
        self.windowlayout.addWidget(self.top, 0, 0, 1, 1)
        self.windowlayout.addWidget(self.center, 1, 0, 1, 1)
        self.windowlayout.addWidget(self.bottom, 2, 0, 1, 1)

        # self.temp()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def topsetup(self):
        # actual buttons
        self.PgBackBtn = QtWidgets.QPushButton("<< Prev Page", self.window)
        self.PgBackBtn.setShortcut(QtGui.QKeySequence.MoveToPreviousChar)
        self.PgNextBtn = QtWidgets.QPushButton("Next Page >>", self.window)
        self.PgNextBtn.setShortcut(QtGui.QKeySequence.MoveToNextChar)

        # grid/top area setup
        self.top = QtWidgets.QWidget(self.window)
        self.top.setMinimumSize(QtCore.QSize(940, 70))
        self.top.setContentsMargins(10, 10, 10, 0)
        self.TopBox = QtWidgets.QGridLayout(self.top)
        self.TopBox.setContentsMargins(-1, -1, -20, 6)
        self.spacer = QtWidgets.QSpacerItem(170, self.top.height())

        # adding stuff ontop the top grid layout
        self.TopBox.addWidget(self.PgBackBtn, 0, 0, 0, 1)
        self.TopBox.addWidget(self.PgNextBtn, 0, 4, 0, 1)
        self.TopBox.addItem(self.spacer, 0, 1, 1, 1)

    def centersetup(self):
        self.center = QtWidgets.QFrame(self.window)
        self.center.setMinimumSize(QtCore.QSize(960, 700))
        self.center.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.photolbl = QtWidgets.QLabel(self.center)
        self.photolbl.setAlignment(QtCore.Qt.AlignCenter)
        self.photolbl.setBaseSize(self.center.size())
        self.photolbl.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        # self.photolbl.resizeEvent()
        # self.photolbl.resize(960, 700)  # not big fan of hardcode but :/
        self.photolbl.setText("Please load a picture folder to begin.")
        self.photolbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.centerBox.addWidget(self.photolbl, 0, 1, 0, 1)

    def bottomsetup(self):
        self.bottom = QtWidgets.QWidget(self.window)
        self.bottom.setMinimumHeight(90)
        self.bottom.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )

        self.ObjName = QtWidgets.QLineEdit(self.bottom)
        self.ObjName.setPlaceholderText("What did you draw?")
        self.ObjName.setFont(self.fontL)
        self.SaveBtn = QtWidgets.QPushButton('Save Object',self.bottom)
        self.SaveBtn.setFont(self.font)

        self.toolssetup()

        # Add everything to bottom area
        self.BotBox = QtWidgets.QGridLayout(self.bottom)
        self.BotBox.setContentsMargins(10, 10, 10, 10)
        # self.BotBox.setContentsMargins(0, 10, 0, 0)
        self.BotBox.addWidget(self.Tools, 0, 0, 1, 1)
        self.BotBox.addItem(QtWidgets.QSpacerItem(40, 20), 0, 1, 1, 1)
        self.BotBox.addWidget(self.ObjName, 0, 2, 1, 1)
        self.BotBox.addWidget(self.SaveBtn, 2, 2, 1, 1)


    # Tools Grid = Has all the tools for drawing
    # color picker to be implemented eventually
    def toolssetup(self):
        self.EraseBtn = QtWidgets.QPushButton('Erase',self.bottom)
        self.UndoBtn = QtWidgets.QPushButton('Undo',self.bottom)
        self.ResetBtn = QtWidgets.QPushButton('Reset',self.bottom)
        self.NewObjBtn = QtWidgets.QPushButton('New',self.bottom)

        self.NewObjBtn.setFont(self.font)
        self.ResetBtn.setFont(self.font)
        self.UndoBtn.setFont(self.font)
        self.EraseBtn.setFont(self.font)

        # Make tool grid + add the buttons on
        self.Tools = QtWidgets.QWidget(self.bottom)
        self.ToolGrid = QtWidgets.QGridLayout(self.Tools)
        self.ToolGrid.addWidget(self.NewObjBtn, 0, 0, 1, 1)
        self.ToolGrid.addWidget(self.ResetBtn, 0, 1, 1, 1)
        self.ToolGrid.addWidget(self.UndoBtn, 0, 2, 1, 1)
        self.ToolGrid.addWidget(self.EraseBtn, 0, 3, 1, 1)