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

	NO_INTRUDER = 1
	INTRUDER_PASSING_BY = 2
	INTRUDER_APPROACHING = 3
	INTRUDER_MOVING_CLOSER = 4

	CALLBACK_TYPE = [
		'intruder_status',
		'intruder_detect_logs',
		'detector_status',
	]

	def __init__(self):
		self.intruder_status = self.NO_INTRUDER
		self.detector_status = True
		self.callback_funcs = {}
		self.intruder_detect_logs = []

	def set_detector_status(self, status):
		self.detector_status = status
		self.raise_callback('detector_status', status)
		print('Detector status change to {}'.format(status))

	def set_intruder_status(self, status: int):
		if status not in range(1, 5):
			raise ValueError('Intruder status should be in 1 to 4.')
		if status != self.intruder_status:
			print('Intruder status change to {}'.format(status))
			self.intruder_status = status
			self.raise_callback('intruder_status', status)

	def set_intruder_detect_log(self, log_data):
		self.intruder_detect_logs.append(log_data)
		print('New Intruder detect log {}'.format(log_data))
		self.raise_callback('intruder_detect_logs', log_data)

	def raise_callback(self, callback_type, data):
		if callback_type not in self.CALLBACK_TYPE or callback_type not in self.callback_funcs:
			return

		for func in self.callback_funcs[callback_type]:
			func(data)

	def get_intruder_status(self):
		return self.intruder_status

	def register_callback(self, callback_type, func):
		if callback_type not in self.CALLBACK_TYPE:
			return

		if callback_type not in self.callback_funcs:
			self.callback_funcs[callback_type] = [func]
		else:
			self.callback_funcs[callback_type].append(func)


wss_model = WSSModel()
