#! /usr/bin/python3

import sys
import os
import os.path
import shutil
import glob
import subprocess
import time

debug=True

def _debug(msg):
	if debug:
		print("dbg: %s"%msg)

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
home_path=os.path.expanduser('~')
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

shutil.copy("/etc/xdg/lliurex/desktop/kwinrc","%s/.config/kwinrc"%home_path)
shutil.copy("/etc/xdg/lliurex/desktop/kdeglobals","%s/.config/kdeglobals"%home_path)

#restart plasma
subprocess.run(["/usr/bin/kstart5","plasmashell"])
time.sleep(3)

