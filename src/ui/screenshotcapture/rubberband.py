from PySide6 import QtWidgets
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect

class RubberBand(QtWidgets.QRubberBand):
    def __init__(self, screenshot, arg__1=None, parent=None):
        super().__init__(arg__1, parent)

        self.screenshot = screenshot
        self.cropped_area = None

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
        self.cropped_area = self.screenshot.copy(QRect(p1, p2).normalized())
        self.update()
