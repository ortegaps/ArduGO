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
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from ConfigParser import SafeConfigParser
import logging
import random


import logging
import pty

import shlex
import subprocess
from threading import Thread
import os
import sys
import shlex
import subprocess
from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem

from shutil import copyfile


class Ardugo(activity.Activity):

    def make(self, install):
        pid, fd = pty.fork()
        if pid == 0:
            for i in range(2):
                self.install()

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

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        # Uso un widget principal para los problemas de resolucion x2..
        self.widget_principal = Gtk.EventBox()
        self.crear_menu()
        self.scroll.add(self.widget_principal)
        self.maximize()
       # self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        self.widget_principal.modify_bg(
            Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        self.set_canvas(self.scroll)
        self.scroll.show_all()

    def crear_menu(self):
        self.menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Logos = Gtk.Image()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            'activity/inicio.svg', 1050, 600)
        Logos.set_from_pixbuf(pixbuf)
        Install = Gtk.Button(_('Install Arduino'))
        Install.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Run = Gtk.Button(_('Run Arduino'))
        Run.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Arduino = Gtk.Button(_('What is Arduino'))
        Arduino.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Help = Gtk.Button(_('Help'))
        Help.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        self.menu.add(Logos)
        self.menu.add(Install)
        self.menu.add(Run)
        self.menu.add(Arduino)
        self.menu.add(Help)

        # Diseno
        self.menu.pack_start(Logos, True, False, 10)
        self.menu.pack_start(Install, True, True, 10)
        self.menu.pack_start(Run, True, True, 10)
        self.menu.pack_start(Arduino, False, False, 5)
        self.menu.pack_start(Help, False, False, 5)
        Install.connect('clicked', self.widget_install)
        Arduino.connect('clicked', self.introduction)
        Run.connect('clicked', self.run)
        Help.connect('clicked', self.help)
        self.menu.show_all()
        self.widget_principal.add(self.menu)
        self.widget_principal.show_all()

    def limpiar_ventana(self):
        for widget in self.widget_principal.get_children():
            self.widget_principal.remove(widget)

    def entrar_a_menu(self, widget=None):
        if not self.menu:
            self.crear_menu()

        self.limpiar_ventana()
        self.widget_principal.add(self.menu)
        self.widget_principal.show_all()

    def introduction(self, Arduino):
        self.limpiar_ventana()

        introduction = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        titulo = Gtk.Label(_('Introduction on Arduino Board'))
        titulo.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        info = Gtk.TextView()
        info.set_wrap_mode(Gtk.WrapMode.WORD)
        info.set_editable(False)

        textbuffer = info.get_buffer()
        textbuffer.set_text(_("\nWhat is Arduino?\n"

 "\nArduino is an open-source electronics platform based on easy-to-use hardware and software.\n" 
 "Arduino boards are able to read inputs - light on a sensor, a finger on a button, or a Twitter message - and turn it into an output - activating a motor, turning on an LED, publishing something online.\n"
 "You can tell your board what to do by sending a set of instructions to the microcontroller on the board.\n"
 "To do so you use the Arduino programming language (based on Wiring), and the Arduino Software (IDE), based on Processing Over the years.\n"
 "Arduino has been the brain of thousands of projects, from everyday objects to complex scientific instruments.\n"
 "A worldwide community of makers - students, hobbyists, artists, programmers, and professionals - has gathered around this open-source platform,\n" " their contributions have added up to an incredible amount of"
  "accessible knowledge that can be of great help to novices and experts alike.\n"
  "differentiating its offer from simple 8-bit boards to products for IoT applications, wearable, 3D printing, and embedded environments. All Arduino boards are completely open-source, "
  "empowering users to build them independently and eventually adapt them to their particular needs. The software, too, is open-source, and it is growing through the contributions of users worldwide.\n"

 "\nWhy Arduino?\n"

 
 "\nThanks to its simple and accessible user experience, Arduino has been used in thousands of different projects and applications.\n"
  "The Arduino software is easy-to-use for beginners, yet flexible enough for advanced users.\n" 
 "It runs on Mac, Windows, and Linux. Teachers and students use it to build low cost scientific instruments, "
 "to prove chemistry and physics principles, or to get started with programming and robotics.\n" "Designers and architects build interactive prototypes, musicians and artists use it for installations and to experiment with new musical instruments." 
 "Makers, of course, use it to build many of the projects exhibited at the Maker Faire, for example." 
 "\nArduino is a key tool to learn new things. Anyone - children, hobbyists, artists, programmers - can start tinkering just following the step by step instructions of a kit, or sharing ideas online with other members of the Arduino community."

 "\nThere are many other microcontrollers and microcontroller platforms available for physical computing. " "Parallax Basic Stamp, Netmedia's BX-24, Phidgets, MIT's Handyboard, and many others offer similar functionality.\n" 
 "All of these tools take the messy details of microcontroller programming and wrap it up in an easy-to-use package. " 
 "Arduino also simplifies the process of working with microcontrollers, but it offers some advantage for teachers, students, and interested amateurs over other systems:\n"

	"Inexpensive - Arduino boards are relatively inexpensive compared to other microcontroller platforms." 
	"\nThe least expensive version of the Arduino module can be assembled by hand, and even the pre-assembled Arduino modules cost less than $50"
    "\nCross-platform - The Arduino Software (IDE) runs on Windows, Macintosh OSX, and Linux operating systems. Most microcontroller systems are limited to Windows."
    "\nSimple, clear programming environment - The Arduino Software (IDE) is easy-to-use for beginners, yet flexible enough for advanced users to take advantage of as well."
    "\nFor teachers, it's conveniently based on the Processing programming environment, so students learning to program in that environment will be familiar with how the Arduino IDE works."
    "\nOpen source and extensible software - The Arduino software is published as open source tools, available for extension by experienced programmers. "
    "\nThe language can be expanded through C++ libraries, and people wanting to understand the technical details can make the leap from Arduino to the AVR C programming language on which it's based."
    "\nSimilarly, you can add AVR-C code directly into your Arduino programs if you want to."

 "Open source and extensible hardware - The plans of the Arduino boards are published under a Creative Commons license, so experienced circuit designers can make their own version of the module, extending it and improving it. "
 "Even relatively inexperienced users can build the breadboard version of the module in order to understand how it works and save money.\n"

 "\nHow do I use Arduino?\n"

 "\nSee the getting started guide. If you are looking for inspiration you can find a great variety of Tutorials on Arduino Project Hub.\n"
 "The text of the Arduino getting started guide is licensed under a Creative Commons Attribution-ShareAlike 3.0 License. Code samples in the guide are released into the public domain.\n"

 "\nInformation from https://www.arduino.cc/en/Guide/Introduction"))

        quit = Gtk.Button(_('Exit'))
        quit.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))

        Arduino.connect('clicked', self.introduction)

        quit.connect('clicked', self.entrar_a_menu)

        introduction.pack_start(titulo, False, False, 0)
        introduction.pack_start(info, True, True, 10)
        introduction.pack_start(quit, False, False, 10)

        self.widget_principal.add(introduction)
        self.show_all()

    def help(self, Help):
        self.limpiar_ventana()

        helping = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title = Gtk.Label(_('Help if you can not connect your arduino board'))
        title.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        infor = Gtk.TextView()
        infor.set_wrap_mode(Gtk.WrapMode.WORD)
        infor.set_editable(False)

        textbuffer = infor.get_buffer()
        textbuffer.set_text(_("\nIf you can not connect your Arduino board, these could be some problems.\n"  "\nProblem: The serial port can not establish connection to the board.\n"  
        "\nSolution: Give permissions to the desired port for example :\n" "<ACM0> entering the terminal and typing\n" "\n$ sudo chmod 777 /dev/ACM0\n" 
        "\nor if you do not know which port you can give permissions to all ports with\n" "\n$ sudo chmod 777 /dev/*\n"
 		"\nYou may have selected your board appropriately, but with the wrong microcontroller option. Make sure the microcontroller matches your board\n"
 		"(either ATmega8, ATmega168, ATmega328, or ATmega1280) - the name is written on the largest chip on the board.\n"

 		"\nCheck if you use a noisy power supply. This could cause the chip to lose its sketch.\n"

		"\nOn the other hand, the sketch may be too large for the card. When you upload your sketch, Arduino 0004 and later check if it is too large for the ATmega8,\n"
		"but base your calculation on a 1 Kb bootloader. You could have larger size bulbs (eg 2 Kb of the 8 Kb available on your board) . If you use official Arduino boards,\n"
		"this problem will not occur.\n"))


        quiti = Gtk.Button(_('Exit'))
        quiti.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        Help.connect('clicked', self.help)

        quiti.connect('clicked', self.entrar_a_menu)

        helping.pack_start(title, False, False, 0)
        helping.pack_start(infor, True, True, 10)
        helping.pack_start(quiti, False, False, 10)

        self.widget_principal.add(helping)
        self.widget_principal.show_all()

    def widget_install(self, Help):
        self.limpiar_ventana()
        installing = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title = Gtk.Label(
            _('Steps to install Arduino IDE an pyserial on your XO'))
        title.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        informa = Gtk.TextView()
        informa.set_wrap_mode(Gtk.WrapMode.WORD)
        informa.set_editable(False)

        textbuffer = informa.get_buffer()
        textbuffer.set_text(_("To install the Arduino IDE you must enter the Terminal Activity and type these commands:\n"
"First step: To locate in the directory where the package to install is located for that type\n" "\n$cd /home/olpc/Activities/ArduGO.activity/\n" "\nor some other location depending on how they are ripping Sugar.\n"

 "\nSecond Step: Install the Arduino package on your system, for that you write in the terminal:\n" "\n$sudo yum install -y arduino-1.0.5-6.fc20.noarch\n"
       
 "\nThird Step: Install the Pyserial package on your system, for that you write in the terminal:\n" "\n$sudo yum install -y pyserial-2.7-1.fc20.noarch\n"
      
 "\nThen you can start IDE Arduino from the main menu :)"))

        exit = Gtk.Button(_('Exit'))

        exit.connect('clicked', self.entrar_a_menu)
        exit.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("light blue"))
        installing.pack_start(title, False, False, 10)
        installing.pack_start(informa, True, True, 10)
        installing.pack_start(exit, False, False, 10)

        self.widget_principal.add(installing)
        self.widget_principal.show_all()

    def run_command(self, cmd):
        os.system(cmd)

    def install_paquete(self):
        paquete = "arduino-1.0.5-6.fc20.noarch"
        self.run_command("yum install -y " + paquete)

    def install_paquete2(self):
        paquete2 = "pyserial-2.7-1.fc20.noarch"
        self.run_command("yum install -y " + paquete2)

    def run(self, Arduino):
        self.run_command("arduino")
        self.run_command("sudo chmod 777 /dev/*")

    def install(self):
        self.install_paquete()
        self.install_paquete2()
        os._exit(os.EX_OK)
