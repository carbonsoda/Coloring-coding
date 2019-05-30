import os
import gc
import numpy as np
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

        # constants
        self.pen = QtGui.QPen(QtCore.Qt.cyan, 3, QtCore.Qt.SolidLine)

        self.image = QtGui.QPixmap(parent.width(), parent.height())
        self.image.fill(QtCore.Qt.transparent)

        self.painter = QtGui.QPainter(self.image)
        self.painter.setPen(self.pen)
        #self.image.fill(QtCore.Qt.transparent)

    def isValidPoint(self, point):
        return 0 <= point.x() <= self.width() and 0<= point.y() <= self.height()
        #return 500 >= point.x() >= 0 and 500 >= point.y() >= 0

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.firstPoint = e.pos()
            self.lastPoint = e.pos()

    def mouseMoveEvent(self, e):
        if e.buttons() and QtCore.Qt.LeftButton and self.drawing:
            self.painter.drawLine(self.lastPoint, e.pos())
            self.lastPoint = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button == QtCore.Qt.LeftButton:
            self.painter.drawLine(self.lastPoint, self.firstPoint)
            self.update()
            self.drawing = False

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.image)
        painter.setPen(self.pen)
        painter.drawLine()

    def destroy(self, idk):
        self.painter.eraseRect(self.width(), self.height())
        self.update()
