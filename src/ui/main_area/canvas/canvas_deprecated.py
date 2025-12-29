from PySide6 import QtWidgets
from PySide6.QtCore import Qt

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Init the Graphics Scene and add a pixmap selector to it
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addItem(self.pixmap)
        self.setScene(self.scene)

    def display_pixmap(self, pixmap):
        self.pixmap.setPixmap(pixmap)
        self.fitInView(self.pixmap, Qt.KeepAspectRatio)

    # def resizeEvent(self, event):
    #     """Ensure the pixmap always fits when the view is resized."""
    #     super().resizeEvent(event)
    #     if not self.pixmap.pixmap().isNull():
    #         self.fitInView(self.pixmap, Qt.KeepAspectRatio)


