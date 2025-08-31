#!/bin/bash

echo "Building CSS..."
npm run build-prod

echo "Build complete!"
echo "You can now run: python3 app.py"
echo "Note: Markdown content is now processed dynamically by Flask-FlatPages"
