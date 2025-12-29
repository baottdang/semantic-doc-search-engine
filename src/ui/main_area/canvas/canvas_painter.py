from PySide6 import QtWidgets
from PySide6.QtGui import QPainter
from PySide6.QtCore import QPoint, Qt

class CanvasPainter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Components
        self.image = None
        self.anchor_image = None

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def paintEvent(self, event):
        if self.image:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Getting the center of canvas
            canvas_w = self.width()
            canvas_h = self.height()
            image_w = self.image.width()
            image_h = self.image.height()

            # Update anchor
            anchor_x = (canvas_w - image_w) // 2
            anchor_y = (canvas_h - image_h) // 2

            painter.drawImage(QPoint(anchor_x, anchor_y), self.image)

    def update_scale_image(self):
        if self.image:
            self.image = self.anchor_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation)

    def update_image(self, qimage):
        """
        Update the image of this canvas

        :param qimage: QImage instance 
        """
        # Update anchor and image
        self.image = qimage
        self.anchor_image = qimage

        # Signal redraw
        self.update() # This is recommended over calling repaint(), see the docs on QtWidget for details

    def is_empty(self):
        return self.image is None