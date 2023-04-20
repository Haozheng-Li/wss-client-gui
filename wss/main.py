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

import sys
from PySide6.QtWidgets import QApplication

from wss.core import settings
from wss.gui import WSSMainWindow

if settings.USE_GUI:
	app = QApplication(sys.argv)
	window = WSSMainWindow()
	window.show()
	sys.exit(app.exec())
else:
	pass
