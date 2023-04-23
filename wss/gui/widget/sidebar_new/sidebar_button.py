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

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SidebarButton(QFrame):
    def __init__(self):
        super(SidebarButton, self).__init__()
        self.layout = None
        self.button = None
        self.bg_frame = None
        self.bg_layout = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName('sidebar_button_bg')
        self.bg_frame.setFixedSize(120, 120)
        self.bg_frame.setStyleSheet("background:#33383c; border-radius: 30px;")

        self.bg_layout = QVBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 20, 0, 20)
        self.bg_layout.setSpacing(0)

        self.layout.addWidget(self.bg_frame)

        self.button_name = QLabel()
        self.button_name.setMaximumHeight(20)
        self.button_name.setStyleSheet("font: 15pt;color:#e5e8eb;")
        self.button_name.setText("Cameras")
        self.bg_layout.addWidget(self.button_name, 0, Qt.AlignHCenter)

        self.button_logo = QLabel()
        self.button_logo.setFixedSize(40, 40)
        self.button_logo.setScaledContents(True)
        self.button_logo.setStyleSheet("color:#fff")
        self.button_logo.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/icon/camera.png'))
        self.bg_layout.addWidget(self.button_logo, 0, Qt.AlignHCenter)





