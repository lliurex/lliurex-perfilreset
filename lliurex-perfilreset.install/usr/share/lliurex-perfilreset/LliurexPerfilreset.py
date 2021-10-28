#!/usr/bin/env python
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject, GLib, Gdk

import signal
import gettext
import sys
import threading
import copy
import subprocess
import os

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('lliurex-perfilreset')
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
		
		self.perfilreset_bin="/usr/share/lliurex-perfilreset/perfilreset_helper.py"
		self.applied=False
		
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
		self.main_window.set_resizable(False)
		self.main_window.set_icon_from_file('/usr/share/lliurex-perfilreset/rsrc/lliurex-perfilreset-icon.svg')
		self._set_css_info()
		self.main_window.set_name("WINDOW")
		self.main_box=builder.get_object("main_box")
		
		self.close_button=builder.get_object("close_button")
		self.msg_label=builder.get_object("msg_label")
		self.msg_label.set_name("MSG_LABEL")
		self.reset_button=builder.get_object("reset_button")
		
		self.reveal=Gtk.Revealer()
		self.reveal.set_name("WHITE_BACKGROUND")
		self.reveal.set_transition_duration(1)

		lbl_rvl=Gtk.Label(_("Resetting profile..."))
		lbl_rvl.set_name("NOTIF_LABEL")
		lbl_rvl.set_hexpand(False)
		lbl_rvl.set_vexpand(False)
		lbl_rvl.set_halign(Gtk.Align.CENTER)
		lbl_rvl.set_valign(Gtk.Align.CENTER)
		self.reveal.add(lbl_rvl)
		self.main_box.attach(self.reveal,0,0,1,4)
		
		self.connect_signals()
		self.main_window.show_all()
		self.msg_label.hide()
		self.lock_quit=False
		self.detect_konsole()
		
	#def start_gui
	
	
	def connect_signals(self):
		
		self.main_window.connect("destroy",self.close_button_clicked)
		self.main_window.connect("delete_event",self.unable_quit)
		self.close_button.connect("clicked",self.close_button_clicked)
		self.reset_button.connect("clicked",self.reset_button_clicked)
		
	#def connect_signals
	
	
	# SIGNALS ########################################################
	
	
	def close_button_clicked(self,widget=True):
		
		Gtk.main_quit()
		if self.applied:
			subprocess.run(["loginctl","terminate-user","%s"%os.environ['USER']])
		sys.exit(0)
		
	#def check_changes
	
	def reset_button_clicked(self,widget):
		self.applied=True

		self.reset_button.set_sensitive(False)
		self.lock_quit=True
		self.msg_label.set_text("")
		spinner = Spinner()
		spinner.start()
		self.retcode=None
		self.reveal.set_reveal_child(True)
		th=threading.Thread(target=self._th_reset_profile)
		GLib.timeout_add(1000,self.show_reveal,th)
		th.start()
		self.retcode=1
		spinner.stop()
	#def reset_clicked
	
	# ##################### ##########################################
	
	def _th_reset_profile(self,*args):
		time.sleep(1)
		subprocess.run(["/usr/share/lliurex-perfilreset/perfilreset_helper.py","1"])
		time.sleep(5)

	def show_reveal(self,*args):
		th=args[-1]
		if th.is_alive():
			return True
		self.reveal.set_reveal_child(False)
		self.reset_button.set_sensitive(True)
		self.lock_quit=False
		#self.msg_label.set_text(_("You must restart the session to end the process"))
		self.msg_label.set_text(_("Close this window to restart the session and apply changes"))
		self.msg_label.show()

		return False
	
	def _set_css_info(self):
	
		css = b"""

		GtkLabel {
			font-family: Roboto;
		}

		#WINDOW{
		
		background-color: #ffffff;
		
		}

		#NOTIF_LABEL{
			background: #3366cc;
			font: 11px Roboto;
			color:white;
			border: dashed 1px silver;
			padding:6px;
		}

		#MSG_LABEL {
			color: #24478f;
			font: 11pt Roboto Bold;

		}

		#WHITE_BACKGROUND {
			background: rgba(1,1,1,0);
			box-shadow: 1px 1px 1px 10px white;
		
		}

		"""
		self.style_provider=Gtk.CssProvider()
		self.style_provider.load_from_data(css)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	#def set_css_info	

	def detect_konsole(self):

		cmd='ps -ef | grep "konsole" | grep -v "grep"'
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		data=p.communicate()[0]

		if type(data) is bytes:
			result=data.decode()
		else:
			result=data
		isrunning= [ x.strip() for x in result.split('\n') ]
		isrunning.pop()
		count=len(isrunning)
		if count>0:
			msg_alert=(_("%s open terminals have been detected.\nIn order for the terminal configuration to be restored they must be\nclosed before starting the process")%count)
			self.msg_label.set_text(msg_alert)
			self.msg_label.show()

	#def detect_konsole
	
	def unable_quit(self,widget,event):

		if self.lock_quit:
			if self.applied:
				subprocess.run(["loginctl","terminate-user","%s"%os.environ['USER']])
			return True
		else:	
			return False
			
	#def unable_quit		
	
#class LliurexPerfilreset


if __name__=="__main__":
	
	pass
	
