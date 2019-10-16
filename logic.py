import os
from PySide2 import QtCore, QtGui, QtWidgets


class Navigation(object):
    def __init__(self):
        self.imgfolder = []
        self.savepath = ""  # Coded folder
        self.title = ""  # book name
        self.picsize = QtCore.QSize()

        self.page = 1

    def makesavepath(self, objname):
        page = str(self.page)
        if len(page) < 2:
            page = '0' + str(self.page)
        filename = self.title + '_pg' + page + '_' + objname + '.png'
        return os.path.join(self.savepath, filename).replace('\\', '/')

    def load_folder(self):
        self.imgfolder = {}
        folder = QtWidgets.QFileDialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)

        fileext = (".jpg", ".jpeg", ".png", ".gif")
        fileschema = ("Slide", "Page", "Pg", "P")

        for path, _, files in os.walk(folder):
            self.imgfolder[0] = path
            for img in files:
                if img.endswith(fileext) and any(schema in img for schema in fileschema):
                    index = int(os.path.splitext(img)[0][-2:])
                    imgpath = os.path.join(path, img).replace('\\', '/')
                    self.imgfolder[index] = imgpath
            break

        if len(self.imgfolder) < 1:
            # has no img files
            self.loadErrorMsg()
            return False
        else:
            newpath = os.path.join(self.imgfolder[0], 'Coded').replace('\\', '/')
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.chmod(newpath, 0o777)

            self.imgfolder[0] = (self.imgfolder[0], newpath)

            self.savepath = self.imgfolder[0][1]
            self.title = os.path.split(self.imgfolder[0][0])[1]

            return True

    def load_pic(self, photolabel, framesize, hasWork, next=0):
        if hasWork:
            self.reminderMsg()
            return False
        elif len(self.imgfolder) < 1:
            pass
        else:
            # if next = 0, its the inital load
            if next == 1:
                if (self.page + 1) < len(self.pgs):
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

    def loadErrorMsg(self):
        msg = QtWidgets.QMessageBox()

        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Loading Issue")
        msg.setText("This folder doesn't contain any images.")
        msg.setInformativeText("Only jpg, jpeg, png, and gif files are accepted. Please try again.")

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
