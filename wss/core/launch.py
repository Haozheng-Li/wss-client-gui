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

import base64
import sys

from PySide2.QtWidgets import QApplication

from wss.core import settings
from wss.core.model import wss_model
from wss.gui import WSSMainWindow
from wss.profiler import AsyncProfiler
from wss.net import AsyncWebsocketClient
from wss.detector import IntruderDetector
from wss.accessories.cameras import get_camera_manager


class LaunchManager:
	def __init__(self):
		self.profiler = None
		self.gui = None
		self.gui_app = None
		self.net_client = None
		self.camera_manager = None
		self.camera_detector = None
		self._accept_operation_command = False

	def launch_net_client(self):
		self.net_client = AsyncWebsocketClient(settings.WSS_CONNECTION_URL.format(api_key=settings.WSS_SECRET_KEY))
		self.net_client.register_message_callback(self.on_receive_message)
		self.net_client.connect()

	def init_callback(self):
		wss_model.register_callback('intruder_detect_logs', self.on_detect_event_change)

	def init_profiler(self):
		self.profiler = AsyncProfiler()
		self.profiler.register_callback(self.on_profiler_update)
		self.profiler.start()

	def launch_wss(self):
		# self.launch_net_client()
		# self.init_profiler()
		self.launch_camera()
		self.launch_camera_detector()
		self.launch_gui()

	def launch_camera(self):
		self.camera_manager = get_camera_manager()
		self.camera_manager.initialize_cameras(self.camera_manager.detect_cameras())
		self.camera_manager.start_all()

	def launch_camera_detector(self):
		self.camera_detector = IntruderDetector(save_path=str(settings.BASE_DIR / 'output'))
		self.camera_detector.register_callback(self.on_detect_event_change)
		self.camera_manager.set_detector(self.camera_detector)

	def launch_gui(self):
		self.gui_app = QApplication(sys.argv)
		self.gui = WSSMainWindow()
		self.gui.show()
		sys.exit(self.gui_app.exec_())

	def on_profiler_update(self, data):
		print(data)
		return
		self.net_client.send(data, 'profiler')

	def enable_detection(self, operation, feedback=True):
		if operation == 'enable':
			self.camera_manager.start_all()
		else:
			self.camera_manager.stop_all()

		print(operation + ' detection')
		if feedback:
			self.net_client.send({'operation_type': 'intruder_detection', 'operation': operation},
			          message_type='operation_feedback')

	def enable_profiler(self, operation, feedback=True):
		if operation == 'enable':
			self.profiler.start()
		else:
			self.profiler.stop()

		print(operation + ' profiler')
		if feedback:
			self.net_client.send({'operation_type': 'profiler', 'operation': operation}, message_type='operation_feedback')

	def on_receive_message(self, data):
		message = data.get('message', '')
		message_type = data.get('message_type', '')

		if message_type == 'init':
			self.on_system_init_message(message)
		elif message_type == 'operation':
			self.on_operation_message(message)
	
	def on_system_init_message(self, message):
		operation = message.get('operation', '')
		operation_type = message.get('operation_type', '')

		if operation_type == 'profiler':
			self.enable_profiler(operation, feedback=False)
		elif operation_type == 'intruder_detection':
			self.enable_detection(operation, feedback=False)

	def on_operation_message(self, message):
		if not self._accept_operation_command:
			return

		operation = message.get('operation', '')
		operation_type = message.get('operation_type', '')

		if operation_type == 'profiler':
			self.enable_profiler(operation)
		elif operation_type == 'intruder_detection':
			self.enable_detection(operation)
		elif operation_type == 'restart':
			self.restart()

	def restart(self):
		print("Received restart message")
		self.net_client.send({'operation_type': 'restart', 'operation': ''}, message_type='operation_feedback')

	def on_detect_event_change(self, data):
		print('detect event', data)
		return
		path = data.get('path', '')
		intruder_type = data.get('intruder_type', 0)

		if path and intruder_type:
			message = {'intruder_type': intruder_type, 'data_type': 'image',
			           'data_file': None, 'data_file_name': path.replace('output/', '')}
			with open(path, "rb") as f:
				image_data = base64.b64encode(f.read()).decode("utf-8")
				message['data_file'] = image_data
			self.net_client.send(message=message, message_type='detect_event')


if __name__ == '__main__':
	launch_manager = LaunchManager()
	launch_manager.launch_wss()


