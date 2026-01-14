# ExportPlus Usage Guide

## Three Ways to Use ExportPlus

### Option 1: From the Export Plus Workbench (Default)

1. **Switch to Export Plus workbench** from the workbench dropdown
2. **Use the toolbar** with labeled buttons: `STEP`, `STL`, `OBJ`, `SVG`, `DXF`, `PDF`
3. **Or use the menu**: `Export Plus` → choose format
4. The toolbar buttons show the format name directly for easy identification

**Advantages:**
- Quick access via toolbar
- Clear visual indication of available formats
- All export options in one place

### Option 2: From the File Menu (Integrated)

When you activate the Export Plus workbench, it also adds items to:
- **File → Export with Scaling** submenu

This gives you access to scaling exports from the standard File menu.

**Advantages:**
- Familiar workflow (File menu)
- Works alongside standard export
- Available when Export Plus workbench is active

### Option 3: Global Integration (Advanced)

To make ExportPlus available in ALL workbenches without switching:

1. Open `H:\code\FreeCAD\src\Mod\ExportPlus\Init.py`
2. **Uncomment** lines 34-40 (remove the `#` at the start of each line)
3. Restart FreeCAD

This adds "Export with Scaling" to the File menu permanently, available in all workbenches.

**Advantages:**
- Always available, no need to switch workbenches
- Integrates seamlessly with FreeCAD
- Becomes your default export method

## Button Labels

All toolbar buttons now display the format name directly:
- **STEP** - for CAD interchange
- **STL** - for 3D printing
- **OBJ** - for 3D graphics
- **SVG** - for 2D vector graphics
- **DXF** - for 2D CAD
- **PDF** - for documentation

The format name appears as text on the button, making it easy to identify at a glance.

## Quick Start

### Export a model in inches (instead of mm):

1. Create your model (FreeCAD uses mm internally)
2. Switch to Export Plus workbench
3. Open **Edit → Preferences → Import-Export → Export Plus Settings**
4. Click the **"Inches (0.0393701)"** preset button
5. Click **OK**
6. Select your object
7. Click the **STEP** button (or any format)
8. Choose filename and save

Your model is now exported in inches!

## Scaling Presets

The preferences page includes quick preset buttons:

| Button | Factor | Description |
|--------|--------|-------------|
| **mm (1.0)** | 1.0 | Millimeters (FreeCAD default) |
| **Inches (0.0393701)** | 0.0393701 | Convert mm to inches |
| **cm (0.1)** | 0.1 | Convert mm to centimeters |
| **Meters (0.001)** | 0.001 | Convert mm to meters |

Click any button to instantly set the global scaling factor.

## Advanced: Per-Format Scaling

You can override the global setting for specific formats:

1. Go to **Edit → Preferences → Import-Export → Export Plus Settings**
2. Set a **Global scaling factor** (e.g., 1.0 for mm)
3. Under a specific format (e.g., "STEP Format"), set a different value
4. Set to `0` to use the global setting

**Example:**
- Global: `1.0` (millimeters)
- STEP: `0.0393701` (inches)
- STL: `0` (use global = mm)

Now STEP exports in inches, but STL exports in mm!

## Workflow Examples

### Example 1: Mechanical Part for Machinist (Imperial)

```
1. Design part in FreeCAD (uses mm)
2. Switch to Export Plus workbench
3. Preferences → Click "Inches" button
4. Select part → Click "STEP" button
5. Machinist receives STEP file in inches
```

### Example 2: 3D Printing (Metric)

```
1. Design model in FreeCAD
2. Switch to Export Plus workbench
3. Preferences → Click "mm" button (or leave at default 1.0)
4. Select model → Click "STL" button
5. Slicer receives STL in mm (standard for 3D printing)
```

### Example 3: Mixed Export (Architectural)

```
1. Design building in FreeCAD
2. Preferences → Set:
   - Global: 0.001 (meters)
   - DXF: 0.1 (centimeters for floor plans)
   - STEP: 0 (use global = meters)
3. Export STEP for structural engineering (meters)
4. Export DXF for floor plans (centimeters)
```

## Checking Current Scaling

The current scaling factor is shown in:
1. **Console output** when you export: `"Exporting STEP with scaling factor: 0.0393701"`
2. **Preferences dialog**: Edit → Preferences → Import-Export → Export Plus Settings

## Tips

- **Test first**: Export a simple 100mm cube and measure it in your target application
- **Save presets**: Note your commonly used scaling factors
- **Global vs. Format**: Use global for consistency, per-format for special cases
- **Remember**: FreeCAD always works in mm internally; scaling only affects export

## Troubleshooting

**Q: Buttons do nothing**
- Make sure to activate the Export Plus workbench first
- Try clicking the preset buttons, then reopen preferences to see if they connected

**Q: Wrong scale after export**
- Check console message for actual scaling factor used
- Verify preferences are saved (click OK, not Cancel)
- Remember: 0 in format-specific settings means "use global"

**Q: Can't find Export Plus workbench**
- Check workbench dropdown at top
- Look for "Export Plus" entry
- Verify installation (see INSTALL.md)

**Q: Want it in File menu always**
- Edit Init.py and uncomment lines 34-40
- Restart FreeCAD
- "Export with Scaling" appears in File menu

## Keyboard Shortcuts

- **Ctrl+Shift+E**: Export STEP (when Export Plus is active)

Additional shortcuts can be configured in:
**Tools → Customize → Keyboard**

## Next Steps

- Read [README.md](README.md) for full documentation
- See [INSTALL.md](INSTALL.md) for installation details
- Check preferences for all available options
- Experiment with different scaling factors for your workflow

Happy exporting! 🚀
