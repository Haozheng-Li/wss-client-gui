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

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget, QCheckBox, QListWidgetItem, QHBoxLayout, QFrame


class CamerasView(QWidget):
	def __init__(self):
		super(CamerasView, self).__init__()
		self.camera_frame = None
		self.content_layout = None
		self.content = None
		self.layout = None
		self.title_div = None
		self.title = None

	def setup_title(self):
		self.title = QLabel()
		self.title.setText('Cameras')
		self.title.setMaximumHeight(20)
		self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
		self.layout.addWidget(self.title)

		self.title_div = HorizontalDiv(theme.DARK_FOUR)
		self.layout.addWidget(self.title_div)

	def setup_ui(self):
		self.setObjectName('cameras')

		self.layout = QVBoxLayout(self)
		self.layout.setSpacing(15)
		self.layout.setObjectName(u"layout")
		self.layout.setContentsMargins(12, 12, 12, 12)

		self.setup_title()

		self.content = QFrame()
		self.content_layout = QHBoxLayout(self.content)

		self.camera_frame = QLabel()
		self.content_layout.addWidget(self.camera_frame)

		self.layout.addWidget(self.content)

	def show_camera_frame(self):
		flag, self.image = self.cap.read()  # 从视频流中读取

		show = cv2.resize(self.image, (640, 480))
		show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
		showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
		self.camera_frame.setPixmap(QPixmap.fromImage(showImage))


class AccessoriesView(QWidget):
	def __init__(self):
		super().__init__()

		self.accessories_container = None
		self.title_div = None
		self.title = None
		self.layout = None
		self.parent = None
		
	def setup_title(self):
		self.title = QLabel()
		self.title.setText('Accessories')
		self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
		self.title.setMaximumHeight(20)
		self.layout.addWidget(self.title)

		self.title_div = HorizontalDiv(theme.DARK_FOUR)
		self.layout.addWidget(self.title_div)

	def setup_ui(self):
		self.setObjectName('accessories')
		
		self.layout = QVBoxLayout(self)
		self.layout.setSpacing(15)
		self.layout.setObjectName(u"layout")
		self.layout.setContentsMargins(12, 12, 12, 12)
		
		self.setup_title()

		self.accessories_container = QListWidget(self)
		self.accessories_container.setStyleSheet(f"background-color: {theme.BG_TWO}; border-radius: 8px;")
		self.accessories_container.setObjectName(u"accessories_container")

		self.layout.addWidget(self.accessories_container)

		item = AccessoryBox()
		item2 = AccessoryBox()
		self.add_accessory(item)
		self.add_accessory(item2)

	def add_accessory(self, widget):
		item = QListWidgetItem()
		item.setSizeHint(QSize(100, 100))
		self.accessories_container.addItem(item)
		self.accessories_container.setItemWidget(item, widget)


class AccessoryBox(QWidget):
	def __init__(self):
		super(AccessoryBox, self).__init__()
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
		self.camera_figure.setPixmap(QPixmap(settings.BASE_DIR / 'static/image/usb-camera.png'))  # 图片路径

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


