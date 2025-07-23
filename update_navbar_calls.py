#!/usr/bin/env python3
"""
Script to update loadNavbar() calls with appropriate basePath parameter
based on file directory depth
"""

import re
import os
import sys
from pathlib import Path

def update_navbar_calls(file_path, dry_run=True):
    """
    Update loadNavbar calls in HTML files to include correct basePath
    
    Args:
        file_path: Path to the HTML file
        dry_run: If True, only show what would be changed without modifying files
    
    Returns:
        bool: True if replacement was made, False otherwise
    """
    
    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    # Calculate directory depth relative to the search directory
    search_dir = Path(".")  # You can change this if needed
    file_relative_path = Path(file_path).relative_to(search_dir)
    depth = len(file_relative_path.parts) - 1  # Subtract 1 for the filename
    
    # Create the appropriate basePath
    if depth == 0:
        # Root level - no basePath needed
        base_path = ""
        base_path_param = ""
    else:
        # Subdirectory - need ../
        base_path = "../" * depth
        base_path_param = f", '{base_path}'"
    
    # Pattern to match existing loadNavbar calls
    # This matches: loadNavbar('anything') or loadNavbar('anything', 'anything')
    navbar_pattern = re.compile(
        r"loadNavbar\(\s*['\"]([^'\"]*)['\"](?:\s*,\s*['\"][^'\"]*['\"])?\s*\)",
        re.IGNORECASE
    )
    
    matches = list(navbar_pattern.finditer(content))
    if not matches:
        return False
    
    changes_made = []
    new_content = content
    
    # Process matches in reverse order to maintain string positions
    for match in reversed(matches):
        old_call = match.group(0)
        active_page = match.group(1)  # Extract the first parameter (activePage)
        
        # Create the new call
        new_call = f"loadNavbar('{active_page}'{base_path_param})"
        
        # Replace in content
        new_content = new_content[:match.start()] + new_call + new_content[match.end():]
        changes_made.append((old_call, new_call))
    
    if dry_run:
        print(f"\n{'='*60}")
        print(f"File: {file_path}")
        print(f"Directory depth: {depth}")
        print(f"Base path: '{base_path}' (empty = root level)")
        print(f"{'='*60}")
        
        for i, (old_call, new_call) in enumerate(changes_made, 1):
            print(f"\n{i}. loadNavbar call update:")
            print(f"   OLD: {old_call}")
            print(f"   NEW: {new_call}")
        
        return True
    else:
        # Apply changes
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Updated {len(changes_made)} loadNavbar call(s) in: {file_path}")
            return True
        except Exception as e:
            print(f"✗ Error writing to {file_path}: {e}")
            return False

def main():
    """Main function to process files"""
    
    # Configuration
    search_directory = "."  # Current directory, change as needed
    file_extensions = ['.html', '.htm']  # File types to search
    
    # Parse command line arguments
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        dry_run = False
        print("APPLYING CHANGES MODE - Files will be modified!")
    else:
        print("DRY RUN MODE - No files will be modified")
        print("Use --apply flag to actually make changes")
    
    print(f"Searching in: {os.path.abspath(search_directory)}")
    print(f"File types: {', '.join(file_extensions)}")
    
    # Find all HTML files
    html_files = []
    for ext in file_extensions:
        html_files.extend(Path(search_directory).rglob(f"*{ext}"))
    
    if not html_files:
        print("No HTML files found!")
        return
    
    print(f"Found {len(html_files)} HTML files to check")
    
    # Process each file
    files_modified = 0
    for file_path in sorted(html_files):  # Sort for consistent output
        if update_navbar_calls(file_path, dry_run):
            files_modified += 1
    
    print(f"\n{'='*60}")
    if dry_run:
        print(f"DRY RUN COMPLETE: {files_modified} files would be modified")
        if files_modified > 0:
            print("Run with --apply flag to make actual changes")
    else:
        print(f"COMPLETE: {files_modified} files were modified")
    
    if files_modified > 0:
        print("\nDirectory structure detected:")
        for file_path in sorted(html_files):
            file_relative_path = Path(file_path).relative_to(Path("."))
            depth = len(file_relative_path.parts) - 1
            base_path = "../" * depth if depth > 0 else "(root)"
            print(f"  {file_relative_path} → basePath: '{base_path}'")

if __name__ == "__main__":
    main()
