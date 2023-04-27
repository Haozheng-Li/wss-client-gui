# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/23
#
# A PyQt-based GUI library for WSS projects
# ============================================
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Copyright (c) 2023 Haozheng Li. All rights reserved.

from wss.core import settings

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SidebarButton(QFrame):
    clicked = Signal(object)

    def __init__(self, text, icon_path, icon_active_path, size=120, border_radius=30, can_be_selected=True):
        super(SidebarButton, self).__init__()
        self.button_logo = None
        self.button_text = None
        self.button_size = size
        self.border_radius = border_radius
        self.layout = None
        self.button = None
        self.bg_frame = None
        self.bg_layout = None
        self._is_active = False
        self._is_pressed = False

        self.text = text
        self.icon_path = icon_path
        self.icon_active_path = icon_active_path
        self.setup_ui()

        self.can_be_selected = can_be_selected

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName('sidebar_button_bg')
        self.bg_frame.setFixedSize(self.button_size, self.button_size)
        self.bg_frame.setStyleSheet(f"background:#2C313C; border-radius: {self.border_radius}px;")

        self.bg_layout = QVBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 20, 0, 20)
        self.bg_layout.setSpacing(5)

        self.layout.addWidget(self.bg_frame)

        if self.text:
            self.button_text = QLabel()
            self.button_text.setMaximumHeight(20)
            self.button_text.setStyleSheet("font: 12pt;color:#e5e8eb;")
            self.button_text.setText(self.text)
            self.bg_layout.addWidget(self.button_text, 0, Qt.AlignHCenter)

        self.button_logo = QLabel()
        self.button_logo.setFixedSize(27, 27)
        self.button_logo.setScaledContents(True)
        self.button_logo.setPixmap(QPixmap(self.icon_path))
        self.bg_layout.addWidget(self.button_logo, 0, Qt.AlignHCenter)

    def get_text(self):
        return self.text

    def update(self):
        if (self._is_active and self.can_be_selected) or self._is_pressed:
            if self.button_text:
                self.button_text.setStyleSheet("font: 12pt;color:#2C313C;")
            self.bg_frame.setStyleSheet(f"background:#f2fbf3; border-radius: {self.border_radius}px;")
            self.button_logo.setPixmap(QPixmap(self.icon_active_path))
        else:
            if self.button_text:
                self.button_text.setStyleSheet("font: 12pt;color:#f2fbf3;")
            self.bg_frame.setStyleSheet(f"background:#2C313C; border-radius: {self.border_radius}px;")
            self.button_logo.setPixmap(QPixmap(self.icon_path))

    def set_active(self):
        self._is_active = True
        self.update()

    def set_inactive(self):
        self._is_active = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_pressed = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._is_pressed:
            self._is_pressed = False
            self.clicked.emit(self)
            self.update()






