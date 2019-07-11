import ctypes
from PySide2 import QtCore, QtGui, QtWidgets

class UiMain:
    def setupUi(self, MainWindow):
        self.setConstants()

        MainWindow.setFixedSize(self.windowSize)
        self.window = QtWidgets.QWidget(MainWindow)
        self.window.setFixedSize(self.windowSize)
        MainWindow.setCentralWidget(self.window)

        self.menubar = MainWindow.menuBar()
        self.menusetup()

        self.topsetup()
        self.centersetup()
        self.bottomsetup()

        windowlayout = QtWidgets.QGridLayout(self.window)
        windowlayout.addWidget(self.top, 0, 0, 1, 1)
        windowlayout.addWidget(self.center, 1, 0, 1, 1)
        windowlayout.addWidget(self.bottom, 3, 0, 1, 1)
        windowlayout.addItem(QtWidgets.QSpacerItem(1000, 20), 3, 0, 1, 1)
        self.window.setLayout(windowlayout)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setConstants(self):
        ratio = 6 / 4
        h = ctypes.windll.user32.GetSystemMetrics(1) - 300
        size = QtCore.QSize(int(h * ratio), h)

        width = int(size.width() - 40)
        self.width = width
        self.topbotSize = QtCore.QSize(width, 90)
        self.centerSize = QtCore.QSize(width, int(size.height() * 0.75))
        self.windowSize = size


        # Aesthetics
        self.font = QtGui.QFont("Arial", 12)  # default size
        self.fontS = QtGui.QFont("Arial", 9)  # small
        self.fontL = QtGui.QFont("Arial", 14)  # large
        self.sizeExpanding = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

    def menusetup(self):
        filemenu = self.menubar.addMenu('File')
        self.loadAction = QtWidgets.QAction('Load New Folder')
        self.loadAction.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.loadAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.load2ndAction = QtWidgets.QAction('Load Folder as 2nd Coder')
        self.load2ndAction.setShortcut((QtGui.QKeySequence('Ctrl+P')))
        self.load2ndAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)

        self.exitAction = QtWidgets.QAction('Save && Exit')
        self.exitAction.setShortcut(QtGui.QKeySequence('Ctrl+E'))
        self.exitAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)


        filemenu.addAction(self.loadAction)
        filemenu.addAction(self.load2ndAction)
        filemenu.addSeparator()
        filemenu.addAction(self.exitAction)

        viewmenu = self.menubar.addMenu('View')
        self.folderviewAction = QtWidgets.QAction('Open Coded Folder')
        self.folderviewAction.setShortcut(QtGui.QKeySequence('Ctrl+V'))

        viewmenu.addAction(self.folderviewAction)

    def topsetup(self):
        # actual buttons
        self.PgBackBtn = QtWidgets.QPushButton("<< Prev Page", self.window)
        self.PgBackBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left))
        self.PgNextBtn = QtWidgets.QPushButton("Next Page >>", self.window)
        self.PgNextBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right))

        self.Pglbl = QtWidgets.QLabel('Page\n0', self.window)
        font = self.fontS
        font.setWeight(57)
        self.Pglbl.setFont(font)
        self.Pglbl.setAlignment(QtCore.Qt.AlignCenter)

        # grid/top area setup
        self.top = QtWidgets.QWidget(self.window)
        # self.top.setFixedSize(self.topbotSize)
        self.top.setFixedSize(QtCore.QSize(self.width, 40))
        self.top.setContentsMargins(10, -10, 10, 0)
        self.TopBox = QtWidgets.QGridLayout(self.top)
        self.TopBox.setContentsMargins(-1, -1, -20, 6)
        self.TopBox.setHorizontalSpacing(100)
        self.spacer = QtWidgets.QSpacerItem(170, self.top.height())

        # adding stuff ontop the top grid layout
        self.TopBox.addWidget(self.PgBackBtn, 0, 0, 0, 1)
        self.TopBox.addWidget(self.Pglbl, 0, 2, 1, 1)
        self.TopBox.addWidget(self.PgNextBtn, 0, 4, 0, 1)
        # self.TopBox.addItem(self.spacer, 0, 1, 2, 1)

    def centersetup(self):
        self.center = QtWidgets.QFrame(self.window)
        self.center.setFixedSize(self.centerSize)

        self.photolbl = QtWidgets.QLabel(self.center)
        self.photolbl.setText("Please load a picture folder to begin.")
        self.photolbl.setAlignment(QtCore.Qt.AlignCenter)
        self.photolbl.setMaximumSize(self.center.size())
        self.photolbl.setSizePolicy(self.sizeExpanding)

    def bottomsetup(self):
        # widget/area + layout initializing
        self.bottom = QtWidgets.QWidget(self.window)
        # self.bottom.setFixedSize(self.topbotSize)
        self.bottom.setFixedWidth(self.width)
        self.bottom.setFixedHeight(90)

        self.BotBox = QtWidgets.QGridLayout(self.bottom)
        self.BotBox.setContentsMargins(20, 10, 10, 20)
        self.BotBox.setHorizontalSpacing(10)
        self.BotBox.setVerticalSpacing(17)

        self.ObjName = QtWidgets.QLineEdit(self.bottom)
        self.ObjName.setPlaceholderText("What did you draw?")
        self.ObjName.setFont(self.fontL)
        self.ObjName.setFixedHeight(35)
        self.SaveBtn = QtWidgets.QPushButton('Save Object',self.bottom)
        self.SaveBtn.setFont(self.font)
        self.SaveBtn.setFixedHeight(25)
        self.SaveBtn.setShortcut(QtGui.QKeySequence('Ctrl+S'))

        self.toolssetup()
        self.colorpicker()

        # color label misc setup
        colortitlelabel = QtWidgets.QLabel('Pen\nColor')
        colortitlelabel.setAlignment(QtCore.Qt.AlignHCenter)
        colortitlelabel.setFont(self.fontS)
        colortitlelabel.setStyleSheet('text-decoration: underline; padding-top: 0px')
        colortitlelabel.setFixedHeight(40)
        color_lbl = QtWidgets.QLabel()
        color_lbl.setFixedHeight(40)
        color_lbl.setAlignment(QtCore.Qt.AlignBottom)
        self.colorlbl = QtWidgets.QLabel(color_lbl)
        self.colorlbl.setAlignment(QtCore.Qt.AlignBottom)
        self.colorlbl.setStyleSheet('background-color: cyan; padding-top: 15px')  # default color
        self.colorlbl.setFixedSize(QtCore.QSize(30, 20))
        spacer = QtWidgets.QSpacerItem(int(self.window.width() * (1/5)), 20)

        # Add everything to bottom area
        self.BotBox.addWidget(colortitlelabel, 0, 0, 1, 1)
        self.BotBox.addWidget(color_lbl, 2, 0, 1, 1)

        self.BotBox.addWidget(self.colorbox, 0, 1, 4, 1)
        self.BotBox.addWidget(self.Tools, 0, 2, 3, 1)
        self.BotBox.addItem(spacer, 0, 3, 1, 1)

        self.BotBox.addWidget(self.ObjName, 0, 4, 1, 1)
        self.BotBox.addWidget(self.SaveBtn, 2, 4, 1, 1)

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

        self.NewObjBtn.setShortcut(QtGui.QKeySequence('Ctrl+N'))
        self.ResetBtn.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        self.UndoBtn.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        self.EraseBtn.setShortcut(QtGui.QKeySequence('Ctrl+X'))

        # Make tool grid + add the buttons on
        self.Tools = QtWidgets.QWidget(self.bottom)
        self.Tools.setFixedHeight(80)
        self.ToolGrid = QtWidgets.QGridLayout(self.Tools)
        self.ToolGrid.addWidget(self.UndoBtn, 0, 0, 1, 1)
        self.ToolGrid.addWidget(self.EraseBtn, 0, 1, 1, 1)
        self.ToolGrid.addWidget(self.ResetBtn, 1, 0, 1, 1)
        self.ToolGrid.addWidget(self.NewObjBtn, 1, 1, 1, 1)

    # Pen color
    def colorpicker(self):
        colors = [
             'red', 'yellow', '#ffa02f', 'green',
            'cyan', 'magenta', 'black', 'white'
        ]

        self.colorbtns = QtWidgets.QButtonGroup(self.Tools)
        buttons = []
        i = 1  # to give buttons positive ids
        for color in colors:
            button = QtWidgets.QPushButton(self.bottom)
            button.setStyleSheet('background-color: ' + color)
            button.setObjectName(color)
            self.colorbtns.addButton(button, i)
            i += 1
            buttons.append(button)

        self.colorbox = QtWidgets.QGroupBox(self.bottom)
        self.colorbox.setFixedHeight(80)
        colorgrid = QtWidgets.QGridLayout(self.colorbox)

        i = 0
        j = 0
        for button in buttons:
            colorgrid.addWidget(button,i, j, 1, 1)
            j += 1
            if j == 4:
                i += 1
                j = 0