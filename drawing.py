import os
from PySide2 import QtWidgets, QtCore, QtGui


class Drawing(QtWidgets.QWidget):
    # Center QFrame = parent
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = QtGui.QPainterPath()
        self.pathhelper = QtGui.QPainterPath()
        self.p1 = QtCore.QPoint()

        self.strokeshelp = []
        self.strokes = []
        self.setFixedSize(parent.size())
        self.picsize = None

        self.drawing = False
        self.hasWork = False
        self.readyarea = False

        self.color = QtGui.QColor(QtCore.Qt.cyan)  # default color
        self.pen = QtGui.QPen(self.color, 3, QtCore.Qt.SolidLine)

        self.image = self.layerCreate()

    def setNewColor(self, color):
        self.color = QtGui.QColor(color)
        self.pen.setColor(self.color)
        self.update()

    def layerCreate(self, size=None):
        layer = QtGui.QPixmap("gui/Untitled.png")
        if size or self.picsize:
            if size:
                self.setFixedSize(size)
                self.picsize = size
            layer = layer.scaled(self.picsize, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
        return layer

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.pen.setColor(self.color)
        painter.setPen(self.pen)
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        painter.drawPath(self.path)
        painter.drawPath(self.pathhelper)

        painter.drawPixmap(event.rect(), self.image, self.rect())
        if self.hasWork:
            brush = self.color
            brush.setAlpha(100)
            for strokes in self.strokeshelp:
                painter.fillPath(strokes, brush)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.readyarea:
            # avoid everything refilled per mouseRelease
            self.pathhelper = QtGui.QPainterPath()

            self.path.moveTo(event.pos())
            self.pathhelper.moveTo(event.pos())
            self.drawing = True
            self.p1 = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            self.path.lineTo(event.pos())
            self.pathhelper.lineTo(event.pos())

            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            p.drawPath(self.path)

            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.path.lineTo(self.p1)
            self.pathhelper.lineTo(self.p1)
            self.strokeshelp.append(self.pathhelper)

            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            p.drawPath(self.path)
            self.update()

            self.drawing = False
            self.hasWork = True
            self.p1.isNull()

    def undoStroke(self):
        del self.strokeshelp[-1]

        if len(self.strokeshelp) < 1:
            self.mydestroy()
        else:
            self.path = QtGui.QPainterPath()
            self.pathhelper = QtGui.QPainterPath()
            self.image = self.layerCreate()  # resets canvas

            # redraws entire path
            p = QtGui.QPainter(self.image)
            p.setPen(self.pen)
            p.setBackgroundMode(QtCore.Qt.TransparentMode)
            brush = QtGui.QColor(self.color)
            brush.setAlpha(100)

            for blob in self.strokeshelp:
                p.drawPath(blob)
                p.drawPixmap(self.rect(), self.image, self.rect())
                self.path.addPath(blob)
            p.fillPath(self.path, brush)

            self.update()

    def mydestroy(self):
        self.path = QtGui.QPainterPath()
        self.pathhelper = QtGui.QPainterPath()
        self.strokeshelp.clear()
        self.hasWork = False
        self.image = self.layerCreate()
        self.update()

    def savePixels(self, filepath):
        with open(filepath, "w+"):
            self.image.save(filepath, "png")
        os.chmod(filepath, 0o777)

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
