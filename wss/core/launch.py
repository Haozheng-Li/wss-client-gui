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


from wss.accessories.cameras import get_camera_manager

import sys
from PySide2.QtWidgets import QApplication

from wss.core import settings
from wss.gui.launch import WSSMainWindow


class LaunchManager:
	def __init__(self):
		self.window = None
		self.app = None
		self.camera_manager = None

	def launch_wss(self):
		# self.launch_camera()
		self.launch_gui()

	def launch_camera(self):
		self.camera_manager = get_camera_manager()
		self.camera_manager.initialize_cameras(1)
		self.camera_manager.start_all()

	def launch_gui(self):
		self.app = QApplication(sys.argv)
		self.window = WSSMainWindow()
		self.window.show()
		sys.exit(self.app.exec_())


if __name__ == '__main__':
	launch_manager = LaunchManager()
	launch_manager.launch_wss()


