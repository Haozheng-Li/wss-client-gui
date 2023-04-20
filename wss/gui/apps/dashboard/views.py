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
from wss.gui.widget.div import HorizontalDiv

from PySide6.QtWidgets import (QLabel, QScrollArea, QVBoxLayout, QWidget, QListWidget)


class UiAccessories(QWidget):
	
	def __init__(self):
		super().__init__()

		self.accessories_container = None
		self.title_div = None
		self.title = None
		self.layout = None
		self.parent = None
		
	def setup_title(self):
		self.title = QLabel()
		self.title.setObjectName(u"label")
		self.layout.addWidget(self.title)

		self.title_div = HorizontalDiv(theme.DARK_FOUR)
		self.layout.addWidget(self.title_div)

	def setup_ui(self, parent):
		self.setObjectName('accessories')
		
		self.layout = QVBoxLayout(parent)
		self.layout.setSpacing(15)
		self.layout.setObjectName(u"layout")
		self.layout.setContentsMargins(12, 0, 0, 12)
		
		self.setup_title()

		self.accessories_container = QListWidget(parent)
		self.accessories_container.setObjectName(u"accessories_container")

		# self.scrollAreaWidgetContents = QWidget()
		# self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
		# self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 217, 530))
		# self.accessories_container.setWidget(self.scrollAreaWidgetContents)

		self.layout.addWidget(self.accessories_container)

