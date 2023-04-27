# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/23
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
import datetime

from wss.core import settings
from wss.core.model import wss_model
from wss.gui.widget.table import table_style
from wss.gui.widget.dialog import MediaPreviewDialog

from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, QRect
from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QTableWidget, QHeaderView, \
    QAbstractItemView, QTableWidgetItem


class LogManagerView(QWidget):
    def __init__(self):
        super(LogManagerView, self).__init__()
        self.column_headers = None
        self.preview_text = None
        self.preview_dialog = None
        self.log_table = None
        self.sub_title = None
        self.scroll_area = None
        self.log_content = None
        self.log_content_layout = None
        self.title_div = None
        self.title = None
        self.main_layout = None
        self.setup_ui()
        wss_model.register_callback('intruder_detect_logs', self.add_log)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 5, 5, 5)
        self.main_layout.setSpacing(15)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)
        self.setup_log_content()
        self.setup_title()
        self.setup_subtitle()
        self.setup_log_table()
        self.set_logs()

    def setup_title(self):
        self.title = QLabel()
        self.title.setText('Logs')
        self.title.setStyleSheet(f"font: 16pt '{settings.APP_FONT['family']}'")
        self.title.setMaximumHeight(30)
        self.title.setAlignment(Qt.AlignCenter)
        self.log_content_layout.addWidget(self.title)

    def setup_subtitle(self):
        self.sub_title = QLabel()
        self.sub_title.setObjectName(u"description_label")
        self.sub_title.setText('You can view all event logs here.')
        self.sub_title.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.sub_title.setWordWrap(True)
        self.log_content_layout.addWidget(self.sub_title)
    
    def setup_log_content(self):
        self.log_content = QFrame()
        self.log_content_layout = QVBoxLayout(self.log_content)
        self.log_content_layout.setContentsMargins(5, 5, 5, 5)
        self.log_content_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.log_content)

    def setup_log_table(self):
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.log_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.log_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.log_table.cellClicked.connect(self.show_resource_preview)

        style_format = table_style.style.format(
            _radius=8,
            _color="#8a95aa",
            _bg_color="#343b48",
            _header_horizontal_color="#1e2229",
            _header_vertical_color="#3c4454",
            _selection_color="#568af2",
            _bottom_line_color="#3c4454",
            _grid_line_color="#2c313c",
            _scroll_bar_bg_color="#2c313c",
            _scroll_bar_btn_color="#272c36",
            _context_color="#568af2"
        )
        self.log_table.setStyleSheet(style_format)
        self.log_content_layout.addWidget(self.log_table)

    def set_logs(self):
        self.column_headers = []
        headers = ['Thread status', 'Time', 'Image/Video Capture']

        for index, each_header in enumerate(headers):
            header_obj = QTableWidgetItem()
            header_obj.setTextAlignment(Qt.AlignCenter)
            header_obj.setText(each_header)
            self.column_headers.append(header_obj)
            self.log_table.setHorizontalHeaderItem(index, header_obj)

        self.add_log({'intruder_type': 2, 'path': 'D:\Code\wss-client-gui\wss\output\event4_03-30-34.avi', 'time': datetime.datetime(2023, 4, 27, 3, 33, 21, 17730)})

    def add_log(self, data):
        intruder_status = data['intruder_type']
        resource_path = data['path']
        log_time = data['time']

        row_number = self.log_table.rowCount()
        self.log_table.insertRow(row_number)

        normal_font = QFont("Arial", 12)

        intruder_status_item = QTableWidgetItem(str(intruder_status))
        intruder_status_item.setFont(normal_font)
        intruder_status_item.setTextAlignment(Qt.AlignCenter)
        self.log_table.setItem(row_number, 0, intruder_status_item)

        log_time_item = QTableWidgetItem(log_time.strftime("%A, %B %d, %Y"))
        log_time_item.setFont(normal_font)
        log_time_item.setTextAlignment(Qt.AlignCenter)
        self.log_table.setItem(row_number, 1, log_time_item)

        self.preview_text = QTableWidgetItem()
        font = QFont("Arial", 12)
        font.setUnderline(True)
        self.preview_text.setFont(font)
        self.preview_text.setTextAlignment(Qt.AlignCenter)
        self.preview_text.setText('preview')
        self.preview_text.resource_path = resource_path
        self.log_table.setItem(row_number, 2, self.preview_text)
        self.log_table.setRowHeight(row_number, 40)

    def show_resource_preview(self, row, column):
        if column == 2:
            resource_path = self.log_table.item(row, column).resource_path
            self.preview_dialog = MediaPreviewDialog(resource_path)
            self.preview_dialog.show()


        
