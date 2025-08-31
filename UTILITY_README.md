# Utility App - Mapping Gay Guides

A simple standalone Flask app for development and data management tools, separate from the main public site.

## What This Is

Instead of a complex admin dashboard, this is a lightweight utility app that runs on a different port (5002) and contains just the essential tools you need occasionally.

## How to Use

### 1. Start the Utility App
```bash
python utility_app.py
```

This will start the utility app on **port 5002**.

### 2. Access Utility Tools
- **Utility Index**: http://localhost:5002/
- **Amenity Cleanup**: http://localhost:5002/amenity-cleanup
- **Smart Split**: http://localhost:5002/smart-split
- **Database Browser**: http://localhost:5002/database

### 3. Main Site Remains Clean
- Main site continues running on **port 5001**
- No utility page links in main navigation
- Clean, professional public experience

## File Structure

```
├── utility_app.py                    # Standalone utility Flask app
├── templates/
│   └── utility/                      # Utility templates
│       ├── index.html               # Utility tools index
│       ├── amenity_cleanup.html     # Amenity cleanup tool
│       ├── smart_split.html         # Smart split tool
│       └── database.html            # Database browser
├── templates/                        # Main site templates (unchanged)
│   ├── base.html                    # Clean main navigation
│   ├── index.html
│   ├── map.html
│   └── database.html                # Public database page
└── routes/                          # Main site routes (cleaned up)
    ├── main.py                      # No utility routes
    └── api.py                       # Unchanged
```

## Benefits

1. **Simple & Lightweight**: No complex admin structure
2. **Separate Ports**: Main site (5001) vs. utilities (5002)
3. **Clean Main Site**: No utility links cluttering navigation
4. **Easy Access**: Just run `python utility_app.py` when you need tools
5. **No Dependencies**: Standalone app, doesn't affect main site

## Current Status

- ✅ **Utility app structure**: Complete and functional
- 🔄 **Template migration**: In progress (showing placeholders)
- 📋 **Full functionality**: Ready for content transfer

## Migration Plan

1. **Phase 1**: Utility app structure ✅ (Complete)
2. **Phase 2**: Copy template content from old to new utility templates
3. **Phase 3**: Test all functionality
4. **Phase 4**: Remove old templates (optional)

## Usage Workflow

### For Development/Data Management:
1. Run `python utility_app.py`
2. Open http://localhost:5002/
3. Use the tools you need
4. Close when done

### For Public Site:
1. Main site runs normally on port 5001
2. Clean, focused experience
3. No utility page links

## Notes

- The utility app is completely separate from the main site
- You can run both simultaneously (main site on 5001, utilities on 5002)
- When you don't need the tools, just don't run the utility app
- Perfect for occasional use without cluttering the main site
