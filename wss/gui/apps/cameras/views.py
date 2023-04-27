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
from PySide2.QtCore import QSize, QTimer, Signal, Qt
from PySide2.QtGui import QPixmap, QImage

from wss.core import settings
from wss.core.model import wss_model
from wss.gui.style import theme
from wss.gui.widget.button import ToggleButton
from wss.gui.widget.div import HorizontalDiv

from wss.accessories.cameras import get_camera_manager

from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidget, QListWidgetItem, QCheckBox


class CamerasView(QWidget):
    def __init__(self):
        super(CamerasView, self).__init__()
        self.camera_settings_menu = None
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

        self.setup_ui()

    def setup_ui(self):
        self.setObjectName('cameras')

        self.content_layout = QHBoxLayout(self)
        self.content_layout.setSpacing(15)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 5, 5, 5)
        self.setup_left_page()
        self.setup_right_page()

        self.setup_camera_settings_menu()

        self.setup_right_page_content()
        self.setup_left_page_content()

    def setup_left_page(self):
        self.left_page_frame = QFrame()
        self.left_page_frame.setObjectName("left_page_frame")
        self.left_page_frame_layout = QVBoxLayout(self.left_page_frame)
        self.left_page_frame_layout.setSpacing(15)
        self.left_page_frame_layout.setObjectName(u"left_page_frame_layout")
        self.left_page_frame_layout.setContentsMargins(0, 12, 5, 12)

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
        self.right_page_layout.setContentsMargins(5, 12, 5, 12)
        self.right_page_layout.setSpacing(12)

        self.content_layout.addWidget(self.right_page_frame)

    def setup_right_page_content(self):
        self.right_page_content = CameraPreviewOptionsView()
        self.right_page_content.setup_ui()
        self.right_page_content.option_change_signal.connect(self.on_preview_option_change)
        self.right_page_layout.addWidget(self.right_page_content)

    def setup_left_page_content(self):
        self.left_page_content = CameraFigureView()
        self.left_page_content.setup_ui()
        self.left_page_frame_layout.addWidget(self.left_page_content)

    def setup_camera_settings_menu(self):
        self.camera_settings_menu = CameraSettingsMenu()
        self.left_page_frame_layout.addWidget(self.camera_settings_menu)

    def on_preview_option_change(self, option_id):
        self.left_page_content.on_preview_option_change(option_id)


class CameraSettingsMenu(QWidget):
    def __init__(self):
        super(CameraSettingsMenu, self).__init__()
        self.detect_switch_label = None
        self.detect_switch = None
        self.detect_switch_frame_layout = None
        self.detect_switch_frame = None
        self.thread_status_label = None
        self.content_layout = None
        self.bg = None
        self.layout = None
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName('camera_preview_options')
        self.setMaximumHeight(40)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.bg = QFrame()
        self.bg.setStyleSheet(f"background: {theme.BG_TWO}; border-radius: 10;")
        self.content_layout = QHBoxLayout(self.bg)
        self.content_layout.setContentsMargins(10, 0, 10, 0)
        self.content_layout.setSpacing(0)
        self.layout.addWidget(self.bg)

        self.thread_status_label = QLabel()
        self.thread_status_label.setText("Thread status: 1")
        self.thread_status_label.setStyleSheet(f"font:11pt; color: {theme.CONTEXT_COLOR}")
        self.content_layout.addWidget(self.thread_status_label, 0, Qt.AlignLeft)

        self.detect_switch_frame = QFrame()
        self.detect_switch_frame.setStyleSheet("backgroud:#fff")
        self.detect_switch_frame_layout = QHBoxLayout(self.detect_switch_frame)
        self.detect_switch_frame_layout.setContentsMargins(10, 0, 5, 0)
        self.detect_switch_frame_layout.setSpacing(10)

        self.detect_switch = ToggleButton(            
            width=50,
            bg_color=theme.DARK_TWO,
            circle_color=theme.ICON_COLOR,
            active_color=theme.CONTEXT_COLOR)

        self.detect_switch.switch_signal.connect(self.on_detect_switch_change)

        self.detect_switch_label = QLabel()
        self.detect_switch_label.setText("Detect status")
        self.detect_switch_label.setStyleSheet(f"font:11pt; color: {theme.CONTEXT_COLOR}")
        self.detect_switch_frame_layout.addWidget(self.detect_switch_label)
        self.detect_switch_frame_layout.addWidget(self.detect_switch)

        self.content_layout.addWidget(self.detect_switch_frame, 0, Qt.AlignRight)

    def on_detect_switch_change(self, status):
        wss_model.set_detector_status(status)


