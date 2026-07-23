from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QCursor
from ui.screenshotcapture.rubberband import RubberBand
import mss, cv2
import numpy as np

class ScreenCapture(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        screen = QtWidgets.QApplication.screenAt(QCursor.pos())
        self.screenshot_full = screen.grabWindow(0)

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            self.screenshot_full_mss = cv2.cvtColor(np.array(sct.grab(monitor))[:, :, :3], cv2.COLOR_BGR2RGB) # RGB

        # RubberBand for selection
        self.rubberband = RubberBand(screenshot=self.screenshot_full, arg__1=QtWidgets.QRubberBand.Rectangle, parent=self)
        self.origin = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ratio = self.screenshot_full.devicePixelRatioF()

    def paintEvent(self, event):
        painter = QPainter(self) 
        painter.setOpacity(0.5) 
        painter.drawPixmap(0, 0, self.screenshot_full)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QRect(self.origin, QSize()))
        self.rubberband.show()

    def mouseMoveEvent(self, event):
        self.rubberband.update_screenshot(self.origin, event.pos())
        self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        rect = self.rubberband.geometry()

        x1 = round(rect.left() * self.ratio)
        y1 = round(rect.top() * self.ratio)

        x2 = round((rect.left() + rect.width()) * self.ratio)
        y2 = round((rect.top() + rect.height()) * self.ratio)

        self.capture = np.ascontiguousarray(
            self.screenshot_full_mss[y1:y2, x1:x2]
        )
        self.close()

    def get_capture(self, tries=0):
        # if self.capture is not None:
            return self.capture
        # elif tries < 3:
        #     time.sleep(0.5)
        #     tries += 1
        #     return self.get_capture(tries)
        # else:
        #     return None
