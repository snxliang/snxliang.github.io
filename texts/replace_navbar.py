#!/usr/bin/env python3
"""
Script to replace old navbar HTML with new navbar structure
Handles varying whitespace and indentation
"""

import re
import os
import sys
from pathlib import Path

def process_file(file_path, dry_run=True):
    """
    Process a file to make all navbar-related replacements
    
    Args:
        file_path: Path to the HTML file
        dry_run: If True, only show what would be changed without modifying files
    
    Returns:
        bool: True if any replacement was made, False otherwise
    """
    
    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    changes_made = []
    
    # 1. Replace old navbar HTML structure
    old_navbar_pattern = re.compile(
        r'<ul\s+class="navbar">\s*'
        r'<li\s+class="navbarel">\s*<a\s+style="text-decoration:\s*none;\s*color:\s*inherit;"\s+href="\.\./index\.html">home</a>\s*</li>\s*'
        r'<li\s+class="navbarel">\s*<a\s+style="text-decoration:\s*none;\s*color:\s*inherit;"\s+href="\.\./fiction\.html">fiction</a>\s*</li>\s*'
        r'<li\s+class="navbarel">\s*<a\s+style="text-decoration:\s*none;\s*color:\s*inherit;"\s+href="\.\./nfiction\.html">non-fiction</a>\s*</li>\s*'
        r'<li\s+class="navbarel">\s*<a\s+style="text-decoration:\s*none;\s*color:\s*inherit;"\s+href="\.\./photo\.html">photo</a>\s*</li>\s*'
        r'<li\s+class="navbarel">\s*<a\s+style="text-decoration:\s*none;\s*color:\s*inherit;"\s+href="\.\./about\.html">about</a>\s*</li>\s*'
        r'</ul>',
        re.IGNORECASE | re.DOTALL
    )
    
    navbar_match = old_navbar_pattern.search(content)
    if navbar_match:
        # Get the indentation of the original navbar
        lines_before = content[:navbar_match.start()].split('\n')
        last_line = lines_before[-1] if lines_before else ""
        indentation = re.match(r'^(\s*)', last_line).group(1) if last_line else ""
        
        # New replacement HTML
        new_navbar = '''<!--Navigation bar-->
<div id="navbar"></div>
<script src="../navbar.js"></script>
<script>
$(document).ready(function(){
    loadNavbar('projects')
});
</script>
<!--end of Navigation bar-->'''
        
        # Apply indentation to each line of the new navbar
        indented_new_navbar = '\n'.join(
            indentation + line if line.strip() else line 
            for line in new_navbar.split('\n')
        )
        
        content = old_navbar_pattern.sub(indented_new_navbar, content)
        changes_made.append(("Navbar HTML structure", navbar_match.group(), indented_new_navbar))
    
    # 2. Replace existing navbar.js references with ../navbar.js
    navbar_js_pattern = re.compile(r'<script\s+src="navbar\.js">', re.IGNORECASE)
    navbar_js_matches = list(navbar_js_pattern.finditer(content))
    if navbar_js_matches:
        content = navbar_js_pattern.sub('<script src="../navbar.js">', content)
        changes_made.append(("navbar.js path", 'src="navbar.js"', 'src="../navbar.js"'))
    
    # 3. Add jQuery script before </head> if it doesn't already exist
    jquery_pattern = re.compile(r'jquery', re.IGNORECASE)
    head_pattern = re.compile(r'(\s*)</head>', re.IGNORECASE)
    
    if not jquery_pattern.search(content):
        head_match = head_pattern.search(content)
        if head_match:
            indentation = head_match.group(1)  # Get the indentation before </head>
            jquery_script = f'{indentation}<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n{indentation}</head>'
            content = head_pattern.sub(jquery_script, content)
            changes_made.append(("jQuery script", "before </head>", "Added jQuery CDN"))
    
    # Show results or apply changes
    if not changes_made:
        return False
    
    if dry_run:
        print(f"\n{'='*60}")
        print(f"File: {file_path}")
        print(f"{'='*60}")
        for i, (change_type, old_text, new_text) in enumerate(changes_made, 1):
            print(f"\n{i}. {change_type}:")
            print("-" * 40)
            if change_type == "Navbar HTML structure":
                print("OLD:")
                print(old_text)
                print("\nNEW:")
                print(new_text)
            else:
                print(f"OLD: {old_text}")
                print(f"NEW: {new_text}")
            print("-" * 40)
        return True
    else:
        # Apply changes
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            change_summary = ", ".join([change[0] for change in changes_made])
            print(f"✓ Successfully updated: {file_path} ({change_summary})")
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
    for file_path in html_files:
        if process_file(file_path, dry_run):
            files_modified += 1
    
    print(f"\n{'='*50}")
    if dry_run:
        print(f"DRY RUN COMPLETE: {files_modified} files would be modified")
        if files_modified > 0:
            print("Run with --apply flag to make actual changes")
    else:
        print(f"COMPLETE: {files_modified} files were modified")

if __name__ == "__main__":
    main()
