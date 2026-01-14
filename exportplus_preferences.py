# SPDX-License-Identifier: LGPL-2.1-or-later
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2026 ExportPlus Workbench                               *
# *                                                                         *
# *   This file is part of FreeCAD.                                         *
# *                                                                         *
# *   FreeCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with FreeCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""Preferences page for ExportPlus workbench with button functionality"""

import os
import FreeCAD
from PySide import QtCore, QtGui, QtUiTools


class PreferencesHelper(QtCore.QObject):
    """Helper class to connect preset buttons after UI loads"""

    def __init__(self, parent=None):
        super(PreferencesHelper, self).__init__(parent)

    def setupConnections(self):
        """Find and connect the preset buttons in the preferences dialog"""
        # This gets called after a short delay to ensure widgets are loaded
        from PySide import QtGui

        app = QtGui.QApplication.instance()
        if not app:
            return

        # Find all widgets and look for our preference page
        for widget in app.allWidgets():
            if not widget:
                continue

            # Try to find our specific widgets
            spinBox = None
            btnMM = None
            btnInches = None
            btnCM = None
            btnMeters = None

            # Search for children
            for child in widget.findChildren(QtGui.QDoubleSpinBox):
                if child.objectName() == "doubleSpinBoxGlobalScale":
                    spinBox = child
                    break

            if spinBox:
                # Found the spinbox, now find buttons
                parent = spinBox.parent()
                while parent and not btnMM:
                    for btn in parent.findChildren(QtGui.QPushButton):
                        name = btn.objectName()
                        if name == "btnPresetMM":
                            btnMM = btn
                        elif name == "btnPresetInches":
                            btnInches = btn
                        elif name == "btnPresetCM":
                            btnCM = btn
                        elif name == "btnPresetMeters":
                            btnMeters = btn
                    parent = parent.parent() if parent else None

                # Connect the buttons
                if btnMM:
                    try:
                        btnMM.clicked.disconnect()  # Disconnect any existing
                    except:
                        pass
                    btnMM.clicked.connect(lambda: spinBox.setValue(1.0))

                if btnInches:
                    try:
                        btnInches.clicked.disconnect()
                    except:
                        pass
                    btnInches.clicked.connect(lambda: spinBox.setValue(0.0393701))

                if btnCM:
                    try:
                        btnCM.clicked.disconnect()
                    except:
                        pass
                    btnCM.clicked.connect(lambda: spinBox.setValue(0.1))

                if btnMeters:
                    try:
                        btnMeters.clicked.disconnect()
                    except:
                        pass
                    btnMeters.clicked.connect(lambda: spinBox.setValue(0.001))

                FreeCAD.Console.PrintLog("ExportPlus: Preset buttons connected\n")
                break


# Global helper instance
_prefs_helper = None


def connectPreferenceButtons():
    """Public function to connect preference page buttons"""
    global _prefs_helper

    if _prefs_helper is None:
        _prefs_helper = PreferencesHelper()

    # Use a timer to delay the connection until widgets are ready
    QtCore.QTimer.singleShot(500, _prefs_helper.setupConnections)
