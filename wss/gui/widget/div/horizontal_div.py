# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/20
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
from PySide2.QtWidgets import QWidget, QHBoxLayout, QFrame


class HorizontalDiv(QWidget):
	def __init__(self, color=theme.DARK_FOUR):
		super(HorizontalDiv, self).__init__()
		self.layout = None
		self.line = None
		self.color = color
		self.setup_ui()
	
	def setup_ui(self):
		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(5, 0, 5, 0)
		self.line = QFrame()
		self.line.setStyleSheet(f"background: {self.color};")
		self.line.setMaximumHeight(1)
		self.line.setMinimumHeight(1)
		self.layout.addWidget(self.line)
		self.setMaximumHeight(1)
