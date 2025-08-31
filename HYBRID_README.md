# Hybrid Flask/Flask-FlatPages Architecture

This project uses a hybrid approach combining Flask for interactive features and Flask-FlatPages for content pages.

## Architecture Overview

### Content Pages (Flask-FlatPages)
- **Homepage** (`/`) - Generated from `content/markdown/index.md`
- **About** (`/about/`) - Generated from `content/markdown/about.md`
- **Methodology** (`/methodology/`) - Generated from `content/markdown/methodology.md`
- **Articles** (`/articles/`) - Generated from `content/markdown/articles.md`

### Interactive Pages (Flask)
- **Map** (`/map`) - Interactive map visualization
- **Database** (`/database`) - Database browser with search/filter
- **Utility Tools** (`/utility/*`) - Admin and data management tools

## File Structure

```
├── content/
│   └── markdown/          # Source markdown files
│       ├── index.md
│       ├── about.md
│       ├── methodology.md
│       └── articles.md
├── templates/
│   ├── base.html          # Base template
│   ├── page.html          # Template for markdown pages
│   └── ...                # Other Flask templates
├── build.sh               # CSS build script
└── app.py                 # Main Flask application with Flask-FlatPages
```

## Workflow

### Development Workflow

1. **Edit Content**: Modify markdown files in `content/markdown/`
2. **Build CSS**: Run `./build.sh` to build CSS (optional, only if CSS changes)
3. **Test**: Run `python3 app.py` to start the Flask server
4. **View Changes**: Changes to markdown are reflected immediately!

### Adding New Content Pages

1. Create a new markdown file in `content/markdown/`
2. Add frontmatter with metadata:
   ```yaml
   ---
   title: "Page Title"
   subtitle: "Optional subtitle"
   layout: "page-type"
   ---
   ```
3. Access at `/pagename/` - no additional configuration needed!

### Adding New Interactive Pages

1. Create a new Flask route in `routes/main.py`
2. Create a corresponding template in `templates/`
3. No build step needed - Flask handles these dynamically

## Build Process

The build process is now much simpler:

### CSS Build (`npm run build-prod`)
- Compiles Tailwind CSS with DaisyUI
- Applies custom theme colors
- Minifies for production

### Markdown Processing (Flask-FlatPages)
- **Dynamic**: Markdown is processed on-the-fly
- **No build step**: Changes are reflected immediately
- **Template integration**: Uses `templates/page.html`
- **Consistent styling**: All pages use the same base template

## Benefits of This Approach

### For Content Pages
- **Instant Updates**: No build step needed for content changes
- **Easy Editing**: Content creators can work in markdown
- **Version Control**: Markdown files are easy to track in git
- **SEO Friendly**: Proper HTML structure with templates
- **Consistent Styling**: All pages use the same base template

### For Interactive Pages
- **Dynamic Features**: Flask handles complex interactions
- **Database Integration**: Real-time data access
- **User Input**: Forms, search, filtering
- **API Endpoints**: RESTful APIs for data access

## Customization

### Styling
- Modify `tailwind.config.js` for theme changes
- Edit `static/css/input.css` for custom styles
- Update `templates/page.html` for markdown page layout
- Update `templates/base.html` for overall site layout

### Content
- Add new markdown files to `content/markdown/`
- Use standard markdown syntax with extensions:
  - Tables
  - Code highlighting
  - Footnotes
  - Task lists
  - Frontmatter metadata

### Navigation
- Update navigation links in `templates/base.html`
- Ensure consistency between content and interactive pages

## Deployment

### Development
```bash
./build.sh  # Only needed if CSS changes
python3 app.py
```

### Production
```bash
./build.sh
# Deploy Flask app to server
# No static file generation needed!
```

## Dependencies

- **Python**: Flask, Flask-FlatPages, markdown, pyyaml, jinja2
- **Node.js**: tailwindcss, daisyui
- **System**: bash (for build script)

## Troubleshooting

### Common Issues

1. **Markdown not rendering**: Check frontmatter syntax and markdown formatting
2. **CSS not updating**: Run `./build.sh` to rebuild CSS
3. **Links broken**: Ensure navigation uses correct `url_for()` calls
4. **Theme not applying**: Check CSS variables in templates

### Debugging

- Check Flask-FlatPages configuration in `app.py`
- Verify markdown files are in `content/markdown/`
- Test template rendering with `templates/page.html`
- Check Flask routes in `app.py`

## Key Differences from Previous Approach

### Before (Static Generation)
- Required `build_static.py` to convert markdown to HTML
- Generated static HTML files in `content/static/`
- Needed build step for every content change
- No template integration for content pages

### Now (Flask-FlatPages)
- Dynamic markdown processing
- Template integration with `templates/page.html`
- No build step for content changes
- Consistent styling across all pages
- Better error handling and debugging
