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

from wss.core import settings
from wss.gui.style import theme
from wss.gui.widget.div import HorizontalDiv

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget


class AccessoriesView(QWidget):
	def __init__(self):
		super().__init__()

		self.accessories_container = None
		self.title_div = None
		self.title = None
		self.layout = None
		self.parent = None
		
	def setup_title(self):
		self.title = QLabel()
		self.title.setText('Accessories')
		self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
		self.layout.addWidget(self.title)

		self.title_div = HorizontalDiv(theme.DARK_FOUR)
		self.layout.addWidget(self.title_div)

	def setup_ui(self):
		self.setObjectName('accessories')
		
		self.layout = QVBoxLayout(self)
		self.layout.setSpacing(15)
		self.layout.setObjectName(u"layout")
		self.layout.setContentsMargins(12, 12, 12, 12)
		
		self.setup_title()

		self.accessories_container = QListWidget(self)
		self.accessories_container.setStyleSheet(f"background-color: {theme.BG_TWO}; border-radius: 8px;")
		self.accessories_container.setObjectName(u"accessories_container")

		self.layout.addWidget(self.accessories_container)

	def add_accessory(self, item):
		self.accessories_container.addItem(item)


class AccessoryBox(QWidget):
	def __init__(self):
		super(AccessoryBox, self).__init__()

	def setup_ui(self):
		pass
