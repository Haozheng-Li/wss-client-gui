# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/18
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

from wss.gui.style import theme_default
from wss.core import settings

THEME_DEFINE = {
	"default": theme_default
}


class Theme:
	def __init__(self):
		self.theme_settings = THEME_DEFINE.get(settings.THEME)
		if not self.theme_settings:
			raise RuntimeError('Theme name wrong or theme settings file does not exist')
		for setting in dir(self.theme_settings):
			if setting.isupper():
				setattr(self, setting, getattr(self.theme_settings, setting))


theme = Theme()
