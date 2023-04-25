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


class WSSModel:
	def __init__(self):
		self.callbacks = {}
		self.accessories_data = []
		self.logs_data = []

	def set_accessories_data(self, data):
		self.accessories_data = data
		self.emit_signal('accessories_data')

	def register_callback(self, data_name, func):
		if not self.callbacks.get(data_name, None):
			self.callbacks[data_name] = [func]
		else:
			self.callbacks[data_name].append(func)

	def emit_signal(self, data_name):
		callback_funcs = self.callbacks.get(data_name)
		if callback_funcs:
			callback_funcs(getattr(self, data_name))


wss_model = WSSModel()
