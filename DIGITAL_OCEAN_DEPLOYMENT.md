# Digital Ocean App Platform Deployment Guide

## Database Strategy

### ❌ DO NOT Commit the Database File

The `mgg.db` file is **already in `.gitignore`** and should **NOT** be committed or deployed.

### ✅ Why This is Correct

1. **Database files are already in gitignore** (lines 278, 281, 327)
2. **SQLite is not ideal for production** - Use for development only
3. **Database contains actual data** - Should be managed separately

## Deployment Options

### Option 1: PostgreSQL (Recommended for Production) 🌟

For Digital Ocean, use a **managed PostgreSQL database**:

1. **Create a Database** in Digital Ocean:
   - Go to your project → Create → Databases
   - Choose PostgreSQL
   - Note the connection details

2. **Update `app.py`** to use environment variable:
   ```python
   # Replace this line (line 10):
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/amandaregan/Dropbox/MappingGayGuides/MGG-Site/mgg.db'
   
   # With this:
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
       'DATABASE_URL', 
       'sqlite:///mgg.db'  # Fallback for local dev
   )
   ```

3. **Set environment variable** in Digital Ocean:
   - DATABASE_URL should be set automatically by Digital Ocean
   - If not, add it manually with PostgreSQL connection string

### Option 2: SQLite (Not Recommended but Works)

If you must use SQLite:

1. **The database will be created automatically** on first run
2. **But it will be ephemeral** - data lost on each deploy unless persisted
3. **Better for development only**

## Required Changes to Deploy

### 1. Update `app.py` Database URI

The current `app.py` has a hardcoded absolute path that won't work in production:

```python
# Line 10 - CURRENT (hardcoded path):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/amandaregan/Dropbox/MappingGayGuides/MGG-Site/mgg.db'

# Should be changed to:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///mgg.db'  # This will work on Digital Ocean
)
```

### 2. Environment Variables to Set

In Digital Ocean App Platform settings:

```
FLASK_APP=app.py
SECRET_KEY=<your-secret-key-here>
```

If using PostgreSQL, `DATABASE_URL` is usually set automatically.

### 3. Build Command

```
npm run build-prod
```

### 4. Run Command

```
python app.py
```

## Migration Process

If you have existing data in `mgg.db` that you want to use in production:

1. **Export your data** from local SQLite
2. **Use Flask-Migrate** or custom script to import
3. Or **keep a backup** and run import after deployment

## Recommended File Structure for Deployment

```
Files to Deploy:
✅ app.py
✅ routes/
✅ templates/
✅ static/
✅ content/
✅ requirements.txt
✅ package.json
✅ tailwind.config.js
✅ build commands
✅ init_db.py (or your initialization script)

Files NOT to Deploy:
❌ mgg.db (already in .gitignore)
❌ utilities/ (already in .gitignore)
❌ __pycache__/
❌ node_modules/ (will be built during deployment)
```

## Quick Checklist

- [x] `.db` files are in `.gitignore`
- [x] `utilities/` is in `.gitignore`
- [ ] Update `app.py` to use `os.environ.get('DATABASE_URL')`
- [ ] Choose database strategy (PostgreSQL recommended)
- [ ] Set up environment variables in Digital Ocean
- [ ] Configure build/run commands
- [ ] Deploy and test

## Next Steps

1. Update `app.py` line 10 to use environment variable for database
2. Set up PostgreSQL database in Digital Ocean (recommended)
3. Configure the deployment settings
4. Deploy!

