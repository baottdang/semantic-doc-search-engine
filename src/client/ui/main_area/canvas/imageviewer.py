# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import (QMenuBar, QDialog, QFileDialog, QLabel,
                               QWidget, QMessageBox, QScrollArea,
                               QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton)
from PySide6.QtGui import (QColorSpace, QGuiApplication,
                           QImageReader, QImageWriter, QKeySequence,
                           QPalette, QPainter, QPixmap)
from PySide6.QtCore import QDir, QStandardPaths, Qt, Slot
from ui.main_area.canvas.canvas_graphicsview import Canvas

class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale_factor = 1.0
        self._first_file_dialog = True
        self._canvas = Canvas(self)

        self._canvas.setBackgroundRole(QPalette.ColorRole.Base)
        self._canvas.setSizePolicy(QSizePolicy.Policy.Ignored,
                                        QSizePolicy.Policy.Ignored)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._create_actions()

    def _set_image(self, new_image):
        self._image = new_image
        if new_image is not None:
            if self._image.colorSpace().isValid():
                color_space = QColorSpace(QColorSpace.NamedColorSpace.SRgb)
                self._image.convertToColorSpace(color_space)
            self._print_act.setEnabled(True)
            self._canvas.display_pixmap(QPixmap.fromImage(self._image))
            self._scale_factor = 1.0
            self._update_actions()
        else:
            self._clear_image()

    def _clear_image(self):
        self._image = None
        self._canvas.clear_image()
        self._print_act.setEnabled(False)
        self._update_actions()

    def _save_file(self, fileName):
        writer = QImageWriter(fileName)

        native_filename = QDir.toNativeSeparators(fileName)
        if not writer.write(self._image):
            error = writer.errorString()
            message = f"Cannot write {native_filename}: {error}"
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                    message)
            return False
        return True

    @Slot()
    def _save_as(self):
        dialog = QFileDialog(self, "Save File As")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptMode.AcceptSave)
        while (dialog.exec() == QDialog.DialogCode.Accepted
               and not self._save_file(dialog.selectedFiles()[0])):
            pass

    @Slot()
    def _print_(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            with QPainter(printer) as painter:
                pixmap = self._canvas.pixmap()
                rect = painter.viewport()
                size = pixmap.size()
                size.scale(rect.size(), Qt.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(pixmap.rect())
                painter.drawPixmap(0, 0, pixmap)

    @Slot()
    def _copy(self):
        QGuiApplication.clipboard().setImage(self._image)

    @Slot()
    def _zoom_in(self):
        self._canvas.zoom_in(1.25, 5)

    @Slot()
    def _zoom_out(self):
        self._canvas.zoom_out(0.8, -5)

    @Slot()
    def _fit_to_window(self):
        self._canvas.reset_view()
        self._scale_factor = 1.0

    def _create_actions(self):
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("&File")

        self._save_as_act = file_menu.addAction("&Save As...")
        self._save_as_act.triggered.connect(self._save_as)
        self._save_as_act.setEnabled(False)

        self._print_act = file_menu.addAction("&Print...")
        self._print_act.triggered.connect(self._print_)
        self._print_act.setShortcut(QKeySequence.StandardKey.Print)
        self._print_act.setEnabled(False)

        file_menu.addSeparator()

        edit_menu = self.menu_bar.addMenu("&Edit")

        self._copy_act = edit_menu.addAction("&Copy")
        self._copy_act.triggered.connect(self._copy)
        self._copy_act.setShortcut(QKeySequence.StandardKey.Copy)
        self._copy_act.setEnabled(False)

        self._zoom_in_act = QPushButton("Zoom &In (25%)")
        self._zoom_in_act.setShortcut(QKeySequence.StandardKey.ZoomIn)
        self._zoom_in_act.clicked.connect(self._zoom_in)
        self._zoom_in_act.setEnabled(False)

        self._zoom_out_act = QPushButton("Zoom &Out (25%)")
        self._zoom_out_act.clicked.connect(self._zoom_out)
        self._zoom_out_act.setShortcut(QKeySequence.StandardKey.ZoomOut)
        self._zoom_out_act.setEnabled(False)

        self._fit_to_window_act = QPushButton("&Fit to Window")
        self._fit_to_window_act.clicked.connect(self._fit_to_window)
        self._fit_to_window_act.setShortcut("Ctrl+S")
        self._fit_to_window_act.setEnabled(False)

        edit_layout = QHBoxLayout()

        edit_layout.addWidget(self._zoom_in_act)
        edit_layout.addWidget(self._zoom_out_act)
        edit_layout.addWidget(self._fit_to_window_act)

        self.layout.setMenuBar(self.menu_bar)
        self.layout.addLayout(edit_layout)
        self.layout.addWidget(self._canvas)

    def _update_actions(self):
        has_image = not self._image is None
        self._save_as_act.setEnabled(has_image)
        self._copy_act.setEnabled(has_image)
        
        self._zoom_in_act.setEnabled(has_image)
        self._zoom_out_act.setEnabled(has_image)
        self._fit_to_window_act.setEnabled(has_image)

    def _adjust_scrollbar(self, scrollBar, factor):
        pos = int(factor * scrollBar.value()
                  + ((factor - 1) * scrollBar.pageStep() / 2))
        scrollBar.setValue(pos)

    def _initialize_image_filedialog(self, dialog, acceptMode):
        if self._first_file_dialog:
            self._first_file_dialog = False
            locations = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.PicturesLocation)  # noqa: E501
            directory = locations[-1] if locations else QDir.currentPath()
            dialog.setDirectory(directory)

        mime_types = [m.data().decode('utf-8') for m in QImageWriter.supportedMimeTypes()]
        mime_types.sort()

        dialog.setMimeTypeFilters(mime_types)
        dialog.selectMimeTypeFilter("image/jpeg")
        dialog.setAcceptMode(acceptMode)
        if acceptMode == QFileDialog.AcceptMode.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    def update_scale_image(self):
        self._canvas.update_scale_image()

    def is_empty(self):
        return self._canvas.is_empty() 