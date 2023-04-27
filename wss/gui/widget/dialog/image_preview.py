# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/27
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
import os
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QVBoxLayout, QLabel, QDialog, QApplication
from PySide2.QtGui import QPixmap


class MediaPreviewDialog(QDialog):
	def __init__(self, media_path):
		super(MediaPreviewDialog, self).__init__()

		self.video_widget = None
		self.media_player = None
		self.content_layout = None
		self.image_label = None

		self.media_path = media_path
		self.setup_ui()
		self.center()

	def setup_ui(self):
		self.setWindowTitle('Media Preview')
		self.setGeometry(100, 100, 400, 300)

		self.content_layout = QVBoxLayout(self)

		_, ext = os.path.splitext(self.media_path)
		if ext.lower() in ['.png', '.jpg', '.jpeg']:
			self.image_label = QLabel(self)
			self.image_label.setPixmap(QPixmap(self.media_path))
			self.image_label.setScaledContents(True)
			self.content_layout.addWidget(self.image_label)
		elif ext.lower() in ['.avi', '.mp4']:
			self.media_player = QMediaPlayer(self)
			self.video_widget = QVideoWidget(self)
			self.content_layout.addWidget(self.video_widget)
			video_url = QUrl.fromLocalFile(self.media_path.replace('\\', '/'))
			self.media_player.setVideoOutput(self.video_widget)
			self.media_player.setMedia(QMediaContent(video_url))
			self.media_player.play()

	def focusOutEvent(self, event):
		if hasattr(self, 'media_player'):
			self.media_player.stop()
		self.close()

	def center(self):
		screen_geometry = QApplication.desktop().screenGeometry()
		window_geometry = self.geometry()
		x = (screen_geometry.width() - window_geometry.width()) / 2 + screen_geometry.left()
		y = (screen_geometry.height() - window_geometry.height()) / 2 + screen_geometry.top()
		self.move(x, y)

