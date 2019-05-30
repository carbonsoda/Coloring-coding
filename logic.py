import os
from PySide2 import QtCore, QtGui, QtWidgets

class Navigation(object):
    def __init__(self):
        self.folder = []

        self.error = 0
        self.index = 0

    def load_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()  # type = string
        self._load_folder(directory)

    # collects paths of all pics in folder
    def _load_folder(self, directory):
        fileext = (".jpg", ".jpeg", ".png", ".gif")

        for path, _, files in os.walk(directory):
            for img in files:
                if img.endswith(fileext):
                    self.folder.append(path + os.sep + img)

    # next = boolean
    def btnsindex(self, next):
        if next:
            if (self.index + 1) < len(self.folder):
                self.index += 1
        else:
            if (self.index - 1) > -1:
                self.index -= 1

    def load_pic(self, photolabel, next = 0):
        if next is not 0:  # if next = 0, inital load-up
            self.btnsindex(next)

        image_path = self.folder[self.index]
        photo = QtGui.QPixmap(image_path)

        photolabel.setPixmap(photo)
        photolabel.setScaledContents(True)
        photolabel.show()
        # photolabel.setGeometry(QtCore.QRect(10, 40, photo.width(), photo.height()))


class Drawing(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.setGeometry(parent.geometry())

        self.pen = QtGui.QPen(QtCore.Qt.cyan, 3, QtCore.Qt.SolidLine)
        self.path = QtGui.QPainterPath()

    # to implement later
    def isValidPoint(self, point):
        return 0 <= point.x() <= self.width() and 0<= point.y() <= self.height()
        #return 500 >= point.x() >= 0 and 500 >= point.y() >= 0

    # shrug is purely for the function of the partial
    # partial bc otherwise for some reason they're all auto-clicked?
    def destroy(self, shrug):
        self.path = QtGui.QPainterPath()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.drawPath(self.path)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.path.moveTo(event.pos())
            self.drawing = True
            self.lastPoint = event.pos()
            self.firstPoint = event.pos()

            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            self.path.lineTo(event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == QtCore.Qt.LeftButton:
            self.path.lineTo(self.firstPoint)
            self.drawing = False
            self.update()