class CameraPreviewOptionsView(QWidget):
    
    option_change_signal = Signal(int)
    OPTION_MERGE = 99
    
    def __init__(self):
        super().__init__()
        self.options_container = None
        self.title_div = None
        self.title = None
        self.layout = None
        self.parent = None
        self.boxes = []

    def setup_title(self):
        self.title = QLabel()
        self.title.setText('Preview options')
        self.title.setStyleSheet(f"font: 12pt '{settings.APP_FONT['family']}'")
        self.title.setMaximumHeight(20)
        self.layout.addWidget(self.title)

        self.title_div = HorizontalDiv(theme.DARK_FOUR)
        self.layout.addWidget(self.title_div)

    def setup_ui(self):
        self.setObjectName('camera_preview_options')

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.setup_title()

        self.options_container = QListWidget(self)
        self.options_container.setStyleSheet(f"background-color: {theme.BG_TWO}; border-radius: 8px;")
        self.options_container.setObjectName(u"options_container")

        self.layout.addWidget(self.options_container)

        avaliable_cameras_id = get_camera_manager().get_available_cameras_id()

        option_merge_box = CameraPreviewOptionsBox(text='Merge View',
                                             icon=str(settings.BASE_DIR / 'static/image/icon/camera.png'),
                                             option_id=self.OPTION_MERGE)
        option_merge_box.set_active()
        self.add_options(option_merge_box)

        for index in avaliable_cameras_id:
            option_box = CameraPreviewOptionsBox(text='USB Camera{}'.format(index),
                                            icon=str(settings.BASE_DIR / 'static/image/usb-camera.png'),
                                                 option_id=index)
            self.add_options(option_box)

        self.options_container.setCurrentRow(0)
        self.options_container.currentItemChanged.connect(self.on_item_changed)

    def on_item_changed(self, current, previous):
        selected_widget = self.options_container.itemWidget(current)
        pre_selected_widget = self.options_container.itemWidget(previous)
        selected_widget.set_active()
        pre_selected_widget.set_inactive()
        self.option_change_signal.emit(selected_widget.get_option_id())

    def add_options(self, widget):
        item = QListWidgetItem()
        item.setSizeHint(QSize(120, 100))
        self.boxes.append(item)
        self.options_container.addItem(item)
        self.options_container.setItemWidget(item, widget)


class CameraPreviewOptionsBox(QWidget):
    def __init__(self, text, icon, option_id):
        super(CameraPreviewOptionsBox, self).__init__()
        self.option_id = option_id
        self.label = None
        self.verticalLayout = None
        self.frame = None
        self.container = None
        self.wrapper_layout = None
        self.camera_figure = None
        self.container_layout = None

        self.text = text
        self.icon = icon
        self.setup_ui()

    def get_option_id(self):
        return self.option_id

    def set_active(self):
        self.container.setStyleSheet(f"""
        #container {{
        border-radius: 8px;
        border: 3px solid #568AF2;
        }}
        """)

    def set_inactive(self):
        self.container.setStyleSheet(f"""
        #container {{
        border-radius: 8px;
        border: 3px solid #C3CCDF;
        }}
        """)

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
        border: 3px solid #C3CCDF;
        }}
        """)
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setObjectName(u"horizontalLayout")
        self.container_layout.setContentsMargins(5, 0, 0, 0)
        self.container_layout.setSpacing(0)

        self.camera_figure = QLabel(self)
        camera_figure_size = 48
        self.camera_figure.setMaximumSize(camera_figure_size, camera_figure_size)
        self.camera_figure.setMinimumSize(camera_figure_size, camera_figure_size)
        self.camera_figure.setObjectName(u"pic")
        self.camera_figure.setScaledContents(True)
        self.camera_figure.setPixmap(QPixmap(self.icon))

        self.container_layout.addWidget(self.camera_figure)

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setText(self.text)

        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.container_layout.addWidget(self.frame)
        self.wrapper_layout.addWidget(self.container)


class CameraFigureView(QWidget):
    def __init__(self):
        super(CameraFigureView, self).__init__()
        self.preview_option_id = CameraPreviewOptionsView.OPTION_MERGE
        self.capture = None
        self.timer = None
        self.title = None
        self.title_div = None

        self.camera_figure_content_layout = None
        self.camera_frame_preview = None
        self.camera_figure_content = None

        self.content_layout = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_camera_frame)
        self.timer.start(50)
        self.camera_manager = None

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
        self.content_layout.setSpacing(10)
        self.content_layout.setObjectName(u"camera_figure_layout")
        self.content_layout.setContentsMargins(5, 5, 5, 5)

        self.setup_title()

        self.camera_figure_content = QFrame()
        self.camera_figure_content_layout = QHBoxLayout(self.camera_figure_content)
        self.content_layout.addWidget(self.camera_figure_content)

        self.setup_camera_preview_page()

    def setup_camera_preview_page(self):
        self.camera_frame_preview = QLabel()
        self.camera_frame_preview.setObjectName(u"camera_frame_preview")
        self.camera_frame_preview.setScaledContents(True)
        self.camera_figure_content_layout.addWidget(self.camera_frame_preview)

    def on_preview_option_change(self, option_id):
        self.preview_option_id = option_id

    def _update_camera_frame(self):
        if not self.camera_manager:
            self.camera_manager = get_camera_manager()
        if not self.camera_manager.get_available_cameras_id() or not self.camera_manager.get_camera_start_status():
            return

        if self.preview_option_id == 99:
            frame = cv2.cvtColor(self.camera_manager.get_merge_frame(), cv2.COLOR_BGR2RGB)
        else:
            frame = cv2.cvtColor(self.camera_manager.get_camera_frame(self.preview_option_id), cv2.COLOR_BGR2RGB)

        frame_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.camera_frame_preview.setPixmap(QPixmap.fromImage(frame_image))

