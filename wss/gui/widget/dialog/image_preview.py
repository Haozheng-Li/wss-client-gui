# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/27
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

from PySide2.QtWidgets import QVBoxLayout, QLabel, QDialog, QApplication
from PySide2.QtGui import QPixmap


class ResourcePreviewDialog(QDialog):
	def __init__(self, image_path):
		super(ResourcePreviewDialog, self).__init__()

		self.content_layout = None
		self.image_label = None

		self.image_path = image_path
		self.setup_ui()
		self.center()

	def setup_ui(self):
		self.setWindowTitle('Resource Preview')
		self.setGeometry(100, 100, 400, 300)

		self.content_layout = QVBoxLayout(self)

		self.image_label = QLabel(self)

		self.image_label.setPixmap(QPixmap(self.image_path))
		self.image_label.setScaledContents(True)

		self.content_layout.addWidget(self.image_label)

	def focusOutEvent(self, event):
		self.close()

	def center(self):
		screen_geometry = QApplication.desktop().screenGeometry()
		window_geometry = self.geometry()
		x = (screen_geometry.width() - window_geometry.width()) / 2 + screen_geometry.left()
		y = (screen_geometry.height() - window_geometry.height()) / 2 + screen_geometry.top()
		self.move(x, y)

