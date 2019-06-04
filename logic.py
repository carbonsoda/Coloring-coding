import os
from PySide2 import QtCore, QtGui, QtWidgets

class Navigation(object):
    def __init__(self):
        self.folder = []
        self.foldername = ""
        self.filenametemplate = ""

        self.index = 0
        self.page = 1

    def load_folder(self, hasWork):
        if len(self.folder) > 0 and hasWork:
            if hasWork:
                self.loadErrorMsg(False)
                return False
            else:  # reset for new collection
                self.folder = []
                self.foldername = ""

        # directory = QtWidgets.QFileDialog.getExistingDirectory()  # type = string
        directory = QtWidgets.QFileDialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)

        fileext = (".jpg", ".jpeg", ".png", ".gif")
        pathing = ""

        for path, _, files in os.walk(directory):
            pathing = path
            for img in files:
                if img.endswith(fileext):
                    self.folder.append(path + os.sep + img)
            break

        if len(self.folder) < 1:
            self.loadErrorMsg(True)
            return False

        self.foldername = os.path.split(directory)[1]
        self._load_folder(pathing)
        return True

    def _load_folder(self, directory):
        newpath = os.path.join(directory, 'Coded').replace('\\','/')
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        temp = newpath + os.sep + self.foldername + '_pg_'
        self.filenametemplate = temp.replace('\\', '/')

    # next = boolean
    def btnsindex(self, next):
        if next:
            if (self.index + 1) < len(self.folder):
                self.index += 1
                self.page += 1
        else:
            if (self.index - 1) > -1:
                self.index -= 1
                self.page -= 1

    def load_pic(self, photolabel, isSaved = True, next = 0):
        if isSaved:
            if next is not 0:  # if next = 0, inital load-up
                self.btnsindex(next)

            image_path = self.folder[self.index]
            photo = QtGui.QPixmap(image_path)

            photolabel.setPixmap(photo)
            photolabel.setScaledContents(True)
            photolabel.show()
        else:
            self.reminderMsg()

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

class Drawing(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(parent.geometry())
        self.path = QtGui.QPainterPath()
        self.firstPoint = QtCore.QPoint()
        self.recorder = []

        self.drawing = False
        self.hasWork = False
        self.readyarea = False

        self.pen = QtGui.QPen(QtCore.Qt.cyan, 3, QtCore.Qt.SolidLine)

        self.image = self._drawingLayer()

    def _drawingLayer(self):
        pixmap = QtGui.QPixmap('gui/Untitled.png')
        return pixmap.scaled(self.width(), self.height())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        painter.drawPath(self.path)

        painter.drawPixmap(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.readyarea:
            self.path.moveTo(event.pos())
            self.drawing = True
            self.firstPoint = event.pos()
            self.recorder.append(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            self.path.lineTo(event.pos())
            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            p.drawPath(self.path)

            self.hasWork = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == QtCore.Qt.LeftButton and self.drawing:
            self.drawing = False
            self.hasWork = True

    def finishBlob(self, endPoint):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.drawTo(endPoint)


    def isValidPoint(self, point):
        self.xValid = True
        self.yValid = True
        if not (0 <= point.x() <= self.width()):
            self.xValid = False
        if not (0 <= point.y() <= self.height()):
            self.yValid = False
        return self.xValid and self.yValid

    # 3 cases for what needs fixing
    def pointFixer(self, point):
        if not self.xValid:
            if not self.yValid:
                pass
            else:
                point.x = self.width()
        elif not self.yValid:
            pass
        return point

    def destroy(self, new):
        self.path = QtGui.QPainterPath()
        self.hasWork = False
        self.image = self._drawingLayer()
        self.update()

    def savePixels(self, filename):
        self.image.save(filename, "png")
        self.hasWork = False
        self.saveConfirmation(True)

    def saveConfirmation(self, isNamed):
        msg = QtWidgets.QMessageBox()
        if isNamed:
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Save Successful!")
        else:
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Please enter an object name")

        msg.setWindowTitle("Save Reference Object")
        msg.exec_()
