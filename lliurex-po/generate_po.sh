#!/bin/bash

UI_FILES="../lliurex-perfilreset.install/usr/share/lliurex-perfilreset/rsrc/lliurex-perfilreset.ui "
PYTHON_FILES="../lliurex-perfilreset.install/usr/share/lliurex-perfilreset/LliurexPerfilreset.py"

xgettext $UI_FILES $PYTHON_FILES -o lliurex-perfilreset/lliurex-perfilreset.pot

