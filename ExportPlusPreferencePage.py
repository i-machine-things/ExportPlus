# SPDX-License-Identifier: LGPL-2.1-or-later

"""Custom preference page class for ExportPlus that handles button connections"""

import os
import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui


class ExportPlusPreferencePage:
    """Preference page class with connected preset buttons"""

    def __init__(self):
        # Load the UI file
        self.form = self.loadUi()

        if self.form:
            # Connect the preset buttons immediately
            try:
                self.form.btnPresetMM.clicked.connect(lambda: self.form.doubleSpinBoxGlobalScale.setValue(1.0))
                self.form.btnPresetInches.clicked.connect(lambda: self.form.doubleSpinBoxGlobalScale.setValue(0.0393701))
                self.form.btnPresetCM.clicked.connect(lambda: self.form.doubleSpinBoxGlobalScale.setValue(0.1))
                self.form.btnPresetMeters.clicked.connect(lambda: self.form.doubleSpinBoxGlobalScale.setValue(0.001))
                FreeCAD.Console.PrintLog("ExportPlus: Preset buttons connected successfully\n")
            except Exception as e:
                FreeCAD.Console.PrintWarning(f"ExportPlus: Failed to connect buttons: {e}\n")

    def loadUi(self):
        """Load the UI file and return the widget"""
        # Find the UI file
        import sys
        ui_path = None

        for path in sys.path:
            candidate = os.path.join(path, "ExportPlus", "Resources", "ui", "preferences-exportplus.ui")
            if os.path.exists(candidate):
                ui_path = candidate
                break

        if not ui_path:
            # Try alternate locations
            possible_paths = [
                os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "ExportPlus", "Resources", "ui", "preferences-exportplus.ui"),
                os.path.join(FreeCAD.getResourceDir(), "..", "Mod", "ExportPlus", "Resources", "ui", "preferences-exportplus.ui"),
                os.path.join(FreeCAD.getResourceDir(), "Mod", "ExportPlus", "Resources", "ui", "preferences-exportplus.ui"),
            ]

            for path in possible_paths:
                normalized = os.path.normpath(path)
                if os.path.exists(normalized):
                    ui_path = normalized
                    break

        if not ui_path or not os.path.exists(ui_path):
            FreeCAD.Console.PrintError(f"ExportPlus: Could not find UI file\n")
            return None

        # Load the UI file
        try:
            from PySide import QtUiTools
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(ui_path)
            ui_file.open(QtCore.QFile.ReadOnly)
            widget = loader.load(ui_file)
            ui_file.close()
            return widget
        except Exception as e:
            FreeCAD.Console.PrintError(f"ExportPlus: Error loading UI: {e}\n")
            return None
