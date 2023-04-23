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

from wss.gui.style import theme

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class SidebarMenu(QWidget):
    def __init__(self):
        super(SidebarMenu, self).__init__()
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

        self.sidebar_top_menu = QFrame()
        self.sidebar_top_layout = QVBoxLayout(self.sidebar_top_menu)
        self.sidebar_top_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar_bottom_menu = QFrame()
        self.sidebar_bottom_layout = QVBoxLayout(self.sidebar_bottom_menu)
        self.sidebar_bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_layout.addWidget(self.sidebar_top_menu, 0, Qt.AlignTop)
        self.bg_layout.addWidget(self.sidebar_bottom_menu, 0, Qt.AlignBottom)

        self.main_layout.addWidget(self.bg)

    def add_menus(self, menus):
        pass
