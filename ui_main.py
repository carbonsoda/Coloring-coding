from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(835, 708)  # resize to 2x: (1670, 1410)
        self.window = QtWidgets.QWidget(MainWindow)
        self.window.setFixedSize(830, 705)  # resize to 2x: (1660, 1410)

        # constants
        self.w = self.window.width()
        self.h = self.window.height()

        # Aesthetics
        self.font = QtGui.QFont("Arial", 12)  # default size
        self.fontS = QtGui.QFont("Arial", 9)  # small
        self.fontL = QtGui.QFont("Arial", 14)  # large

        self.sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.menusetup()
        self.mainsetup()

        # Until menusetup actually works :/
        self.temp()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def mainsetup(self):
        self.topsetup()
        self.centersetup()
        self.bottomsetup()

    def topsetup(self):
        # actual buttons
        self.PgBackBtn = QtWidgets.QPushButton("<< Prev Page", self.window)
        # self.PgBackBtn.setIcon(QtGui.QIcon(QtGui.QPixmap('left.png')))
        # self.PgBackBtn.setStyleSheet("QPushButton { text-align: left; }")
        self.PgBackBtn.setSizePolicy(self.sizepolicy)

        self.PgNextBtn = QtWidgets.QPushButton("Next Page >>", self.window)
        # self.PgNextBtn.setIcon(QtGui.QIcon(QtGui.QPixmap('right.png')))
        # self.PgNextBtn.setStyleSheet("QPushButton { text-align: right;}")
        self.PgNextBtn.setSizePolicy(self.sizepolicy)

        # grid/top area setup
        self.top = QtWidgets.QWidget(self.window)
        self.top.setContentsMargins(-1, -1, 0, 2)
        self.top.setGeometry(QtCore.QRect(20, 10, 790, 40))
        self.TopBox = QtWidgets.QGridLayout(self.top)
        self.TopBox.setGeometry(QtCore.QRect(20, 10, 789, 40))
        self.TopBox.setContentsMargins(-1, -1, -20, 6)
        self.spacer = QtWidgets.QSpacerItem(150, self.top.height())

        # adding stuff ontop the top grid layout
        self.TopBox.addWidget(self.PgBackBtn, 0, 0, 0, 1)
        self.TopBox.addWidget(self.PgNextBtn, 0, 4, 0, 1)
        self.TopBox.addItem(self.spacer, 0, 1, 1, 1)


    def temp(self):
        self.loadbtn = QtWidgets.QPushButton("Load Folder", self.window)
        self.TopBox.addWidget(self.loadbtn, 0, 2, 1, 1)
        # self.TopBox.addWidget(self.loadbtn, 0, 2, 0, 1, QtCore.Qt.AlignHCenter)
        spacer2 = self.spacer
        self.TopBox.addItem(spacer2, 0, 3, 1, 1)  # spacer


    # sets up everything for img under layer
    def imglayersetup(self):
        self.photolbl = QtWidgets.QLabel(self.centerArea)
        self.photolbl.resize(self.w, 520)  # not big fan of hardcode but :/

        self.centerBox.addWidget(self.photolbl, 0, 1, 0, 1)

    def centersetup(self):
        self.centerArea = QtWidgets.QFrame(self.window)
        self.centerArea.setGeometry(QtCore.QRect(20, 60, 790, 520))
        self.centerBox = QtWidgets.QGridLayout(self.centerArea)

        self.imglayersetup()

    def bottomsetup(self):
        self.bottom = QtWidgets.QWidget(self.window)
        self.bottom.setGeometry(QtCore.QRect(20, 580, 791, 94))


        self.ObjName = QtWidgets.QLineEdit(self.bottom)
        self.ObjName.setPlaceholderText("What did you draw?")
        self.ObjName.setFont(self.fontL)

        # Save button -- entire drawing + object name
        self.SaveBtn = QtWidgets.QPushButton('Save Object',self.bottom)
        self.SaveBtn.setFont(self.font)

        self.toolssetup()

        # Add everything to bottom area
        self.BotBox = QtWidgets.QGridLayout(self.bottom)
        # self.BotBox.setContentsMargins(0, 10, 0, 0)
        self.BotBox.addWidget(self.Tools, 0, 0, 1, 1)
        self.BotBox.addItem(QtWidgets.QSpacerItem(40, 20), 0, 1, 1, 1)
        self.BotBox.addWidget(self.ObjName, 0, 2, 1, 1)
        self.BotBox.addWidget(self.SaveBtn, 2, 2, 1, 1)


    # Tools Grid = Has all the tools for drawing
    # color picker to be implemented eventually
    # Helper method for self.bottomsetup()
    def toolssetup(self):
        # REDO button
        self.RedoBtn = QtWidgets.QPushButton('Redo',self.bottom)
        # UNDO button
        self.UndoBtn = QtWidgets.QPushButton('Undo',self.bottom)
        # RESET button
        self.ResetBtn = QtWidgets.QPushButton('Reset',self.bottom)
        # NEW OBJECT button
        self.NewObjBtn = QtWidgets.QPushButton('New',self.bottom)

        # Set font
        # Wish I could figure out to do it in bulk.....
        self.NewObjBtn.setFont(self.font)
        self.ResetBtn.setFont(self.font)
        self.UndoBtn.setFont(self.font)
        self.RedoBtn.setFont(self.font)

        # Make tool grid + add the buttons on
        self.Tools = QtWidgets.QWidget(self.bottom)
        self.ToolGrid = QtWidgets.QGridLayout(self.Tools)
        self.ToolGrid.addWidget(self.NewObjBtn, 0, 0, 1, 1)
        self.ToolGrid.addWidget(self.ResetBtn, 0, 1, 1, 1)
        self.ToolGrid.addWidget(self.UndoBtn, 0, 2, 1, 1)
        self.ToolGrid.addWidget(self.RedoBtn, 0, 3, 1, 1)

    def menusetup(self):
        # MENU BAR
        self.menubar = QtWidgets.QMenuBar(self.window)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.w, 21))
        self.menuFile = QtWidgets.QMenu(self.menubar)

        # Loading in folder of picture book photos
        self.PicLoadBtn = QtWidgets.QAction(self.window)
        # SUBJECT ACTIONS
        self.SubjNewBtn = QtWidgets.QAction(self.window)  # Create new Subject file
        self.SubjLoadBtn = QtWidgets.QAction(self.window)  # Load existing Subject file
        self.SubjSave = QtWidgets.QAction(self.window)

        # self.ExitBtn = QtWidgets.QAction(MainWindow)

        self.menuFile.addAction(self.PicLoadBtn)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.SubjNewBtn)
        self.menuFile.addAction(self.SubjLoadBtn)
        self.menuFile.addAction(self.SubjSave)
        # self.menuFile.addSeparator()
        # self.menuFile.addAction(self.ExitBtn)
        self.menubar.addAction(self.menuFile.menuAction())

