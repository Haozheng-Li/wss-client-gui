# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/19
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

from wss.core import settings
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QGraphicsDropShadowEffect


class LayoutWrapper(QFrame):
	def __init__(
			self,
			parent,
			layout=Qt.Vertical,
			margin=0,
			spacing=2,
			bg_color="#2c313c",
			text_color="#fff",
			text_font="9pt 'Segoe UI'",
			border_radius=10,
			border_size=2,
			border_color="#343b48",
			enable_shadow=True
	):
		super().__init__()

		self.parent = parent
		self.layout = layout
		self.margin = margin
		self.bg_color = bg_color
		self.text_color = text_color
		self.text_font = text_font
		self.border_radius = border_radius
		self.border_size = border_size
		self.border_color = border_color
		self.enable_shadow = enable_shadow

		# OBJECT NAME
		# ///////////////////////////////////////////////////////////////
		self.setObjectName("pod_bg_app")

		# APPLY STYLESHEET
		# ///////////////////////////////////////////////////////////////
		self.set_stylesheet()

		# ADD LAYOUT
		# ///////////////////////////////////////////////////////////////
		if layout == Qt.Vertical:
			# VERTICAL LAYOUT
			self.layout = QHBoxLayout(self)
		else:
			# HORIZONTAL LAYOUT
			self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(margin, margin, margin, margin)
		self.layout.setSpacing(spacing)

		# ADD DROP SHADOW
		# ///////////////////////////////////////////////////////////////
		if settings.CUSTOM_TITLE_BAR:
			if enable_shadow:
				self.shadow = QGraphicsDropShadowEffect()
				self.shadow.setBlurRadius(20)
				self.shadow.setXOffset(0)
				self.shadow.setYOffset(0)
				self.shadow.setColor(QColor(0, 0, 0, 160))
				self.setGraphicsEffect(self.shadow)

	# APPLY AND UPDATE STYLESHEET
	# ///////////////////////////////////////////////////////////////
	def set_stylesheet(
			self,
			bg_color=None,
			border_radius=None,
			border_size=None,
			border_color=None,
			text_color=None,
			text_font=None
	):
		# CHECK BG COLOR
		if bg_color is not None:
			internal_bg_color = bg_color
		else:
			internal_bg_color = self.bg_color

		# CHECK BORDER RADIUS
		if border_radius is not None:
			internal_border_radius = border_radius
		else:
			internal_border_radius = self.border_radius

		# CHECK BORDER SIZE
		if border_size is not None:
			internal_border_size = border_size
		else:
			internal_border_size = self.border_size

		# CHECK BORDER COLOR
		if text_color is not None:
			internal_text_color = text_color
		else:
			internal_text_color = self.text_color

		# CHECK TEXT COLOR
		if border_color is not None:
			internal_border_color = border_color
		else:
			internal_border_color = self.border_color

		# CHECK TEXT COLOR
		if text_font is not None:
			internal_text_font = text_font
		else:
			internal_text_font = self.text_font

		bg_style = """
		#pod_bg_app {{
		    background-color: {_bg_color};
		    border-radius: {_border_radius};
		    border: {_border_size}px solid {_border_color};
		}}
		QFrame {{ 
		    color: {_text_color};
		    font: {_text_font};
		}}
		"""

		self.setStyleSheet(bg_style.format(
			_bg_color=internal_bg_color,
			_border_radius=internal_border_radius,
			_border_size=internal_border_size,
			_border_color=internal_border_color,
			_text_color=internal_text_color,
			_text_font=internal_text_font
		))
