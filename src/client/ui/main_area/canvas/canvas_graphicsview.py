from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QWheelEvent

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Init the Graphics Scene and add a pixmap selector to it
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

    def display_pixmap(self, pixmap):
        self.pixmap.setPixmap(pixmap)

        self.scene.setSceneRect(self.pixmap.boundingRect())

        self._zoom = 0
        self.resetTransform()

        self.fitInView(self.pixmap, Qt.KeepAspectRatio)

    def is_empty(self):
        return self.pixmap.pixmap().isNull()
    
    def clear_image(self):
        self.pixmap.setPixmap(QPixmap())

    def reset_view(self):
        self.fitInView(self.pixmap, Qt.KeepAspectRatio)
        self._zoom = 0

    def zoom_in(self, factor, limit):
        if self._zoom <= limit:
            self._zoom += 1
        else:
            return
        self.scale(factor, factor)

    def zoom_out(self, factor, limit):
        if self._zoom >= limit:
            self._zoom -= 1
        else:
            return

        self.scale(factor, factor)

    def update_scale_image(self):
        """Ensure the pixmap always fits when the view is resized."""
        self.setSceneRect(self.rect())
        if not self.pixmap.pixmap().isNull():
            self.pixmap.pixmap().scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)