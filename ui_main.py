from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(835, 708)
        self.window = QtWidgets.QWidget(MainWindow)
        self.window.setFixedSize(830, 705)

        # Aesthetics
        self.font = QtGui.QFont("Arial", 12)  # default size
        self.fontS = QtGui.QFont("Arial", 9)  # small
        self.fontL = QtGui.QFont("Arial", 14)  # large

        self.menusetup()
        # bring focus to the content stuff below? I think?
        # MainWindow.setCentralWidget(self.window)
        # Content
        self.mainsetup()

        self.temp()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def mainsetup(self):
        self.topsetup()
        self.centersetup()
        self.bottomsetup()

    def topsetup(self):
        self.top = QtWidgets.QWidget(self.window)
        self.top.setContentsMargins(-1, -1, 200, 6)
        self.top.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.top.setGeometry(QtCore.QRect(20, 10, 830, 40))
        self.TopBox = QtWidgets.QGridLayout(self.top)
        self.TopBox.setContentsMargins(-1, -1, -20, 6)

        # actual buttons
        self.PgBackBtn = QtWidgets.QPushButton("<< Previous Page", self.window)
        self.PgNextBtn = QtWidgets.QPushButton("Next Page >>", self.window)

        # adding to the top area
        self.TopBox.addWidget(self.PgBackBtn, 0, 0, 0, 1)
        self.TopBox.addWidget(self.PgNextBtn, 0, 4, 0, 1)
        self.TopBox.addItem(QtWidgets.QSpacerItem(235, 20), 0, 1, 1, 1)  # spacer

    def temp(self):
        self.loadbtn = QtWidgets.QPushButton("Load Folder", self.window)

        self.TopBox.addWidget(self.loadbtn, 0, 2, 1, 1)
        self.TopBox.addItem(QtWidgets.QSpacerItem(235, 20), 0, 3, 1, 1)  # spacer

    # sets up everything for img under layer
    def imglayersetup(self):
        self.photolbl = QtWidgets.QLabel(self.centerArea)
        self.photolbl.resize(790, 520)  # not big fan of hardcode but :/

        # photo = QtGui.QPixmap('placeholder.png')
        # self.photolbl.setPixmap(photo)
        # self.photolbl.setScaledContents(True)

        self.centerBox.addWidget(self.photolbl, 0, 1, 0, 1)

    def drawlayersetup(self):
        self.drawPnl = QtWidgets.QWidget(self)
        self.drawPnl.setGeometry(QtCore.QRect(20, 60, 790, 520))
        self.drawPnl.setStyleSheet("background-color: transparent")


        self.centerBox.addWidget(self.drawPnl, 0, 1, 0, 1)

    def centersetup(self):
        self.centerArea = QtWidgets.QFrame(self.window)
        self.centerArea.setGeometry(QtCore.QRect(20, 60, 790, 520))
        self.centerBox = QtWidgets.QGridLayout(self.centerArea)

        self.imglayersetup()
        # self.drawlayersetup()

    def bottomsetup(self):
        self.bottom = QtWidgets.QWidget(self.window)
        self.bottom.setGeometry(QtCore.QRect(20, 580, 791, 94))


        self.ObjextInput = QtWidgets.QLineEdit(self.bottom)
        self.ObjextInput.setPlaceholderText("What did you draw?")
        self.ObjextInput.setFont(self.fontL)

        # Save button -- entire drawing + object name
        self.SaveBtn = QtWidgets.QPushButton('Save Object',self.bottom)
        self.SaveBtn.setFont(self.font)

        self.toolssetup()

        # Add everything to bottom area
        self.BotBox = QtWidgets.QGridLayout(self.bottom)
        # self.BotBox.setContentsMargins(0, 10, 0, 0)
        self.BotBox.addWidget(self.Tools, 0, 0, 1, 1)
        self.BotBox.addItem(QtWidgets.QSpacerItem(40, 20), 0, 1, 1, 1)
        self.BotBox.addWidget(self.ObjextInput, 0, 2, 1, 1)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 835, 21))
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

