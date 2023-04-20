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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QWidget, QHBoxLayout, QFrame, QLabel


class Footer(QWidget):
    def __init__(
        self,
        copyright,
        version,
        bg_two,
        font_family,
        text_size,
        text_description_color,
        radius=8,
        padding=10
    ):
        super().__init__()

        self.separator = None
        self.version_label = None
        self.copyright_label = None
        self.bg_layout = None
        self.bg_frame = None
        self.widget_layout = None
        self._copyright = copyright
        self._version = version
        self._bg_two = bg_two
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding

        self.setup_ui()

    def setup_ui(self):
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        style = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg_two};
        }}
        .QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style)

        self.widget_layout.addWidget(self.bg_frame)

        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)

        self.copyright_label = QLabel(self._copyright)
        self.copyright_label.setAlignment(Qt.AlignVCenter)

        self.version_label = QLabel(self._version)
        self.version_label.setAlignment(Qt.AlignVCenter)

        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
