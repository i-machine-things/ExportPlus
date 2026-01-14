# ExportPlus Changelog

## Version 1.1.0 (2026-01-13)

### New Features
- **Global Keyboard Shortcuts** - Shortcuts now work in any workbench, not just ExportPlus
  - Ctrl+Shift+E: Quick Export dialog
  - Ctrl+Shift+S: Direct STL export
  - Ctrl+Shift+D: Direct DXF export

- **Quick Export Dialog** - Fast format selection with single shortcut
  - Press Ctrl+Shift+E to open
  - In-dialog shortcuts: S, T, O, D, V, P for each format
  - Esc to cancel

- **File Menu Integration** - Access ExportPlus from File → Export with Scaling
  - Available in all workbenches
  - No need to switch to ExportPlus workbench

### Bug Fixes
- Fixed TypeError in QuickExportDialog lambda functions
  - Lambda functions now properly handle the `checked` parameter from button clicks
  - Added default parameter value to prevent missing argument errors

### Technical Changes
- Moved global initialization from Init.py to InitGui.py
- Created exportplus_init_global.py for global integration
- QShortcut objects registered with ApplicationShortcut context for global availability
- Shortcuts stored in module-level list to prevent garbage collection

### Documentation Updates
- Updated README.md with global shortcuts information
- Updated KEYBOARD_SHORTCUTS.md with new Ctrl+Shift+E shortcut
- Added file structure documentation
- Updated changelog with version history

---

## Version 1.0.0 (2026-01-13)

### Initial Release
- Support for 6 export formats: STEP, STL, OBJ, DXF, SVG, PDF
- Global scaling factor for all exports
- Per-format scaling factor overrides
- Quick preset buttons for common unit conversions:
  - Millimeters (1.0)
  - Inches (0.0393701)
  - Centimeters (0.1)
  - Meters (0.001)
- Preferences UI integration
- Export Plus workbench with toolbar and menu
- Format-specific keyboard shortcuts (workbench-only)
- Context menu integration
