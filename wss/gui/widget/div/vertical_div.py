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

from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame


class VerticalDiv(QWidget):
	def __init__(self, color):
		super(VerticalDiv, self).__init__()
		self.layout = None
		self.line = None
		self.color = color
		self.setup_ui()

	def setup_ui(self):
		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(0, 5, 0, 5)
		self.line = QFrame()
		self.line.setStyleSheet(f"background: {self.color};")
		self.line.setMaximumWidth(1)
		self.line.setMinimumWidth(1)
		self.layout.addWidget(self.line)
		self.setMaximumWidth(20)
		self.setMinimumWidth(20)