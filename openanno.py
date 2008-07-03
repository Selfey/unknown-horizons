#!/usr/bin/env python

# ###################################################
# Copyright (C) 2008 The OpenAnno Team
# team@openanno.org
# This file is part of OpenAnno.
#
# OpenAnno is free software; you can redistribute it and/or modify
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

import sys
import os

def findFIFE():
	global fife_path
	try:
		import config
		_paths = [config.fife_path]
	except (ImportError, AttributeError):
		_paths = []
	_paths += [ a + '/' + b + '/' + c for a in ('.', '..', '../..') for b in ('.', 'fife', 'FIFE', 'Fife') for c in ('.', 'trunk') ]

	fife_path = None
	for p in _paths:
		if p not in sys.path:
			# check if we are in a fife dir...
			for pe in [ os.path.abspath(p + '/' + a) for a in ('.', 'engine', 'engine/extensions', 'engine/swigwrappers/python') ]:
				if not os.path.exists(pe):
					break
			else:
				fife_path = p
				print "Found FIFE in:", fife_path

				#add python paths (<fife>/engine/extensions <fife>/engine/swigwrappers/python)
				for pe in [ os.path.abspath(fife_path + '/' + a) for a in ('engine/extensions', 'engine/swigwrappers/python') ]:
					if os.path.exists(pe):
						sys.path.append(pe)
				os.environ['PYTHONPATH'] = os.path.pathsep.join(os.environ.get('PYTHONPATH', '').split(os.path.pathsep) + [ os.path.abspath(fife_path + '/' + a) for a in ('engine/extensions', 'engine/swigwrappers/python') ])

				#add windows paths (<fife>/.)
				os.environ['PATH'] = os.path.pathsep.join(os.environ.get('PATH', '').split(os.path.pathsep) + [ os.path.abspath(fife_path + '/' + a) for a in ('.') ])
				os.path.defpath += os.path.pathsep + os.path.pathsep.join([ os.path.abspath(fife_path + '/' + a) for a in ('.') ])
				break
	else:
		print 'FIFE was not found.'
		print "Please create a config.py file and add a line with: fife_path = '<path to fife>' eg. fife_path = '../../fife/trunk/'"
		exit()

	try:
		if not os.environ.get('LD_LIBRARY_PATH', '').startswith(os.path.abspath(fife_path)):
			try:
				import fife
			except ImportError, e:
				os.environ['LD_LIBRARY_PATH'] = os.path.pathsep.join([ os.path.abspath(p + '/' + a) for a in ('ext/minizip', 'ext/install/lib') ] + (os.environ['LD_LIBRARY_PATH'].split(os.path.pathsep) if os.environ.has_key('LD_LIBRARY_PATH') else []))
				print "Restarting with proper LD_LIBRARY_PATH..."
				args = [sys.executable] + sys.argv
				#we are already in openanno root, so just exec local executeable
				args[1] = "openanno.py"
				os.execvp(args[0], args)
		else:
			import fife
	except ImportError, e:
		print 'FIFE was not found or failed to load'
		print 'Reason: ' + e.message
		print "Please create a config.py file and add a line with: path = '<path to fife>' eg. path = '../../fife/trunk/'"
		exit()

if __name__ == '__main__':
	#chdir to openanno root
	os.chdir( os.path.split( os.path.realpath( sys.argv[0]) )[0] )

	#find fife and setup search paths
	findFIFE()

	#for some external libraries distributed with openanno
	sys.path.append('game/ext')

	#start openanno
	import game.main
	game.main.start()
