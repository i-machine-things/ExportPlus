# ExportPlus Workbench - Installation Guide

## Quick Start

The ExportPlus workbench has been created in your FreeCAD source tree at:
```
H:\code\FreeCAD\src\Mod\ExportPlus\
```

## Installation Options

### Option 1: Build with FreeCAD (Recommended for Development)

If you're building FreeCAD from source, the workbench is already in place and should be available after building.

**Steps:**
1. Configure your build (if not already done):
   ```bash
   cd H:\code\FreeCAD
   cmake -B build -S .
   ```

2. Build FreeCAD:
   ```bash
   cmake --build build
   ```

3. Run FreeCAD from your build directory

4. The ExportPlus workbench should appear in the workbench dropdown

### Option 2: Copy to User Mod Directory (For Testing)

To test the workbench without rebuilding FreeCAD:

**Windows:**
```cmd
xcopy /E /I "H:\code\FreeCAD\src\Mod\ExportPlus" "%APPDATA%\FreeCAD\Mod\ExportPlus"
```

**Linux/macOS:**
```bash
cp -r "H:/code/FreeCAD/src/Mod/ExportPlus" ~/.FreeCAD/Mod/ExportPlus
```

Then restart FreeCAD.

## Verification

After installation, verify the workbench is available:

1. **Launch FreeCAD**
2. **Check the workbench dropdown** - You should see "Export Plus" in the list
3. **Open Preferences** (Edit → Preferences)
4. **Navigate to Import-Export** - You should see "Export Plus Settings" as a page

## Testing the Workbench

### Quick Test

1. **Create a test object:**
   - Open FreeCAD
   - Create a new document (File → New)
   - Create a simple box: Go to Part workbench → Create a cube

2. **Select the object** in the 3D view

3. **Switch to Export Plus workbench**

4. **Configure scaling:**
   - Edit → Preferences → Import-Export → Export Plus Settings
   - Set "Global scaling factor" to `0.0393701` (inches)
   - Click OK

5. **Export:**
   - Click "Export STEP (with scaling)" button
   - Choose a filename and save
   - Check the console for the message: "Exporting STEP with scaling factor: 0.0393701"

6. **Verify:**
   - Re-import the file (File → Import)
   - Measure the imported object - it should be ~39.37 times smaller (mm to inches conversion)

## Files Created

```
ExportPlus/
├── Init.py                                    # Module initialization
├── InitGui.py                                 # Workbench GUI setup
├── exportplus_commands.py                     # Export commands with scaling
├── README.md                                  # Full documentation
├── INSTALL.md                                 # This file
└── Resources/
    ├── icons/
    │   └── ExportPlus.svg                    # Workbench icon (blue document with plus)
    └── ui/
        └── preferences-exportplus.ui          # Preferences page with scaling options
```

## Troubleshooting

### Workbench doesn't appear

**Check 1: File location**
```bash
# The files should be at:
# Windows: %APPDATA%\FreeCAD\Mod\ExportPlus\
# Linux: ~/.FreeCAD/Mod/ExportPlus/
# Or in the FreeCAD source tree for development builds
```

**Check 2: Python errors**
- Open FreeCAD
- Go to View → Panels → Report view
- Look for any error messages related to ExportPlus

**Check 3: Restart FreeCAD**
- Completely close FreeCAD (not just the window, check Task Manager)
- Reopen it

### Import errors

If you see errors like "No module named exportplus_commands":

1. Make sure all files are in the correct location
2. Check that `Init.py` and `InitGui.py` are in the ExportPlus root directory
3. Verify `exportplus_commands.py` is also in the root directory

### Preferences page doesn't appear

If the preferences page is missing:

1. Check that `preferences-exportplus.ui` exists at:
   ```
   ExportPlus/Resources/ui/preferences-exportplus.ui
   ```

2. Verify the path in `InitGui.py` is correct (it should use `os.path.join`)

### Export doesn't scale

If exports work but scaling isn't applied:

1. Check your preference settings:
   - Edit → Preferences → Import-Export → Export Plus Settings
   - Verify the scaling factor is not 1.0 or 0.0

2. Check the console output:
   - It should print: "Exporting [FORMAT] with scaling factor: [value]"

3. Make sure you're using the ExportPlus commands, not the standard File → Export

## Advanced Configuration

### Custom Scaling Presets

The preferences UI includes preset buttons. To add more presets, edit:
```
ExportPlus/Resources/ui/preferences-exportplus.ui
```

Add new button widgets in the "Quick presets" section.

### Additional Export Formats

To add support for more formats:

1. Edit `exportplus_commands.py`
2. Create a new command class (follow the existing pattern)
3. Register it with `FreeCADGui.addCommand()`
4. Add it to the command list in `InitGui.py`
5. Add scaling options to `preferences-exportplus.ui`

## Integration with FreeCAD Build System

If you want to integrate this properly into the FreeCAD build:

1. **Add CMakeLists.txt** (optional for Python-only workbenches):
   ```cmake
   # Not strictly necessary for pure Python workbenches
   # FreeCAD automatically loads modules from src/Mod/
   ```

2. **The workbench will automatically be included** in FreeCAD builds since it's in `src/Mod/`

3. **To make it optional**, you could add a build flag (requires modifying root CMakeLists.txt)

## Uninstallation

To remove the workbench:

**From source tree:**
```bash
rm -rf H:\code\FreeCAD\src\Mod\ExportPlus
```

**From user directory:**

**Windows:**
```cmd
rmdir /S "%APPDATA%\FreeCAD\Mod\ExportPlus"
```

**Linux/macOS:**
```bash
rm -rf ~/.FreeCAD/Mod/ExportPlus
```

Then restart FreeCAD.

## Next Steps

1. **Read the full documentation** in `README.md`
2. **Test all export formats** to ensure they work with your models
3. **Experiment with different scaling factors** for your use cases
4. **Provide feedback** if you find issues or have suggestions

## Support

For questions or issues:
- Check the `README.md` for detailed usage instructions
- Visit the FreeCAD Forum: https://forum.freecad.org/
- Report bugs: https://github.com/FreeCAD/FreeCAD/issues

Happy exporting! 🚀
