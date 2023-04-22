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
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QImage

from wss.core import settings
from wss.gui.style import theme
from wss.gui.widget.div import HorizontalDiv

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidget, QListWidgetItem, QCheckBox


class CamerasView(QWidget):
    def __init__(self):
        super(CamerasView, self).__init__()
        self.right_page_content = None
        self.left_page_content = None
        self.right_page_layout = None
        self.right_page_frame = None
        self.left_page_frame_layout = None
        self.left_page_frame = None
        self.camera_frame = None
        self.content_layout = None
        self.content = None
        self.content_layout = None
        self.left_page_title_div = None
        self.left_page_title = None

    def setup_ui(self):
        self.setObjectName('cameras')

        self.content_layout = QHBoxLayout(self)
        self.content_layout.setSpacing(15)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 5, 5, 5)
        self.setup_left_page()
        self.setup_right_page()

        self.setup_left_page_content()
        self.setup_right_page_content()

    def setup_left_page(self):
        self.left_page_frame = QFrame()
        self.left_page_frame.setObjectName("left_page_frame")
        self.left_page_frame.setStyleSheet(f'''
            #left_page_frame {{
                border-radius: 8px;
                background-color: {theme.BG_TWO};
            }}
        ''')
        self.left_page_frame_layout = QVBoxLayout(self.left_page_frame)
        self.left_page_frame_layout.setSpacing(15)
        self.left_page_frame_layout.setObjectName(u"left_page_frame_layout")
        self.left_page_frame_layout.setContentsMargins(12, 12, 12, 12)

        self.content_layout.addWidget(self.left_page_frame)

    def setup_right_page(self):
        self.right_page_frame = QFrame()
        self.right_page_frame.setObjectName("right_page_frame")
        self.right_page_frame.setMinimumWidth(settings.APP_RIGHT_COLUMN_SIZE['maximum'])
        self.right_page_frame.setMaximumWidth(settings.APP_RIGHT_COLUMN_SIZE['maximum'])

        self.right_page_frame.setStyleSheet(f'''
            #right_page_frame {{
                border-radius: 8px;
                background-color: {theme.BG_TWO};
            }}
        ''')

        self.right_page_layout = QVBoxLayout(self.right_page_frame)
        self.right_page_layout.setContentsMargins(5, 5, 5, 5)
        self.right_page_layout.setSpacing(0)

        self.content_layout.addWidget(self.right_page_frame)

    def setup_right_page_content(self):
        self.right_page_content = AvailableCamerasView()
        self.right_page_content.setup_ui()
        self.right_page_layout.addWidget(self.right_page_content)

    def setup_left_page_content(self):
        self.left_page_content = CameraFigureView()
        self.left_page_content.setup_ui()
        self.left_page_frame_layout.addWidget(self.left_page_content)


class AvailableCamerasView(QWidget):
    def __init__(self):
        super().__init__()
        self.available_cameras_container = None
        self.title_div = None
        self.title = None
        self.layout = None
        self.parent = None

    def setup_title(self):
        self.title = QLabel()
        self.title.setText('Available Cameras')
        self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
        self.title.setMaximumHeight(20)
        self.layout.addWidget(self.title)

        self.title_div = HorizontalDiv(theme.DARK_FOUR)
        self.layout.addWidget(self.title_div)

    def setup_ui(self):
        self.setObjectName('available_cameras')

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(12, 12, 12, 12)

        self.setup_title()

        self.available_cameras_container = QListWidget(self)
        self.available_cameras_container.setStyleSheet(f"background-color: {theme.BG_TWO}; border-radius: 8px;")
        self.available_cameras_container.setObjectName(u"available_cameras_container")

        self.layout.addWidget(self.available_cameras_container)

        item = AvailableCameraBox()
        item2 = AvailableCameraBox()
        self.add_accessory(item)
        self.add_accessory(item2)

    def add_accessory(self, widget):
        item = QListWidgetItem()
        item.setSizeHint(QSize(100, 100))
        self.available_cameras_container.addItem(item)
        self.available_cameras_container.setItemWidget(item, widget)


class AvailableCameraBox(QWidget):
    def __init__(self):
        super(AvailableCameraBox, self).__init__()
        self.camera_figure = None
        self.container_layout = None
        self.setStyleSheet("background:#fff;")
        self.setup_ui()

    def set_data(self, data):
        pass

    def setup_ui(self):
        self.setStyleSheet(f"""
		    QFrame {{ 
				background-color: {theme.BG_TWO};
        }}""")
        self.wrapper_layout = QHBoxLayout(self)
        self.container = QFrame()
        self.container.setObjectName(u'container')
        self.container.setStyleSheet(f"""

	        #container {{
		        border-radius: 8px;
		        border: 3px solid #568af2;
	        }}
	    """)
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setObjectName(u"horizontalLayout")
        self.container_layout.setContentsMargins(10, 0, 0, 0)
        self.container_layout.setSpacing(0)

        self.camera_figure = QLabel(self)
        self.camera_figure.setMaximumSize(64, 64)
        self.camera_figure.setMinimumSize(64, 64)
        self.camera_figure.setObjectName(u"pic")
        self.camera_figure.setScaledContents(True)
        self.camera_figure.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/usb-cameras.png'))

        self.container_layout.addWidget(self.camera_figure)

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setText("USB Camera 1")

        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)
        self.container_layout.addWidget(self.frame)
        self.wrapper_layout.addWidget(self.container)


class CameraFigureView(QWidget):
    def __init__(self):
        super(CameraFigureView, self).__init__()
        self.camera_figure_content_layout = None
        self.camera_frame_preview = None
        self.camera_figure_content = None
        self.title_div = None
        self.title = None
        self.content_layout = None

    def setup_title(self):
        self.title = QLabel()
        self.title.setText('Camera Figure')
        self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
        self.title.setMaximumHeight(20)
        self.content_layout.addWidget(self.title)

        self.title_div = HorizontalDiv(theme.DARK_FOUR)
        self.content_layout.addWidget(self.title_div)

    def setup_ui(self):
        self.setObjectName('camera_figure')
        
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setSpacing(15)
        self.content_layout.setObjectName(u"camera_figure_layout")
        self.content_layout.setContentsMargins(12, 12, 12, 12)

        self.setup_title()
        
        self.camera_figure_content = QFrame()
        self.camera_figure_content_layout = QHBoxLayout(self.camera_figure_content)
        self.content_layout.addWidget(self.camera_figure_content)

        self.setup_camera_preview_page()

    def setup_camera_preview_page(self):
        self.camera_frame_preview = QLabel()
        self.camera_frame_preview.setObjectName(u"pic")
        self.camera_frame_preview.setScaledContents(True)
        self.camera_frame_preview.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/usb-cameras.png'))

        self.camera_figure_content_layout.addWidget(self.camera_frame_preview)
