#!/usr/bin/env python
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject, GLib

import signal
import gettext
import sys
import threading
import copy
import subprocess
import os

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('lliurex-pefilreset')
_ = gettext.gettext

import time


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

class LliurexPerfilreset:
	
	def __init__(self,args_dic):
		
		self.perfilreset_bin="/usr/sbin/lliurex-perfilreset"
		
		if args_dic["gui"]:
			
			self.start_gui()
			GObject.threads_init()
			Gtk.main()
		
	#def __init__(self):
	
	
	def start_gui(self):

		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-perfilreset')
		builder.add_from_file("/usr/share/lliurex-perfilreset/rsrc/lliurex-perfilreset.ui")
		self.main_window=builder.get_object("main_window")
		self.main_window.set_icon_from_file('/usr/share/lliurex-perfilreset/rsrc/lliurex-perfilreset-icon.svg')
		
		self.main_box=builder.get_object("main_box")
		
		self.close_button=builder.get_object("close_button")
		self.reset_button=builder.get_object("reset_button")
		
		self.connect_signals()
		self.main_window.show()
		
	#def start_gui
	
	
	def connect_signals(self):
		
		self.main_window.connect("destroy",Gtk.main_quit)
		
		self.close_button.connect("clicked",self.close_button_clicked)
		self.reset_button.connect("clicked",self.reset_button_clicked)
		
	#def connect_signals
	
	
	# SIGNALS ########################################################
	
	
	def close_button_clicked(self,widget=True):
		
		print ("Process closed")
		Gtk.main_quit()
		sys.exit(0)
		
	#def check_changes
	
	
	
	
	def reset_button_clicked(self,widget):
		spinner = Spinner()
		spinner.start()
		subprocess.call("/usr/sbin/lliurex-perfilreset 1", shell=True)
		os.system("pkill mate-panel")
		time.sleep(3)
		spinner.stop()
		#print ("hola")
		
	#def reset_clicked
	
	# ##################### ##########################################
	
	
	
#class LliurexPerfilreset


if __name__=="__main__":
	
	pass
	
