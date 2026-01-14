#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
"""
Example script demonstrating ExportPlus workbench usage

This script can be run from the FreeCAD Python console or as a macro
to demonstrate the scaling export functionality.
"""

import FreeCAD
import Part
import os
import tempfile


def example_create_test_object():
    """Create a simple test object - a 100mm cube"""
    print("Creating test object: 100mm x 100mm x 100mm cube")

    # Create a new document if needed
    if FreeCAD.ActiveDocument is None:
        doc = FreeCAD.newDocument("ExportPlusTest")
    else:
        doc = FreeCAD.ActiveDocument

    # Create a 100mm cube
    box = doc.addObject("Part::Box", "TestCube")
    box.Length = 100.0  # mm
    box.Width = 100.0   # mm
    box.Height = 100.0  # mm

    doc.recompute()
    print(f"Created {box.Label}: {box.Length}mm x {box.Width}mm x {box.Height}mm")

    return box


def example_set_scaling_preferences():
    """Set some example scaling preferences"""
    print("\nConfiguring scaling preferences...")

    param_grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/ExportPlus")

    # Set global scaling to inches (1mm = 0.0393701 inches)
    param_grp.SetFloat("GlobalScalingFactor", 0.0393701)
    print("  Global scaling factor: 0.0393701 (mm to inches)")

    # Set STEP-specific scaling to meters (just as example)
    param_grp.SetFloat("STEPScalingFactor", 0.001)
    print("  STEP-specific scaling: 0.001 (mm to meters)")

    print("Preferences configured!")


def example_export_with_scaling():
    """Demonstrate exporting with scaling"""
    print("\n" + "=" * 60)
    print("ExportPlus Workbench - Example Usage")
    print("=" * 60)

    # Step 1: Create test object
    test_object = example_create_test_object()

    # Step 2: Set preferences
    example_set_scaling_preferences()

    # Step 3: Demonstrate manual scaling
    print("\nDemonstrating scaling functionality...")

    # Get scaling factor
    param_grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/ExportPlus")
    scale_factor = param_grp.GetFloat("GlobalScalingFactor", 1.0)

    print(f"\nOriginal object size: {test_object.Shape.BoundBox.XLength}mm")

    # Create scaled copy
    scaled_shape = test_object.Shape.copy()
    scaled_shape.scale(scale_factor)

    print(f"Scaled object size: {scaled_shape.BoundBox.XLength:.6f}mm")
    print(f"Scaling factor applied: {scale_factor}")
    print(f"Expected size in inches: {100 * scale_factor:.6f} inches (~3.937 inches)")

    # Step 4: Show how to export
    print("\n" + "-" * 60)
    print("To export with scaling using the workbench:")
    print("-" * 60)
    print("1. Select your object in the 3D view")
    print("2. Switch to 'Export Plus' workbench")
    print("3. Click the appropriate export button:")
    print("   - Export STEP (with scaling)")
    print("   - Export STL (with scaling)")
    print("   - Export OBJ (with scaling)")
    print("   - etc.")
    print("4. Choose filename and save")
    print("5. The file will be exported with scaling applied!")

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


def example_show_all_settings():
    """Display all current ExportPlus settings"""
    print("\nCurrent ExportPlus Settings:")
    print("-" * 60)

    param_grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/ExportPlus")

    settings = {
        "GlobalScalingFactor": "Global",
        "STEPScalingFactor": "STEP",
        "STLScalingFactor": "STL",
        "OBJScalingFactor": "OBJ",
        "DXFScalingFactor": "DXF",
        "SVGScalingFactor": "SVG",
    }

    for param_name, label in settings.items():
        value = param_grp.GetFloat(param_name, 0.0)
        if value == 0.0 and param_name != "GlobalScalingFactor":
            print(f"  {label:10s}: {value} (using global)")
        else:
            print(f"  {label:10s}: {value}")


def example_reset_settings():
    """Reset all settings to defaults"""
    print("\nResetting all ExportPlus settings to defaults...")

    param_grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/ExportPlus")

    param_grp.SetFloat("GlobalScalingFactor", 1.0)
    param_grp.SetFloat("STEPScalingFactor", 0.0)
    param_grp.SetFloat("STLScalingFactor", 0.0)
    param_grp.SetFloat("OBJScalingFactor", 0.0)
    param_grp.SetFloat("DXFScalingFactor", 0.0)
    param_grp.SetFloat("SVGScalingFactor", 0.0)

    print("Settings reset!")


def example_common_conversions():
    """Show common unit conversion factors"""
    print("\n" + "=" * 60)
    print("Common Unit Conversions (from mm)")
    print("=" * 60)

    conversions = [
        ("Millimeters (mm)", 1.0),
        ("Centimeters (cm)", 0.1),
        ("Meters (m)", 0.001),
        ("Inches (in)", 0.0393701),
        ("Feet (ft)", 0.00328084),
        ("Micrometers (μm)", 1000.0),
    ]

    print("\n{:20s} {:>15s} {:>20s}".format("Unit", "Factor", "100mm becomes"))
    print("-" * 60)

    for unit_name, factor in conversions:
        result = 100.0 * factor
        print(f"{unit_name:20s} {factor:>15.6f} {result:>15.6f} {unit_name.split('(')[1][:-1]}")


# Main execution
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# ExportPlus Workbench - Example Script")
    print("#" * 60)

    # Run the main example
    example_export_with_scaling()

    # Show conversion table
    example_common_conversions()

    # Show current settings
    example_show_all_settings()

    print("\n" + "#" * 60)
    print("# Additional Functions Available:")
    print("#" * 60)
    print("# - example_create_test_object()      : Create a test cube")
    print("# - example_set_scaling_preferences() : Configure scaling")
    print("# - example_show_all_settings()       : Display current settings")
    print("# - example_reset_settings()          : Reset to defaults")
    print("# - example_common_conversions()      : Show conversion factors")
    print("#" * 60)
    print("\nYou can run these functions individually from the Python console!")
