# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/21
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

from wss.model import wss_model


class WSSController:
	def __init__(self):
		pass

	def manage_accessories(self):
		wss_model.set_accessories_data({'name': 'USB Camera 0'})

