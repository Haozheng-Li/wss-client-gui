#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/10 17:44
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import cv2
import numpy as np

from wss.accessories.cameras.base import CameraBase
from wss.accessories.cameras.expections import CameraDostNotExist, CameraRunningModeError


__all__ = ['get_camera_manager']

from wss.core import settings

from wss.detector import IntruderDetector

CAMERA_MANAGER = None


def get_camera_manager():
	global CAMERA_MANAGER
	if not CAMERA_MANAGER:
		CAMERA_MANAGER = CameraManager()
	return CAMERA_MANAGER


class CameraManager:
	"""
	Important! In macOS or Linux, CameraManager should be run in main thread.
	"""

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
		self.available_cameras_id = [0, 2]
		return self.available_cameras_id
		
	def _camera_init(self, camera_id) -> object:
		camera = CameraBase(camera_id)
		self._cameras.append(camera)
		print("Camera manager - Init cameras: id {}".format(camera_id))
		return camera

	def initialize_cameras(self, cameras_id) -> None:
		for camera_id in cameras_id:
			self._camera_init(camera_id)

	def get_camera_start_status(self):
		return self.camera_started

	@staticmethod
	def _stop_camera(camera_obj) -> None:
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
		for camera in self._cameras:
			camera.set_properties(width, height, codec, fps)

	def start_camera_by_id(self, camera_id):
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._start_camera(camera)

	def stop_camera_by_id(self, camera_id):
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._stop_camera(camera)

	def start_all(self) -> None:
		for camera in self._cameras:
			self._start_camera(camera)

	def stop_all(self) -> None:
		for camera in self._cameras:
			self._stop_camera(camera)

	def get_camera_by_id(self, camera_id) -> object:
		for camera in self._cameras:
			if camera.camera_id == camera_id:
				return camera
		raise CameraDostNotExist('Camera id {} does not exist'.format(camera_id))

	def get_all_cameras(self) -> list:
		return self._cameras

	def get_mode(self) -> int:
		return self._running_mode

	def switch_mode(self, mode) -> None:
		self._running_mode = mode
		print("Camera Manager - Change running mode: from mode{} to mode {}".format(self._running_mode, mode))

	def switch_camera(self, camera_id) -> None:
		if self._running_mode != self.MODE_PULLING:
			raise CameraRunningModeError("Switch cameras should be running in pulling mode!")
		camera = self.get_camera_by_id(camera_id)
		camera.start()
		self.activated_cameras.append(camera)

	def get_frame(self, camera_id, show_time=False, show_fps=False):
		camera = self.get_camera_by_id(camera_id)
		if camera.get_open_status():
			return camera.read(show_time, show_fps)

	def camera_properties(self, camera_id):
		pass

	def get_merge_frame(self, show_time=False, show_fps=False):
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

	def get_camera_frame(self, camera_id, show_time=False, show_fps=False):
		camera = self.get_camera_by_id(camera_id)
		_, frame = camera.read(show_time, show_fps)
		return frame

	def show(self, camera_id, show_time=False, show_fps=False) -> None:
		"""
		!!Important!! show function will block the main thread
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
		!!Important!! show all function will block the main thread
		"""
		while True:
			cameras_merge_frame = self.get_merge_frame(show_time, show_fps)
			cv2.imshow('All Cameras', cameras_merge_frame)
			key = cv2.waitKey(1) & 0xff
			if key == 27:  # Esc
				break

	def set_detector(self, ) -> None:
		for camera in self._cameras:
			detector = IntruderDetector(save_path=str(settings.BASE_DIR / 'output'))
			camera.enable_detector(detector)
			print("Camera Manager - Set detector: {}".format(detector))
