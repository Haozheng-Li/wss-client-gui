# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/19
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
from PySide6.QtGui import QPixmap

from wss.core import settings
from wss.gui.style import theme
from wss.gui.widget.sidebar_new.sidebar_button import SidebarButton

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class SidebarMenu(QWidget):
    def __init__(self):
        super(SidebarMenu, self).__init__()
        self.icon_frame_layout = None
        self.icon_frame = None
        self.icon = None
        self.bg_layout = None
        self.bg = None
        self.sidebar_bottom_menu = None
        self.sidebar_top_menu = None
        self.sidebar_bottom_layout = None
        self.sidebar_top_layout = None
        self.main_layout = None

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.bg = QFrame()
        self.bg.setStyleSheet(f"background: {theme.DARK_ONE}; border-radius: 8;")

        self.bg_layout = QVBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_logo()

        self.sidebar_top_menu = QFrame()
        self.sidebar_top_layout = QVBoxLayout(self.sidebar_top_menu)
        self.sidebar_top_layout.setContentsMargins(0, 30, 0, 20)
        self.sidebar_top_layout.setSpacing(20)

        self.sidebar_bottom_menu = QFrame()
        self.sidebar_bottom_menu.setStyleSheet("background:#00ff00")
        self.sidebar_bottom_layout = QVBoxLayout(self.sidebar_bottom_menu)
        self.sidebar_bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_layout.addWidget(self.sidebar_top_menu, 0, Qt.AlignTop)
        self.bg_layout.addWidget(self.sidebar_bottom_menu, 0, Qt.AlignBottom)

        self.main_layout.addWidget(self.bg)

        self.add_menu()
    
    def setup_logo(self):
        self.icon_frame = QFrame()
        self.icon_frame.setMaximumHeight(90)
        self.icon_frame_layout = QHBoxLayout(self.icon_frame)
        self.icon_frame_layout.setContentsMargins(0, 3, 0, 3)
        self.icon_frame_layout.setSpacing(10)
        self.bg_layout.addWidget(self.icon_frame)

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/logo/logo-sm.png'))
        self.icon.setScaledContents(True)
        self.icon.setMaximumSize(60, 60)
        self.icon.setMinimumSize(60, 60)
        self.icon_frame_layout.addWidget(self.icon, 0, Qt.AlignVCenter)

    def add_menu(self):
        button = SidebarButton()
        button2 = SidebarButton()
        self.sidebar_top_layout.addWidget(button)
        self.sidebar_top_layout.addWidget(button2)

    def add_menus(self, data):
        pass