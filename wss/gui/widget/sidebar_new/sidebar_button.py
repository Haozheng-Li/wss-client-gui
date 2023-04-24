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

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SidebarButton(QFrame):
    clicked = Signal(object)

    def __init__(self, size=120):
        super(SidebarButton, self).__init__()
        self.icon_path = None
        self.button_logo = None
        self.button_text = None
        self.button_size = size
        self.layout = None
        self.button = None
        self.bg_frame = None
        self.bg_layout = None
        self._is_active = False
        self._is_pressed = False
        self.text = ''
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName('sidebar_button_bg')
        self.bg_frame.setFixedSize(self.button_size, self.button_size)
        self.bg_frame.setStyleSheet("background:#33383c; border-radius: 30px;")

        self.bg_layout = QVBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 20, 0, 20)
        self.bg_layout.setSpacing(0)

        self.layout.addWidget(self.bg_frame)

        self.button_text = QLabel()
        self.button_text.setMaximumHeight(20)
        self.button_text.setStyleSheet("font: 12pt;color:#e5e8eb;")
        self.bg_layout.addWidget(self.button_text, 0, Qt.AlignHCenter)

        self.button_logo = QLabel()
        self.button_logo.setFixedSize(40, 40)
        self.button_logo.setScaledContents(True)
        self.button_logo.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/icon/camera.png'))
        self.bg_layout.addWidget(self.button_logo, 0, Qt.AlignHCenter)
    
    def set_data(self, data):
        self.text = data.get('text', '')
        self.icon_path = data.get('icon_path', '')

        self.button_logo.setPixmap(QPixmap(self.icon_path))
        self.button_text.setText(self.text)

    def get_text(self):
        return self.text

    def update(self):
        if self._is_active or self._is_pressed:
            self.button_text.setStyleSheet("font: 15pt;color:#393b3c;")
            self.bg_frame.setStyleSheet("background:#f2fbf3; border-radius: 30px;")
            self.button_logo.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/icon/camera-active.png'))
        else:
            self.button_text.setStyleSheet("font: 15pt;color:#e5e8eb;")
            self.bg_frame.setStyleSheet("background:#33383c; border-radius: 30px;")
            self.button_logo.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/icon/camera.png'))

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






