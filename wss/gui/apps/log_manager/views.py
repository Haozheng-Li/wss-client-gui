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

from PySide6.QtWidgets import QWidget


class LogManagerView(QWidget):
    def __init__(self):
        super(LogManagerView, self).__init__()
