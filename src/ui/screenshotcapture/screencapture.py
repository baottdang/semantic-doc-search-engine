from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter
from ui.screenshotcapture.rubberband import RubberBand
from ui.screenshotcapture.screencapture_signal import get_screencapture_signal_instance

class ScreenCapture(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        screen = QtWidgets.QApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)

        # RubberBand for selection
        self.rubberband = RubberBand(screenshot=self.screenshot, arg__1=QtWidgets.QRubberBand.Rectangle, parent=self)
        self.origin = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    
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
        screencapture_signal_instance = get_screencapture_signal_instance()
        screencapture_signal_instance.capture_done_signal.emit(cropped.toImage())
        self.close()
