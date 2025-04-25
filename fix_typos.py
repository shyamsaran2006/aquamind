import glob
import re

# The list of files to process
files = glob.glob('./pages/*.py')

# Patterns to fix
replacements = [
    (r"strawberry_dat\]a", "strawberry_data"),
    (r"date_rang\]e", "date_range")
]

# Process each file
for file_path in files:
    print(f"Processing: {file_path}")
    
    # Read the content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Apply the replacements
    modified = False
    for pattern, replacement in replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    # Write back only if modified
    if modified:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"  - Fixed typos in {file_path}")
    else:
        print(f"  - No issues found in {file_path}")

print("Done.")