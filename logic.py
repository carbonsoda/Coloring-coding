import os
from PySide2 import QtCore, QtGui, QtWidgets

class Navigation:
    def __init__(self):
        self.imgfolder = {}
        self.savepath = ""  # Coded folder
        self.title = ""  # book name
        self.picsize = QtCore.QSize()
        self.initals = ""
        self.pgs = []

        self.page = -1
    
    def makesavepath(self, objname):
        page = str(self.pgs[self.page])
        if len(page) < 2:
            page = '0' + page
        filename = self.title + '_pg_' + page + '_' + objname + '.png'
        if len(self.initals) > 1:
            filename = self.initals + '_' + filename
        return os.path.join(self.savepath, filename).replace('\\', '/')
    
    def resetall(self):
        self.imgfolder.clear()
        self.savepath = ''
        self.title = ''
        self.picsize = QtCore.QSize()
        self.page = -1

    def loading(self, input=None):
        if not input:
            self.loadErrorMsg(True)
            return False
        else:
            book = input[0]
            title = input[1]
            try:
                self.page = 0
                self.title = title
                self.pgs = book[1]  # list of int
                self.imgfolder = book[2]
            except KeyError:
                print('hm')
                self.loadErrorMsg(True)
                return False

        return True

    def load_pic(self, photolabel, framesize, hasWork, next=0):
        if hasWork:
            self.reminderMsg()
            return False
        else:
            # if next = 0, its the inital load
            if next == 1:
                if (self.page + 1) <= (len(self.pgs) + 1):
                    self.page +=1
            elif next == 2:
                if (self.page - 1) > 0:
                    self.page -= 1

            page = self.pgs[self.page]

            imagepath = self.imgfolder[page]
            pix = QtGui.QPixmap(imagepath)
            photo = pix.scaled(
                framesize,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation,
            )

            self.picsize = photo.size()
            photolabel.setFixedSize(photo.size())
            photolabel.setPixmap(photo)
            photolabel.show()

            return True

    def loadErrorMsg(self, isError):
        msg = QtWidgets.QMessageBox()

        if isError:
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Loading Issue")
            msg.setText("This folder doesn't contain any images.")
            msg.setInformativeText("Only jpg, jpeg, png, and gif files are accepted. Please try again.")
        else:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Loading Reminder")
            msg.setText("This will replace all images")
            msg.setInformativeText("Please make sure your work is saved")

        msg.exec_()

    def reminderMsg(self):
        msg = QtWidgets.QMessageBox()

        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Save Reminder")
        msg.setText("Please save your work before moving on")
        msg.setInformativeText("Type object's name and click the save button")

        msg.exec_()

    def trainingMsg(self):
        msg = QtWidgets.QMessageBox()

        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Training Name")
        msg.setText("Please input your initials before starting")

        msg.exec_()