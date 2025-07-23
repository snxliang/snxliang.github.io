#!/usr/bin/env python3
"""
Script to replace loadNavbar parameter in HTML files within a specific directory
"""

import re
import os
import sys
from pathlib import Path

def replace_navbar_parameter(file_path, old_param, new_param, dry_run=True):
    """
    Replace parameter in loadNavbar calls
    
    Args:
        file_path: Path to the HTML file
        old_param: Parameter to replace (e.g., 'projects')
        new_param: New parameter (e.g., 'fiction')
        dry_run: If True, only show what would be changed
    
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
    
    # Pattern to match loadNavbar calls with the specific parameter
    # Matches: loadNavbar('old_param') or loadNavbar('old_param', 'basePath')
    pattern = re.compile(
        f"loadNavbar\\(\\s*['\"]({re.escape(old_param)})['\"]",
        re.IGNORECASE
    )
    
    matches = list(pattern.finditer(content))
    if not matches:
        return False
    
    # Replace the parameter
    new_content = pattern.sub(f"loadNavbar('{new_param}'", content)
    
    if dry_run:
        print(f"\n{'='*50}")
        print(f"File: {file_path}")
        print(f"{'='*50}")
        print(f"Found {len(matches)} occurrence(s) of loadNavbar('{old_param}'...)")
        print(f"Would replace '{old_param}' → '{new_param}'")
        
        # Show each match in context
        for i, match in enumerate(matches, 1):
            start = max(0, match.start() - 30)
            end = min(len(content), match.end() + 30)
            context = content[start:end].replace('\n', '\\n').replace('\t', '\\t')
            print(f"  {i}. ...{context}...")
        
        return True
    else:
        # Apply changes
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Replaced {len(matches)} occurrence(s) in: {file_path}")
            return True
        except Exception as e:
            print(f"✗ Error writing to {file_path}: {e}")
            return False

def main():
    """Main function"""
    
    # Configuration - CHANGE THESE VALUES
    target_directory = "texts"  # Directory to search in
    old_parameter = "projects"  # Parameter to replace
    new_parameter = "fiction"   # New parameter value
    file_extensions = ['.html', '.htm']
    
    # Parse command line arguments for custom values
    if len(sys.argv) >= 4:
        target_directory = sys.argv[1]
        old_parameter = sys.argv[2] 
        new_parameter = sys.argv[3]
        dry_run = "--apply" not in sys.argv
    else:
        # Parse dry run flag
        dry_run = True
        if len(sys.argv) > 1 and sys.argv[1] == "--apply":
            dry_run = False
    
    if dry_run:
        print("DRY RUN MODE - No files will be modified")
        print("Use --apply flag to actually make changes")
    else:
        print("APPLYING CHANGES MODE - Files will be modified!")
    
    print(f"Target directory: {target_directory}")
    print(f"Replacing: '{old_parameter}' → '{new_parameter}'")
    print(f"File types: {', '.join(file_extensions)}")
    
    # Check if target directory exists
    target_path = Path(target_directory)
    if not target_path.exists():
        print(f"Error: Directory '{target_directory}' does not exist!")
        return
    if not target_path.is_dir():
        print(f"Error: '{target_directory}' is not a directory!")
        return
    
    # Find HTML files in the target directory (not recursive by default)
    html_files = []
    for ext in file_extensions:
        # Use glob instead of rglob to only search in the target directory
        html_files.extend(target_path.glob(f"*{ext}"))
    
    if not html_files:
        print(f"No HTML files found in '{target_directory}'!")
        return
    
    print(f"Found {len(html_files)} HTML files to check")
    
    # Process each file
    files_modified = 0
    for file_path in sorted(html_files):
        if replace_navbar_parameter(file_path, old_parameter, new_parameter, dry_run):
            files_modified += 1
    
    print(f"\n{'='*50}")
    if dry_run:
        print(f"DRY RUN COMPLETE: {files_modified} files would be modified")
        if files_modified > 0:
            print("Run with --apply flag to make actual changes")
    else:
        print(f"COMPLETE: {files_modified} files were modified")

if __name__ == "__main__":
    print("Usage examples:")
    print("  python3 script.py                           # Dry run with default settings")
    print("  python3 script.py --apply                   # Apply with default settings")
    print("  python3 script.py texts projects fiction   # Custom directory and parameters")
    print("  python3 script.py texts projects fiction --apply  # Custom + apply")
    print()
    main()
