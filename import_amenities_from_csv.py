#!/usr/bin/env python3
"""
Import amenity data from amenities_export.csv
Updates descriptive_name, description, and short_description fields
"""
import csv
import os
from app import app
from models import db, AmenityFeature

def import_amenities_from_csv(csv_path='amenities_export.csv'):
    """Import amenity data from CSV file"""
    with app.app_context():
        print("=" * 60)
        print("Importing Amenity Data from CSV")
        print("=" * 60)
        print()
        
        # Check if CSV file exists
        if not os.path.exists(csv_path):
            print(f"✗ CSV file not found: {csv_path}")
            return False
        
        # Read CSV file
        print(f"Reading CSV file: {csv_path}")
        updated_count = 0
        not_found_count = 0
        skipped_count = 0
        
        # Try different encodings - prioritize cp1252 (Windows) as it's most common for Excel exports
        encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
        file_handle = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                file_handle = open(csv_path, 'r', encoding=encoding)
                # Test read first line
                file_handle.readline()
                file_handle.seek(0)  # Reset to beginning
                used_encoding = encoding
                print(f"Using encoding: {encoding}")
                break
            except (UnicodeDecodeError, UnicodeError):
                if file_handle:
                    file_handle.close()
                continue
        
        if not file_handle:
            print("✗ Could not read CSV file with any supported encoding")
            return False
        
        def fix_encoding_issues(text):
            """Fix common encoding issues from Windows-1252/CP1252 files
            
            When a file is saved as Windows-1252 (CP1252) but read as latin-1,
            certain characters get misinterpreted. This function fixes those.
            """
            if not text:
                return text
            
            # If we read as latin-1 but the file is actually CP1252, these mappings fix it
            # Common CP1252 characters that get misread as latin-1:
            result = text
            
            # Fix apostrophes and quotes (most common issue)
            # 0xD5 in CP1252 context might appear as Õ when misread
            # But more commonly, 0x92 (right single quotation mark in CP1252) appears as a control char
            # Let's fix the actual byte-level issues by re-encoding and decoding properly
            try:
                # If text contains characters that suggest CP1252 misread as latin-1,
                # try to fix them by encoding as latin-1 and decoding as cp1252
                if any(ord(c) > 127 for c in text):
                    # Try to fix by re-encoding/re-decoding
                    fixed_bytes = text.encode('latin-1')
                    fixed_text = fixed_bytes.decode('cp1252', errors='replace')
                    result = fixed_text
            except (UnicodeEncodeError, UnicodeDecodeError):
                # If that doesn't work, do manual replacements
                pass
            
            # Manual fixes for common issues
            fixes = {
                'Õ': "'",  # Common apostrophe issue (0xD5 when misread)
                'â€™': "'",  # UTF-8 smart apostrophe misread
                'â€œ': '"',  # Left double quote
                'â€': '"',  # Right double quote  
                'â€"': '—',  # Em dash
                'â€"': '–',  # En dash
                'â€¦': '…',  # Ellipsis
            }
            
            for wrong, correct in fixes.items():
                result = result.replace(wrong, correct)
            
            return result
        
        with file_handle:
            reader = csv.DictReader(file_handle)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                name = row.get('name', '').strip()
                
                if not name:
                    print(f"  Row {row_num}: Skipping row with no name")
                    skipped_count += 1
                    continue
                
                # Get the amenity from database
                amenity = AmenityFeature.query.filter_by(name=name).first()
                
                if not amenity:
                    print(f"  Row {row_num}: ✗ Amenity not found: {name}")
                    not_found_count += 1
                    continue
                
                # Track if we're updating anything
                updated = False
                
                # Get raw values from CSV and fix encoding issues
                raw_descriptive_name = row.get('descriptive_name', '').strip()
                raw_description = row.get('description', '').strip()
                raw_short_description = row.get('short_description', '').strip()
                
                # Fix encoding issues
                descriptive_name = fix_encoding_issues(raw_descriptive_name) if raw_descriptive_name else None
                description = fix_encoding_issues(raw_description) if raw_description else None
                short_description = fix_encoding_issues(raw_short_description) if raw_short_description else None
                
                # Also fix existing database values that might have encoding issues
                # Check if current values have encoding issues and fix them
                if amenity.descriptive_name and 'Õ' in amenity.descriptive_name:
                    amenity.descriptive_name = fix_encoding_issues(amenity.descriptive_name)
                    updated = True
                if amenity.description and 'Õ' in amenity.description:
                    amenity.description = fix_encoding_issues(amenity.description)
                    updated = True
                if amenity.short_description and 'Õ' in amenity.short_description:
                    amenity.short_description = fix_encoding_issues(amenity.short_description)
                    updated = True
                
                # Update from CSV if provided
                if descriptive_name and descriptive_name != amenity.descriptive_name:
                    amenity.descriptive_name = descriptive_name
                    updated = True
                
                if description and description != amenity.description:
                    amenity.description = description
                    updated = True
                
                if short_description and short_description != amenity.short_description:
                    amenity.short_description = short_description
                    updated = True
                
                if updated:
                    updated_count += 1
                    print(f"  Row {row_num}: ✓ Updated {name}")
                    if descriptive_name:
                        print(f"      Descriptive Name: {descriptive_name}")
                    if description:
                        print(f"      Description: {description[:80]}..." if len(description) > 80 else f"      Description: {description}")
                    if short_description:
                        print(f"      Short Description: {short_description}")
                else:
                    # Check if row has any data
                    has_data = any([
                        row.get('descriptive_name', '').strip(),
                        row.get('description', '').strip(),
                        row.get('short_description', '').strip()
                    ])
                    if not has_data:
                        # Row is empty, skip silently
                        pass
                    else:
                        print(f"  Row {row_num}: - No changes needed for {name}")
        
        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print()
            print("-" * 60)
            print(f"✓ Successfully updated {updated_count} amenity/amenities!")
            if not_found_count > 0:
                print(f"⚠ {not_found_count} amenity/amenities not found in database")
            if skipped_count > 0:
                print(f"⚠ {skipped_count} row(s) skipped")
        else:
            print()
            print("-" * 60)
            print("ℹ No amenities were updated.")
            if not_found_count > 0:
                print(f"⚠ {not_found_count} amenity/amenities not found in database")
        
        print()
        print("=" * 60)
        print("Import complete!")
        print("=" * 60)
        
        return True

if __name__ == '__main__':
    import_amenities_from_csv()
