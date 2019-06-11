import os
from PySide2 import QtCore, QtGui, QtWidgets

class Navigation(object):
    def __init__(self):
        self.folder = []
        self.foldername = ""
        self.path = ""

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
        fileschema = ("Slide", "Page", "Pg")
        pathing = ""

        for path, _, files in os.walk(directory):
            pathing = path
            for img in files:
                # to avoid accidental mis-placed coded files
                # for sake of runtime though, not sure if really needed
                if img.endswith(fileext) and img.startswith(fileschema):
                    self.folder.append(path + os.sep + img)
            break

        if len(self.folder) < 1:
            self.loadErrorMsg(True)
            return False

        self.foldername = os.path.split(directory)[1]
        print(self.foldername)
        print("I am folder name\n")
        self._load_folder(pathing)
        return True

    def _load_folder(self, directory):
        newpath = os.path.join(directory, 'Coded').replace('\\', '/')
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        self.path = newpath
        os.chmod(newpath, 0o775)
        self.make_executable(newpath)

    def make_executable(self, path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(path, mode)
        self.path = path

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

    def load_pic(self, photolabel, hasWork, next=0):
        if hasWork:
            self.reminderMsg(photolabel, next)
        else:
            if next is not 0:  # if next = 0, inital load-up
                self.btnsindex(next)

            image_path = self.folder[self.index]
            pix = QtGui.QPixmap(image_path)
            # photo = pix.scaledToWidth(photolabel.width())
            photo = pix.scaled(photolabel.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            photolabel.setPixmap(photo)
            photolabel.setAlignment(QtCore.Qt.AlignCenter)
            photolabel.show()
            return True
        return False

    # manages resizing event
    def imageResize(self, labelSize):
        image_path = self.folder[self.index]
        pix = QtGui.QPixmap(image_path)
        photo = pix.scaled(labelSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return photo

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

    def reminderMsg(self, label, next):
        print(next)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Save Reminder")
        msg.setText("Please save your work before moving on")
        msg.setInformativeText("Type object's name and click the save button")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Discard)

        msg.exec_()


class Drawing(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(parent.geometry())
        self.path = QtGui.QPainterPath()
        # self.first = QtCore.QPoint()  # first clicked point
        self.p1 = QtCore.QPoint()
        self.p2 = QtCore.QPoint()
        self.strokes = []
        self.step = 0  # step 0 is blank canvas

        self.drawing = False
        self.hasWork = False
        self.readyarea = False

        self.pen = QtGui.QPen(QtCore.Qt.cyan, 3, QtCore.Qt.SolidLine)

        self.image = self._layerCreate()

    def _layerCreate(self):
        pixmap = QtGui.QPixmap('gui/Untitled.png')
        return pixmap.scaled(self.width(), self.height())

    def layerResize(self, labelSize):
        self.image = self.image.scaled(labelSize, QtCore.Qt.KeepAspectRatio)

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
            self.p1 = event.pos()
            if self.step == 0:  # for undo function
                self.strokes.append(self.path)

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            self.path.lineTo(event.pos())
            self.p2 = event.pos()
            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            p.drawPath(self.path)

            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.strokes.append(self.path)  # saves current state of painterpath
            self.step += 1

            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            p.drawLine(self.p1, self.p2)
            self.update()

            self.drawing = False
            self.hasWork = True
            self.p1.isNull()
            self.p2.isNull()

    def undoStroke(self):
        self.path = self.strokes.pop()  # restore state
        self.image = self._layerCreate()  # resets canvas

        # redraws entire path
        p = QtGui.QPainter(self.image)
        p.setPen(self.pen)
        p.setBackgroundMode(QtCore.Qt.TransparentMode)
        p.drawPath(self.path)
        p.drawPixmap(self.rect(), self.image)

        self.update()

    def destroy(self, new):
        self.path = QtGui.QPainterPath()
        self.hasWork = False
        self.image = self._layerCreate()
        # self.step = 0
        # self.strokes.clear()
        self.update()

    def savePixels(self, filename):
        with open(filename, 'w'):
            file = QtCore.QFile(filename)
        file.open(QtCore.QIODevice.WriteOnly)
        file.close()
        self.image.save(file, "png")
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

    def loadErrorMsg(self, isError, file):
        msg = QtWidgets.QMessageBox()

        if isError:
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Loading Issue")
            msg.setText("I can read")
        else:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Loading Reminder")
            msg.setText("I can't read")
            msg.setInformativeText(os.stat(file))
            print(os.stat(file))

        msg.exec_()
