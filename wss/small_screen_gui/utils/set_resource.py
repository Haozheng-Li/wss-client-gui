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

import os
from wss.core import settings


def set_svg_icon(icon_name):
	app_path = str(settings.BASE_DIR)
	folder = "static/image/svg_icons/"
	path = os.path.join(app_path, folder)
	icon = os.path.normpath(os.path.join(path, icon_name))
	return icon


def set_svg_image(icon_name):
	app_path = str(settings.BASE_DIR)
	folder = "static/image/svg_images/"
	path = os.path.join(app_path, folder)
	icon = os.path.normpath(os.path.join(path, icon_name))
	return icon


def set_image(image_name):
	app_path = str(settings.BASE_DIR)
	folder = "static/image/images/"
	path = os.path.join(app_path, folder)
	image = os.path.normpath(os.path.join(path, image_name))
	return image