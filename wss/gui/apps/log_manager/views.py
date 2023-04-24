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
from wss.gui.style import theme

from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout

from wss.gui.widget.div import HorizontalDiv


class LogManagerView(QWidget):
    def __init__(self):
        super(LogManagerView, self).__init__()
        self.log_content_page = None
        self.log_content_page_layout = None
        self.title_div = None
        self.title = None
        self.bg_layout = None
        self.main_layout = None
        self.bg = None
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 5, 5, 5)
        self.main_layout.setSpacing(15)
        
        self.bg = QFrame()
        self.bg.setStyleSheet(f"background-color: {theme.BG_TWO}; border-radius: 8px;")
        self.bg_layout = QVBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(24, 24, 24, 24)
        self.bg_layout.setSpacing(15)
        self.main_layout.addWidget(self.bg)

        self.setup_title()
        
        self.setup_log_content()

    def setup_title(self):
        self.title = QLabel()
        self.title.setText('Camera Figure')
        self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
        self.title.setMaximumHeight(20)
        self.bg_layout.addWidget(self.title)

        self.title_div = HorizontalDiv(theme.DARK_FOUR)
        self.bg_layout.addWidget(self.title_div)
    
    def setup_log_content(self):
        self.log_content_page = QFrame()
        self.log_content_page_layout = QVBoxLayout(self.log_content_page)
        self.log_content_page_layout.setContentsMargins(0, 0, 0, 0)
        self.log_content_page_layout.setSpacing(0)
        
        self.bg_layout.addWidget(self.log_content_page)
        
