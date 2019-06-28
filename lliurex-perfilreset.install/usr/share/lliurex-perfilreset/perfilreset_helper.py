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
home_path="%s/%s"%(os.environ['HOME'],".config")
kdeglobals="%s/kdeglobals"%home_path

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

#restore default configs
_copy_tree("/etc/xdg/lliurex/desktop",home_path)
#Set color scheme
if os.path.isfile(color_scheme):
	with open (color_scheme,'r') as f:
		f_contents=f.readlines()
	with open (kdeglobals,'a') as f:
		f.writelines(f_contents)

#restart plasma
subprocess.run(["/usr/bin/kstart5","plasmashell"])
time.sleep(3)

