# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/18
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

import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class FramelessMainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self._is_frameless = True
		self.is_moving = False
		self.start_point = None
		self.mouse_drag_pos = QPoint()

		self.init_ui()

	def init_ui(self):
		self.refresh_frame()

		layout = QVBoxLayout()

		title_bar = QWidget()
		title_bar_layout = QHBoxLayout(title_bar)

		btn_close = QPushButton('Close')
		btn_minimize = QPushButton('Minimize')
		btn_maximize = QPushButton('Maximize')

		btn_close.clicked.connect(self.close)
		btn_minimize.clicked.connect(self.showMinimized)
		btn_maximize.clicked.connect(self.toggle_maximize_restore)

		title_bar_layout.addWidget(btn_close)
		title_bar_layout.addWidget(btn_minimize)
		title_bar_layout.addWidget(btn_maximize)

		layout.addWidget(title_bar)

		self.setLayout(layout)

	def set_frameless_status(self, status):
		self._is_frameless = status
		self.refresh_frame()

	def refresh_frame(self):
		if self._is_frameless:
			self.setWindowFlags(Qt.FramelessWindowHint)

	def set_ui(self):
		self.setWindowFlags(Qt.FramelessWindowHint)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.is_moving = True
			self.mouse_drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

	def mouseMoveEvent(self, event):
		if event.buttons() & Qt.LeftButton:
			self.move(event.globalPosition().toPoint() - self.mouse_drag_pos)

	def toggle_maximize_restore(self):
		if self.isMaximized():
			self.showNormal()
		else:
			self.showMaximized()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	frameless_window = FramelessMainWindow()
	frameless_window.show()
	sys.exit(app.exec())
