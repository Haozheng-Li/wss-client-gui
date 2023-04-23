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
from wss.gui.widget.sidebar import PyLeftMenu
from wss.gui.widget.sidebar_new import SidebarMenu
from wss.gui.widget.title_bar import PyTitleBar

from wss.gui.widget.footer import Footer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget


class UIMainWindow(object):
    def __init__(self):
        self.app_stacked_widget = None
        self.right_app_page_container = None
        self.layout_wrapper_layout = None
        self.left_page_frame_layout = None
        self.left_app_page_container = None
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
        self.left_app_pages = []

        self.parent = None

    def setup_ui(self, parent):
        self.parent = parent

        self.setup_central_widget()
        self.setup_layout_wrapper()
        self.setup_sidebar()
        self.setup_container()
        self.setup_titlebar()
        self.setup_main_content()
        self.setup_app_stacked_widget()
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
        self.layout_wrapper = QFrame()
        self.layout_wrapper.setObjectName("layout_wrapper")

        self.layout_wrapper_layout = QHBoxLayout(self.layout_wrapper)
        self.layout_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.layout_wrapper_layout.setSpacing(2)

        layout_wrapper_style = f"""
        #layout_wrapper {{
        background-color: {theme.BG_ONE};
        border-radius: 0;
        border: 0px solid {theme.BG_TWO};}}
        QFrame {{ 
        color: {theme.TEXT_FOREGROUND};
        font: {settings.APP_FONT['text_size']}pt '{settings.APP_FONT['family']}';
        }}
        """
        self.layout_wrapper.setStyleSheet(layout_wrapper_style)

        self.central_widget_layout.addWidget(self.layout_wrapper)

    def setup_sidebar(self):
        sidebar_margin = settings.APP_SIDEBAR_MARGINS
        sidebar_maximum_width = settings.APP_SIDEBAR_WIDTH["maximum"]

        self.sidebar_frame = QFrame()
        self.sidebar_frame.setMaximumSize(sidebar_maximum_width + (sidebar_margin * 2), 17280)
        self.sidebar_frame.setMinimumSize(sidebar_maximum_width + (sidebar_margin * 2), 0)

        self.sidebar_layout = QHBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(
            sidebar_margin,
            sidebar_margin,
            sidebar_margin,
            sidebar_margin
        )

        # self.sidebar = PyLeftMenu(
        #     parent=self.sidebar_frame,
        #     app_parent=self.central_widget,  # For tooltip parent
        #     dark_one=theme.DARK_ONE,
        #     dark_three=theme.DARK_THREE,
        #     dark_four=theme.DARK_FOUR,
        #     bg_one=theme.BG_ONE,
        #     icon_color=theme.ICON_COLOR,
        #     icon_color_hover=theme.ICON_HOVER,
        #     icon_color_pressed=theme.ICON_PRESSED,
        #     icon_color_active=theme.ICON_ACTIVE,
        #     context_color=theme.CONTEXT_COLOR,
        #     text_foreground=theme.TEXT_FOREGROUND,
        #     text_active=theme.TEXT_ACTIVE
        # )
        self.sidebar = SidebarMenu()
        self.sidebar_layout.addWidget(self.sidebar)
        self.layout_wrapper_layout.addWidget(self.sidebar_frame)

    def setup_container(self):
        self.container = QFrame()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(5, 3, 5, 3)
        self.layout_wrapper_layout.addWidget(self.container)

    def setup_main_content(self):
        self.main_content_frame = QFrame()
        self.main_content_frame.setObjectName("main_content_frame")
        self.main_content_layout = QHBoxLayout(self.main_content_frame)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(0)

        self.container_layout.addWidget(self.main_content_frame)

    def setup_app_stacked_widget(self):
        self.app_stacked_widget = QStackedWidget(self.left_page_frame)
        self.app_stacked_widget.setObjectName(u"app_stacked_widget")
        self.main_content_frame.setStyleSheet(f'''
        #app_stacked_widget {{
        border-radius: 8px;
        background-color: {theme.BG_ONE};
        }}''')

        self.main_content_layout.addWidget(self.app_stacked_widget)

    def add_app(self, app_page_obj):
        self.app_stacked_widget.addWidget(app_page_obj)

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
