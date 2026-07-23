from PySide6 import QtWidgets
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect, QPoint

class RubberBand(QtWidgets.QRubberBand):
    def __init__(self, screenshot, arg__1=None, parent=None):
        super().__init__(arg__1, parent)

        self.screenshot = screenshot
        self.cropped_area = None
        self.ratio = self.screenshot.devicePixelRatioF()

    def paintEvent(self, event):
        # Overridden method to paint the content of rubberband with an image (background)
        if self.cropped_area is not None:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.cropped_area)

    def update_screenshot(self, p1, p2):
        """
        Update the positions of the 2 anchors of the image content of rubberband
        
        :param p1: Top left anchor
        :param p2: Bottom right anchor
        """
        rect = QRect(
            QPoint(int(p1.x() * self.ratio), int(p1.y() * self.ratio)),
            QPoint(int(p2.x() * self.ratio), int(p2.y() * self.ratio))
        ).normalized()
        self.cropped_area = self.screenshot.copy(rect)
        self.update()
