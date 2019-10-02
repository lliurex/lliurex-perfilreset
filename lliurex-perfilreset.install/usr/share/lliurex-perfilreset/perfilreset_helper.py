#! /usr/bin/python3

import sys
import os
import os.path
import shutil
import glob
import subprocess
import time

debug=False
color_scheme="/usr/share/color-schemes/lliurex.colors"
home_path="%s"%(os.environ['HOME'])
#kdeglobals="%s/kdeglobals"%home_path

def _debug(msg):
	if debug:
		print("dbg: %s"%msg)

def _copy_tree(path,dst):
	_debug("Read %s"%path)
	if not(os.path.isdir(dst)):
		_debug("Mkdir %s"%dst)
		os.makedirs(dst)
	for conf in os.listdir(path):
		confpath="%s/%s"%(path,conf)
		if os.path.isdir(confpath):
			_copy_tree(confpath,dst+"/"+conf)
		else:
			_debug("Copy %s"%confpath)
			shutil.copy(confpath,"%s/"%dst)

def delete_item(item):
	if os.path.isdir(item):
		_debug("dir %s"%item)
		shutil.rmtree(item)
	elif os.path.isfile(item):
		_debug("file %s"%item)
		os.remove(item)
	else:
		_debug("Not found %s"%item)
#def delete_item

def delete_glob(file_glob):
	for item in glob.glob(file_glob):
		_debug("glob %s"%item)
		delete_item(item)
#def delete_glob

def copy_skel_files():
	
	try:
		# Resetting kconsole config
		file_to_copy="/etc/skel/.local/share/konsole/lliurex.profile"
		dest_path=home_path+"/.local/share/konsole/"
		if not os.path.exists(dest_path):
			try:
				os.mkdir(dest_path)
			except Exception as e:
				debug_msg="Error creating %s"%dest_path+". Error:%s"%str(e)
				_debug(debug_msg)
				pass
		
		shutil.copy(file_to_copy,dest_path)
		
		file_to_remove=home_path+"/.config/konsolerc"
		if os.path.exists(file_to_remove):
			os.remove(file_to_remove)
		
		#Resetting ballofilerc
		file_to_copy="/etc/skel/.config/baloofilerc"
		dest_path=home_path+"/.config/"
		shutil.copy(file_to_copy,dest_path)
		
	except Exception as e:

		debug_msg="Error coping skel files %s"%str(e)
		_debug(debug_msg)
		pass

###MAIN

#Quit plasmashell
subprocess.run(["/usr/bin/kquitapp5","plasmashell"])

#Remove all kde config
kde_files=[]
for item in ["plasmashell*","org.kde.dirmodel-qml.kcache","kioexec","krunner","ksycoca5*","krunnerbookmarkrunnerfirefoxdbfile.sqlite"]:
	kde_files.append("%s/.cache/%s"%(home_path,item))
kde_config=[]
for item in ["plasma*","kde*","akonadi*","KDE","kconf_udpaterc","baloo*","dolphinrc","drkonqirc","gwenviewrc","k*rc","katemetainfos"]:
	kde_files.append("%s/.config/%s"%(home_path,item))
kde_local=[]
for item in ["kate","kded5","klipper","knewstuff3","kscreen","konsole","kwalletd","ksysguard","kmail2","kcookiejar","kactivitymanagerd"]:
	kde_files.append("%s/.local/%s"%(home_path,item))
for item in ["dolphin","kate","kcookiejar","kded5","keyrings","klipper","kmail2","knewstuff3","konsole","kscreen","ksysguard","kwalletd",\
				"kxmlgui5","plasma_engine_comic","plasma","plasma_notes","org.kde.gwenview"]:
	kde_files.append("%s/.local/share/%s"%(home_path,item))

for item in kde_files:
	if '*' in item:
		delete_glob(item)
	else:
		delete_item(item)

#Restore some files of skel
copy_skel_files()

'''
#restore default configs
_copy_tree("/etc/xdg/lliurex/desktop",home_path)

#Set color scheme
if os.path.isfile(color_scheme):
	with open (color_scheme,'r') as f:
		f_contents=f.readlines()
	with open (kdeglobals,'a') as f:
		f.writelines(f_contents)
'''
#restart plasma
subprocess.run(["/usr/bin/kstart5","plasmashell"])
time.sleep(60)

