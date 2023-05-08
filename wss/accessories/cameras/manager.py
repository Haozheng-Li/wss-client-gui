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

import cv2
import numpy as np

from wss.accessories.cameras.base import CameraBase
from wss.accessories.cameras.expections import CameraDostNotExist, CameraRunningModeError


__all__ = ['get_camera_manager']

from wss.detector import IntruderDetector

CAMERA_MANAGER = None


def get_camera_manager():
	"""
	Singleton patterns to make sure each camera manager instance are the same one
	:return:
	"""
	global CAMERA_MANAGER
	if not CAMERA_MANAGER:
		CAMERA_MANAGER = CameraManager()
	return CAMERA_MANAGER


class CameraManager:
	MODE_PULLING = 1
	MODE_PARALLEL = 2

	def __init__(self) -> None:
		# Camera Objects
		self._cameras = []
		self.activated_cameras = []

		# Camera manager running mode
		self._running_mode = self.MODE_PULLING
		
		# Camera show
		self._show_status = False
		self._show_thread = None

		self.available_cameras_id = None

		self.camera_started = False

	def get_available_cameras_id(self, max_cameras=4):
		"""
		Get all available cameras on device (Below max_cameras)
		:param max_cameras:
		:return:
		"""
		if self.available_cameras_id is not None:
			return self.available_cameras_id

		self.available_cameras_id = []

		for camera_id in range(max_cameras):
			cap = cv2.VideoCapture(camera_id, cv2.CAP_ANY)

			if cap is None or not cap.isOpened():
				cap.release()
				break
			else:
				self.available_cameras_id.append(camera_id)
				cap.release()
		return self.available_cameras_id
		
	def _camera_init(self, camera_id) -> object:
		camera = CameraBase(camera_id)
		self._cameras.append(camera)
		print("Camera manager - Init cameras: id {}".format(camera_id))
		return camera

	def initialize_cameras(self, cameras_id) -> None:
		"""
		Initialize camera and camera instance
		:param cameras_id:
		:return:
		"""
		for camera_id in cameras_id:
			self._camera_init(camera_id)

	def get_camera_start_status(self):
		"""
		Get camera running status
		:return:
		"""
		return self.camera_started

	def _stop_camera(self, camera_obj) -> None:
		if camera_obj:
			camera_obj.stop()
			camera_obj.release()
			print("Camera manager - Stop cameras: id {}".format(camera_obj.camera_id))

	def _start_camera(self, camera_obj) -> None:
		self.camera_started = True
		if camera_obj:
			camera_obj.start(camera_obj.get_camera_id())
			print("Camera manager - Start cameras: id {}".format(camera_obj.camera_id))

	def set_camera_properties(self, width, height, codec, fps):
		"""
		Set camera running properties
		:param width: Camera frame width
		:param height: Camera frame height
		:param codec: Camera frame codec
		:param fps: Camera frame fps
		:return:
		"""
		for camera in self._cameras:
			camera.set_properties(width, height, codec, fps)

	def start_camera_by_id(self, camera_id):
		"""
		Start one camera
		:param camera_id:
		:return:
		"""
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._start_camera(camera)

	def stop_camera_by_id(self, camera_id):
		"""
		Stop one camera
		:param camera_id:
		:return:
		"""
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._stop_camera(camera)

	def start_all(self) -> None:
		"""
		Start all available cameras
		:return:
		"""
		for camera in self._cameras:
			self._start_camera(camera)

	def stop_all(self) -> None:
		"""
		Stop all camera
		:return:
		"""
		for camera in self._cameras:
			self._stop_camera(camera)

	def get_camera_by_id(self, camera_id: int) -> object:
		"""
		Get camera instance by camera_id
		:param camera_id:
		:return:
		"""
		for camera in self._cameras:
			if camera.camera_id == camera_id:
				return camera
		raise CameraDostNotExist('Camera id {} does not exist'.format(camera_id))

	def get_all_cameras(self) -> list:
		"""
		Get all camera instances
		:return:
		"""
		return self._cameras

	def get_mode(self) -> int:
		"""
		Get current running mode
		:return:
		"""
		return self._running_mode

	def switch_mode(self, mode) -> None:
		"""
		Switch camera manager running mode (Pulling Mode or Parallel Mode)
		:param mode:
		:return:
		"""
		self._running_mode = mode
		print("Camera Manager - Change running mode: from mode{} to mode {}".format(self._running_mode, mode))

	def switch_camera(self, camera_id) -> None:
		"""
		Switch current camera for Pulling Mode
		:param camera_id: The id of the camera which will be set to current camera
		:return:
		"""
		if self._running_mode != self.MODE_PULLING:
			raise CameraRunningModeError("Switch cameras should be running in pulling mode!")
		camera = self.get_camera_by_id(camera_id)
		camera.start()
		self.activated_cameras.append(camera)

	def get_merge_frame(self, show_time=False, show_fps=False):
		"""
		Get cameras merge frame data
		:param show_time: show time of the camera in camera frame data
		:param show_fps: show fps of the camera in camera frame data
		:return:
		"""
		cameras_merge_frame = None
		for index, camera in enumerate(self._cameras):
			_, frame = camera.read(show_time, show_fps)

			if not index:
				cameras_merge_frame = frame
			elif not index % 2:
				cameras_merge_frame = np.vstack((cameras_merge_frame, frame))
			else:
				cameras_merge_frame = np.hstack((cameras_merge_frame, frame))

		return cameras_merge_frame

	def get_camera_frame(self, camera_id: int, show_time=False, show_fps=False):
		"""
		Get camera frame data
		:param camera_id: camera id
		:param show_time: show time of the camera in camera frame data
		:param show_fps: show fps of the camera in camera frame data
		:return:
		"""
		camera = self.get_camera_by_id(camera_id)
		_, frame = camera.read(show_time, show_fps)
		return frame

	def show(self, camera_id, show_time=False, show_fps=False) -> None:
		"""
		Show one camera frame data

		!!Important!!
		show method should be run in main thread, and it will block main thread (Only in DEBUG mode)
		"""
		if self._show_status:
			print("Other showing windows is running. Please close it and retry.")
			return

		camera = self.get_camera_by_id(camera_id)
		if camera:
			while True:
				_, frame = camera.read(show_time, show_fps)
				cv2.imshow('Camera {}'.format(camera_id), frame)
				key = cv2.waitKey(1) & 0xff
				if key == 27:  # Esc
					break

	def show_all(self, show_time=False, show_fps=False) -> None:
		"""
		Show all cameras frame data. All the frame will merge into one frame

		!!Important!!
		show method should be run in main thread, and it will block main thread (Only in DEBUG mode)
		"""
		while True:
			cameras_merge_frame = self.get_merge_frame(show_time, show_fps)
			cv2.imshow('All Cameras', cameras_merge_frame)
			key = cv2.waitKey(1) & 0xff
			if key == 27:  # Esc
				break

	def set_detector(self, ) -> None:
		"""
		Set detector for each camera
		:return:
		"""
		for camera in self._cameras:
			detector = IntruderDetector(save_path='output')
			camera.enable_detector(detector)
			print("Camera Manager - Set detector: {}".format(detector))
