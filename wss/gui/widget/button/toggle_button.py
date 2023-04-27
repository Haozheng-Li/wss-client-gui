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

from PySide2.QtCore import QEasingCurve, Qt, QPropertyAnimation, QPoint, QRect, Property, Signal
from PySide2.QtGui import QPainter, QFont, QColor
from PySide2.QtWidgets import QCheckBox


class ToggleButton(QCheckBox):

	switch_signal = Signal(bool)

	def __init__(
			self,
			width=50,
			bg_color="#777",
			circle_color="#DDD",
			active_color="#00BCFF",
			animation_curve=QEasingCurve.OutBounce
	):
		QCheckBox.__init__(self)
		self.setFixedSize(width, 28)
		self.setCursor(Qt.PointingHandCursor)

		self._bg_color = bg_color
		self._circle_color = circle_color
		self._active_color = active_color

		self._position = self.width() - 26
		self.animation = QPropertyAnimation(self, b"position")
		self.animation.setEasingCurve(animation_curve)
		self.animation.setDuration(500)
		self.setChecked(True)
		self.update()
		self.stateChanged.connect(self.setup_animation)

	@Property(float)
	def position(self):
		return self._position

	@position.setter
	def position(self, pos):
		self._position = pos
		self.update()

	def setup_animation(self, value):
		self.switch_signal.emit(value)
		self.animation.stop()
		if value:
			self.animation.setEndValue(self.width() - 26)
		else:
			self.animation.setEndValue(4)
		self.animation.start()

	def hitButton(self, pos: QPoint):
		return self.contentsRect().contains(pos)

	def paintEvent(self, e):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)
		p.setFont(QFont("Segoe UI", 9))

		# SET PEN
		p.setPen(Qt.NoPen)

		# DRAW RECT
		rect = QRect(0, 0, self.width(), self.height())

		if not self.isChecked():
			p.setBrush(QColor(self._bg_color))
			p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self._position, 3, 22, 22)
		else:
			p.setBrush(QColor(self._active_color))
			p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self._position, 3, 22, 22)

		p.end()