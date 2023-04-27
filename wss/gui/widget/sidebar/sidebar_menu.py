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
from PySide2.QtGui import QPixmap

from wss.core import settings
from wss.gui.style import theme
from wss.gui.widget.div import HorizontalDiv
from wss.gui.widget.sidebar.sidebar_button import SidebarButton

from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout
from PySide2.QtCore import Qt, Signal


class SidebarMenu(QWidget):
    sidebar_clicked = Signal(str)

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

        self.buttons = []

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.bg = QFrame()
        self.bg.setStyleSheet(f"background: {theme.DARK_TWO}; border-radius: 20;")

        self.bg_layout = QVBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_layout.setSpacing(50)
        
        self.setup_logo()

        self.sidebar_top_menu = QFrame()
        self.sidebar_top_layout = QVBoxLayout(self.sidebar_top_menu)
        self.sidebar_top_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_top_layout.setSpacing(40)

        self.sidebar_bottom_menu = QFrame()
        self.sidebar_bottom_layout = QVBoxLayout(self.sidebar_bottom_menu)
        self.sidebar_bottom_layout.setContentsMargins(0, 20, 0, 20)

        self.bg_layout.addWidget(self.sidebar_top_menu, 0, Qt.AlignTop)
        self.bg_layout.addWidget(self.sidebar_bottom_menu, 0, Qt.AlignBottom)

        self.main_layout.addWidget(self.bg)

        self.add_menu()

        self.setup_setting_button()
    
    def setup_logo(self):
        self.icon_frame = QFrame()
        self.icon_frame.setMaximumHeight(120)
        self.icon_frame_layout = QVBoxLayout(self.icon_frame)
        self.icon_frame_layout.setContentsMargins(0, 20, 0, 20)
        self.icon_frame_layout.setSpacing(20)
        self.bg_layout.addWidget(self.icon_frame)

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(str(settings.BASE_DIR / 'static/image/logo/logo-sm.png')))
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(48, 48)
        self.icon_frame_layout.addWidget(self.icon, 0, Qt.AlignHCenter)

        self.icon_div = HorizontalDiv()
        self.icon_frame_layout.addWidget(self.icon_div, 0, Qt.AlignVCenter)

    def add_menu(self):
        button = SidebarButton(text='Cameras',
                               icon_path=str(settings.BASE_DIR / 'static/image/icon/camera.png'),
                               icon_active_path=str(settings.BASE_DIR / 'static/image/icon/camera-active.png'),
                               size=100)
        button2 = SidebarButton(text='Logs',
                                icon_path=str(settings.BASE_DIR / 'static/image/icon/logs.png'),
                                icon_active_path=str(settings.BASE_DIR / 'static/image/icon/logs-active.png'),
                                size=100)
        self.buttons.append(button)
        self.buttons.append(button2)
        button.set_active()
        button.clicked.connect(self.sidebar_button_clicked)
        button2.clicked.connect(self.sidebar_button_clicked)
        self.sidebar_top_layout.addWidget(button)
        self.sidebar_top_layout.addWidget(button2)

    def setup_setting_button(self):
        button = SidebarButton(text='',
                               icon_path=str(settings.BASE_DIR / 'static/image/icon/settings.png'),
                               icon_active_path=str(settings.BASE_DIR / 'static/image/icon/settings-active.png'),
                               size=60, border_radius=20, can_be_selected=False)
        self.sidebar_bottom_layout.addWidget(button)

    def sidebar_button_clicked(self, clicked_button):
        for button in self.buttons:
            if button == clicked_button:
                button.set_active()
            else:
                button.set_inactive()

        self.sidebar_clicked.emit(clicked_button.get_text())

