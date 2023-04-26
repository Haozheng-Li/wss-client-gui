# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/25
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


class WSSModel:
	def __init__(self):
		self.intruder_detect_data = []

	def set_intruder_detect_data(self, data):
		self.intruder_detect_data.append(data)

