# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from horizons.command.game import PauseCommand, UnPauseCommand
from horizons.gui.modules.settings import SettingsDialog
from horizons.gui.modules.editorstartmenu import EditorStartMenu
from horizons.gui.util import load_uh_widget
from horizons.gui.windows import Window


class PauseMenu(Window):

	def __init__(self, session, mainmenu, ingame_gui, windows, in_editor_mode=False):
		super(PauseMenu, self).__init__(windows)

		self._session = session
		self._mainmenu = mainmenu
		self._ingame_gui = ingame_gui

		self.settings_dialog = SettingsDialog(self._windows)

		name = 'editor_pause_menu.xml' if in_editor_mode else 'ingamemenu.xml'
		self._gui = load_uh_widget(name)
		self._gui.position_technique = 'center:center'

		events = {
			'load' : self._show_editor_start_menu if in_editor_mode else mainmenu.load_game,
			'save' : ingame_gui.show_save_map_dialog if in_editor_mode else mainmenu.save_game,
			'sett' : lambda: self._windows.show(self.settings_dialog),
			'help' : ingame_gui.toggle_help,
			'start': self._windows.close,
			'quit' : self._do_quit,
		}

		self._gui.mapEvents({
			# icons
			'loadgameButton': events['load'],
			'savegameButton': events['save'],
			'settingsLink'  : events['sett'],
			'helpLink'      : events['help'],
			'startGame'     : events['start'],
			'closeButton'   : events['quit'],
			# labels
			'loadgame': events['load'],
			'savegame': events['save'],
			'settings': events['sett'],
			'help'    : events['help'],
			'start'   : events['start'],
			'quit'    : events['quit'],
		})

	def show(self):
		PauseCommand(suggestion=True).execute(self._session)
		self._gui.show()

	def hide(self):
		self._gui.hide()
		UnPauseCommand(suggestion=True).execute(self._session)

	def _do_quit(self):
		message = _("Are you sure you want to abort the running session?")
		if self._windows.show_popup(_("Quit Session"), message, show_cancel_button=True):
			self._session.quit()

	def _show_editor_start_menu(self):
		editor_start_menu = EditorStartMenu(self._mainmenu, self._windows)
		self._windows.show(editor_start_menu)
