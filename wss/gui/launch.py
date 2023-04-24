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


from wss.core import settings
from wss.gui.ui import UIMainWindow
from wss.gui.apps import cameras
from wss.gui.apps import log_manager

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow


class WSSMainWindow(QMainWindow):
	add_left_menus = [
		{
			"btn_icon" : "icon_home.svg",
			"btn_id" : "btn_home",
			"btn_text" : "Home",
			"btn_tooltip" : "Home page",
			"show_top" : True,
			"is_active" : True
		},
		{
			"btn_icon": "icon_home.svg",
			"btn_id": "btn_home",
			"btn_text": "Log",
			"btn_tooltip": "Event log",
			"show_top": True,
			"is_active": False
		},
		{
			"btn_icon" : "icon_info.svg",
			"btn_id" : "btn_info",
			"btn_text" : "Information",
			"btn_tooltip" : "Open informations",
			"show_top" : False,
			"is_active" : False
		},
		{
			"btn_icon" : "icon_settings.svg",
			"btn_id" : "btn_settings",
			"btn_text" : "Settings",
			"btn_tooltip" : "Open settings",
			"show_top" : False,
			"is_active" : False
		}
	]

	add_title_bar_menus = [
		{
			"btn_icon" : "icon_search.svg",
			"btn_id" : "btn_search",
			"btn_tooltip" : "Search",
			"is_active" : False
		},
		{
			"btn_icon" : "icon_settings.svg",
			"btn_id" : "btn_top_settings",
			"btn_tooltip" : "Top settings",
			"is_active" : False
		}
	]

	def __init__(self):
		super().__init__()
		self.cameras_page = None
		self.accessories_page = None
		self.ui = None
		self.setObjectName("WSSMainWindow")

		self.init_window_property()
		self.init_ui()
		self.setup_apps()

	def init_ui(self):
		self.ui = UIMainWindow()
		self.ui.setup_ui(self)
		self.init_sidebar()
		self.init_title_bar()

	def init_window_property(self):
		self.resize(*settings.APP_WINDOW_START_UP_SIZE)
		self.setMinimumSize(*settings.APP_WINDOW_START_UP_SIZE)

	def init_sidebar(self):
		self.ui.get_sidebar().sidebar_clicked.connect(self.sidebar_button_clicked)

	def init_property(self):
		self.setWindowTitle(settings.APP_NAME)

		if settings.CUSTOM_TITLE_BAR:
			self.setWindowFlag(Qt.FramelessWindowHint)
			self.setAttribute(Qt.WA_TranslucentBackground)

	def setup_apps(self):
		cameras_page = cameras.views.CamerasView()
		self.ui.add_app('Cameras', cameras_page)
		log_manager_page = log_manager.views.LogManagerView()
		self.ui.add_app('Logs', log_manager_page)

	def init_title_bar(self):
		self.ui.title_bar.add_menus(self.add_title_bar_menus)
		self.ui.title_bar.set_title("Welcome to WSS")

	def sidebar_button_clicked(self, event):
		self.ui.switch_app_page(event)
