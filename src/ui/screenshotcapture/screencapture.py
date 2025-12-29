from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import QPainter
from ui.screenshotcapture.rubberband import RubberBand

class ScreenCapture(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        screen = QtWidgets.QApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)

        # RubberBand for selection
        self.rubberband = RubberBand(screenshot=self.screenshot, arg__1=QtWidgets.QRubberBand.Rectangle, parent=self)
        self.origin = QPoint()
    
    def paintEvent(self, event):
        painter = QPainter(self) 
        painter.setOpacity(0.5) 
        painter.drawPixmap(0, 0, self.screenshot)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QRect(self.origin, QSize()))
        self.rubberband.show()

    def mouseMoveEvent(self, event):
        self.rubberband.update_screenshot(self.origin, event.pos())
        self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        rect = self.rubberband.geometry()
        cropped = self.screenshot.copy(rect)
        cropped.save("snip.png")
        self.close()
