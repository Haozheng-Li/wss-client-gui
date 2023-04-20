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

import datetime
from pathlib import Path

# Project GUI DIR

BASE_DIR = Path(__file__).resolve().parent.parent

# API_KEY for connection with WSS platform

WSS_SECRET_KEY = ''

# Application can run in command line mode or GUI mode

USE_GUI = True

# Development settings

DEBUG = True

INSTALLED_APPS = [
	'dashboard',
	'accessories',
]

# Application definition
APP_NAME = "WSS-Client"

VERSION = "1.0.0"

COPYRIGHT = "By: Haozheng Li"

COPYRIGHT_YEAR = datetime.datetime.today().year

# Static files (Images, QSS)

STATIC_ROOT = BASE_DIR / 'media'

# APP media file storage settings

MEDIA_ROOT = BASE_DIR / 'media'

# APP log files settings
LOG_ROOT = BASE_DIR / 'log'

# Application GUI settings

THEME = "default"
CUSTOM_TITLE_BAR = False

APP_ANIMATION_TIME = 500
APP_WINDOW_MINIUM_SIZE = (960, 540)
APP_WINDOW_START_UP_SIZE = (1400, 720)
APP_SIDEBAR_MARGINS = 3
APP_SIDEBAR_WIDTH = {"minimum": 50, "maximum": 240}
APP_RIGHT_COLUMN_SIZE = {"minimum": 0, "maximum": 260}
APP_FONT = {"family": "Segoe UI", "title_size": 10, "text_size": 9}






