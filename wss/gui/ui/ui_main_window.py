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
from wss.gui.style import theme
from wss.gui.ui.ui_right_column import Ui_RightColumn
from wss.gui.widget.sidebar import PyLeftMenu
from wss.gui.widget.title_bar import PyTitleBar

from wss.gui.widget.footer import Footer
from wss.gui.widget.container import LayoutWrapper
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame


class UIMainWindow(object):
	def __init__(self):
		self.right_page_content = None
		self.right_page_layout = None
		self.title_bar = None
		self.title_bar_layout = None
		self.title_bar_frame = None
		self.right_page_frame = None
		self.sidebar = None
		self.central_widget = None
		
		self.sidebar_layout = None
		self.layout_wrapper = None
		
		self.footer_layout = None
		self.footer_frame = None
		self.footer = None
		self.right_page_bg_frame = None
		self.left_page_frame = None
		self.main_content_layout = None
		self.main_content_frame = None
		self.container_layout = None
		self.container = None
		self.sidebar_frame = None
		self.layout_wrapper = None
		self.central_widget_layout = None
		
		self.parent = None

	def setup_ui(self, parent):
		self.parent = parent

		self.setup_central_widget()
		self.setup_layout_wrapper()
		self.setup_sidebar()
		self.setup_container()
		self.setup_titlebar()
		self.setup_main_content()
		self.setup_left_page()
		self.setup_right_page()
		self.setup_footer()

		self.parent.setCentralWidget(self.central_widget)

	def setup_central_widget(self):
		self.central_widget = QWidget()
		self.central_widget.setStyleSheet(
			f'''
			    font: {settings.APP_FONT["text_size"]}pt "{settings.APP_FONT["family"]}";
			    color: {theme.TEXT_FOREGROUND};
			'''
		)

		self.central_widget_layout = QVBoxLayout(self.central_widget)
		self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

	def setup_layout_wrapper(self):
		self.layout_wrapper = LayoutWrapper(
			self.parent,
			bg_color=theme.BG_ONE,
			border_color=theme.BG_TWO,
			text_color=theme.TEXT_FOREGROUND
		)
		self.layout_wrapper.set_stylesheet(border_radius=0, border_size=0)
		self.central_widget_layout.addWidget(self.layout_wrapper)
	
	def setup_sidebar(self):
		sidebar_margin = settings.APP_SIDEBAR_MARGINS
		sidebar_minimum_width = settings.APP_SIDEBAR_WIDTH["minimum"]

		self.sidebar_frame = QFrame()
		self.sidebar_frame.setMaximumSize(sidebar_minimum_width + (sidebar_margin * 2), 17280)
		self.sidebar_frame.setMinimumSize(sidebar_minimum_width + (sidebar_margin * 2), 0)

		self.sidebar_layout = QHBoxLayout(self.sidebar_frame)
		self.sidebar_layout.setContentsMargins(
			sidebar_margin,
			sidebar_margin,
			sidebar_margin,
			sidebar_margin
		)

		self.sidebar = PyLeftMenu(
			parent=self.sidebar_frame,
			app_parent=self.central_widget,  # For tooltip parent
			dark_one=theme.DARK_ONE,
			dark_three=theme.DARK_THREE,
			dark_four=theme.DARK_FOUR,
			bg_one=theme.BG_ONE,
			icon_color=theme.ICON_COLOR,
			icon_color_hover=theme.ICON_HOVER,
			icon_color_pressed=theme.ICON_PRESSED,
			icon_color_active=theme.ICON_ACTIVE,
			context_color=theme.CONTEXT_COLOR,
			text_foreground=theme.TEXT_FOREGROUND,
			text_active=theme.TEXT_ACTIVE
		)
		self.sidebar_layout.addWidget(self.sidebar)
		self.layout_wrapper.layout.addWidget(self.sidebar_frame)
	
	def setup_container(self):
		self.container = QFrame()
		self.container_layout = QVBoxLayout(self.container)
		self.container_layout.setContentsMargins(3, 3, 3, 3)
		self.layout_wrapper.layout.addWidget(self.container)
	
	def setup_main_content(self):
		self.main_content_frame = QFrame()

		self.main_content_layout = QHBoxLayout(self.main_content_frame)
		self.main_content_layout.setContentsMargins(0, 0, 0, 0)
		self.main_content_layout.setSpacing(0)
		
		self.container_layout.addWidget(self.main_content_frame)
	
	def setup_left_page(self):
		self.left_page_frame = QFrame()
		self.main_content_layout.addWidget(self.left_page_frame)

	def setup_right_page(self):
		self.right_page_frame = QFrame()
		self.right_page_frame.setMinimumWidth(240)
		self.right_page_frame.setMaximumWidth(240)

		self.right_page_layout = QVBoxLayout(self.right_page_frame)
		self.right_page_layout.setContentsMargins(5, 5, 5, 5)
		self.right_page_layout.setSpacing(0)

		self.right_page_bg_frame = QFrame()
		self.right_page_bg_frame.setObjectName("right_page_bg_frame")
		self.right_page_bg_frame.setStyleSheet(f'''
		#right_page_bg_frame {{
		    border-radius: 8px;
		    background-color: {theme.BG_TWO};
		}}
		''')

		self.right_page_layout.addWidget(self.right_page_bg_frame)

		self.right_page_content = Ui_RightColumn()
		self.right_page_content.setupUi(self.right_page_bg_frame)

		self.main_content_layout.addWidget(self.right_page_frame)

	def setup_footer(self):
		self.footer_frame = QFrame()
		self.footer_frame.setMinimumHeight(26)
		self.footer_frame.setMaximumHeight(26)

		self.footer_layout = QVBoxLayout(self.footer_frame)
		self.footer_layout.setContentsMargins(0, 0, 0, 0)

		self.footer = Footer(
			bg_two=theme.BG_TWO,
			copyright=settings.COPYRIGHT,
			version=settings.VERSION,
			font_family=settings.APP_FONT["family"],
			text_size=settings.APP_FONT["text_size"],
			text_description_color=theme.TEXT_DESCRIPTION
		)

		self.footer_layout.addWidget(self.footer)
		self.container_layout.addWidget(self.footer_frame)

	def setup_titlebar(self):
		self.title_bar_frame = QFrame()
		self.title_bar_frame.setMinimumHeight(40)
		self.title_bar_frame.setMaximumHeight(40)

		self.title_bar_layout = QVBoxLayout(self.title_bar_frame)
		self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

		# ADD CUSTOM TITLE BAR TO LAYOUT
		self.title_bar = PyTitleBar(
			self.parent,
			logo_width=100,
			app_parent=self.central_widget,
			logo_image="logo_top_100x22.svg",
			bg_color=theme.BG_TWO,
			div_color=theme.BG_THREE,
			btn_bg_color=theme.BG_TWO,
			btn_bg_color_hover=theme.BG_THREE,
			btn_bg_color_pressed=theme.BG_ONE,
			icon_color=theme.ICON_COLOR,
			icon_color_hover=theme.ICON_HOVER,
			icon_color_pressed=theme.ICON_PRESSED,
			icon_color_active=theme.ICON_ACTIVE,
			context_color=theme.CONTEXT_COLOR,
			dark_one=theme.DARK_ONE,
			text_foreground=theme.TEXT_FOREGROUND,
			radius=8,
			font_family=settings.APP_FONT["family"],
			title_size=settings.APP_FONT["title_size"],
			is_custom_title_bar=settings.CUSTOM_TITLE_BAR
		)
		self.title_bar_layout.addWidget(self.title_bar)
		self.container_layout.addWidget(self.title_bar_frame)
		
	