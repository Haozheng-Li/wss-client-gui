import os
import cv2
import datetime

from wss.core import settings
from wss.detector.base import BaseCameraDetector
from wss.core.model import wss_model

__all__ = ['IntruderDetector']


class IntruderDetector(BaseCameraDetector):
	"""
	result format: {'intruder_type': int, 'path': str}
	"""
	INTRUDER_EVENT1 = 1
	INTRUDER_EVENT2 = 2
	INTRUDER_EVENT3 = 3
	INTRUDER_EVENT4 = 4

	def __init__(self, save_path='') -> None:
		super().__init__()
		self.ori_frame = None
		self.benchmark_frame = None

		self.bg_sub = cv2.createBackgroundSubtractorMOG2(history=400, varThreshold=40, detectShadows=True)
		self.result = {'intruder_type': self.INTRUDER_EVENT1, 'path': ''}
		self.status = self.INTRUDER_EVENT1

		self.save_path = save_path

		self.prev_roi_area = 0
		self.frame_counter = 0
		self.detect_counter = 0
		self.not_detect_counter = 0

		self.detector_status = True

		self.video_output_writer = None
		self.video_output_path = ''

		self.check_path_validity()

		self.face_cascade = cv2.CascadeClassifier(str(settings.BASE_DIR / 'cv_models/haarcascade_frontalface_default.xml'))

		wss_model.register_callback('detector_status', self.set_detector_status)

	def set_detector_status(self, status):
		self.detector_status = status

	def check_path_validity(self):
		"""
		Check output path validity
		:return:
		"""
		if not os.path.exists(self.save_path):
			print("Detector save path do not exist, create directory now.")
			os.mkdir(self.save_path)

	def detect(self, frame):
		"""
		:param frame:
		:return:
		"""
		if not self.detector_status:
			return frame

		self.frame_counter += 1
		frame_copy = frame.copy()
		frame_copy = cv2.GaussianBlur(frame_copy, (11, 11), 0)
		foreground_mask = self.bg_sub.apply(frame_copy)

		_, thresh = cv2.threshold(foreground_mask, 127, 255, cv2.THRESH_BINARY)

		cleaned = cv2.GaussianBlur(thresh, (9, 9), 0)
		contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		if not contours:
			return frame

		human_result, human_frame = self.human_detect(frame)

		max_contour = max(contours, key=cv2.contourArea)

		if cv2.contourArea(max_contour) < 1200 or (cv2.contourArea(max_contour) / self.get_frame_area(frame)) > 0.6:
			self.not_detect_counter += 1
			if self.not_detect_counter > self.fps * 3:
				self.set_event(self.INTRUDER_EVENT1, frame, human_result)
			return frame

		x, y, w, h = cv2.boundingRect(max_contour)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
		mid_point = (int(x + w / 2.0), int(y + h / 2.0))
		cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

		if self.status == self.INTRUDER_EVENT1:
			self.set_event(self.INTRUDER_EVENT2, frame, human_result)

		roi_area = w * h
		if self.prev_roi_area and not self.frame_counter % self.fps:  # Detect per second
			if int((roi_area - self.prev_roi_area) / self.prev_roi_area * 100) > 10:
				self.detect_counter += 1

		if self.detect_counter > 2 and self.status == self.INTRUDER_EVENT2:  # At lease last for 2 seconds
			self.set_event(self.INTRUDER_EVENT3, frame, human_result)

		if self.detect_counter > 4:  # At lease last for 5 seconds
			self.set_event(self.INTRUDER_EVENT4, frame, human_result)

		if not self.frame_counter % (self.fps + 1):
			self.prev_roi_area = roi_area

		# cv2.putText(frame, 'Event {}'.format(self.status), (10, 100), cv2.FONT_HERSHEY_PLAIN, 3,
		#             (0, 0, 255), thickness=2)

		self.frame = frame
		return frame

	def set_event(self, event_type, frame, human_result):
		"""
		Set motion detect event
		:param event_type: event id
		:param frame: camera frame data
		:param human_result: human result data
		:return:
		"""
		if event_type == self.INTRUDER_EVENT1:
			if self.status == self.INTRUDER_EVENT4:
				self.result = {'intruder_type': self.INTRUDER_EVENT4, 'path': self.video_output_path, 'time': datetime.datetime.now()}
				self.on_result_change()
				self.video_output_writer.release()
				self.video_output_writer = None
				self.detect_counter = 0
				self.not_detect_counter = 0
				self.video_output_path = ''
			self.status = event_type
			wss_model.set_intruder_status(self.status)

		if event_type == self.INTRUDER_EVENT2 and human_result:
			self.status = event_type
			wss_model.set_intruder_status(self.status)
			output_path = '{}/event2_{}.jpg'.format(self.save_path, datetime.datetime.now().strftime("%I-%M-%S"))
			cv2.imwrite(output_path, frame)
			self.result = {'intruder_type': event_type, 'path': output_path, 'time': datetime.datetime.now()}
			print("Trigger event2")
			self.on_result_change()

		elif event_type == self.INTRUDER_EVENT3 and human_result:
			self.status = event_type
			wss_model.set_intruder_status(self.status)
			output_path = '{}/event3_{}.jpg'.format(self.save_path, datetime.datetime.now().strftime("%I-%M-%S"))
			cv2.imwrite(output_path, frame)
			self.result = {'intruder_type': event_type, 'path': output_path, 'time': datetime.datetime.now()}
			self.on_result_change()

		elif event_type == self.INTRUDER_EVENT4 and human_result:
			self.status = event_type
			wss_model.set_intruder_status(self.status)
			if not self.video_output_path:
				self.video_output_path = '{}/event4_{}.avi'.format(self.save_path, datetime.datetime.now().strftime("%I-%M-%S"))
			if not self.video_output_writer:
				self.video_output_writer = cv2.VideoWriter(self.video_output_path, cv2.VideoWriter_fourcc(*'XVID'),
				                                           self.fps, (self.width, self.height))
			self.video_output_writer.write(frame)

	def human_detect(self, frame):
		"""
		detect human
		:param frame:
		:return:
		"""
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Detect faces in the image
		faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=2, minSize=(20, 20))

		# Draw rectangles around detected faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
		
		if len(faces):
			results = True
		else:
			results = False

		return results, frame

	def on_result_change(self):
		wss_model.set_intruder_detect_log(self.result)
		if self._callback:
			for each_func in self._callback:
				each_func(self.result)
