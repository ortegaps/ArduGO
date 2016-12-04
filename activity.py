# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import logging
import pygtk
pygtk.require('2.0')
import gtk
import serial

from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton
from shutil import copyfile


class Ardugo(activity.Activity):
   
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()



        self.ventana = gtk.VBox()
        var = serial.Serial('/dev/ttyACM0', 9600)
        self.ba = gtk.Button("Encender LED")
        self.bb = gtk.Button("Apagar LED")
        self.bc = gtk.Button("Flash LED")
        self.ardugo = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file('activity/ardu.svg')
        scaled_pixbuf = pixbuf.scale_simple(400,400,gtk.gdk.INTERP_BILINEAR)
        self.ardugo.set_from_pixbuf(scaled_pixbuf)
        self.ventana.add(self.ardugo)
        self.ventana.add(self.ba)
        self.ventana.add(self.bb)
        self.ventana.add(self.bc)
        self.set_canvas(self.ventana)
    	self.ventana.show_all()

        def vara(self):
        	var.write('a')
        self.ba.connect('clicked',vara)

        def varb(self):
        	var.write('b')
        self.bb.connect('clicked',varb)

        def varc(self):
        	var.write('c')
        self.bc.connect('clicked',varc)