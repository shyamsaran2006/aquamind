import os
import re

# Define the path to the pages directory
pages_dir = './pages'

# Define the replacements
replacements = [
    # Replace 'authenticated' check with 'auth_status'
    (r"if 'authenticated' not in st\.session_state or not st\.session_state\.authenticated:", 
     "if 'auth_status' not in st.session_state or not st.session_state['auth_status']:"),
    
    # Replace st.session_state.authenticated with st.session_state['auth_status']
    (r"st\.session_state\.authenticated", 
     "st.session_state['auth_status']"),
    
    # Replace st.session_state.user with st.session_state['auth_user']
    (r"st\.session_state\.user", 
     "st.session_state['auth_user']"),
    
    # Replace dot notation with dictionary notation for user attributes
    (r"st\.session_state\.user\['([^']+)'\]", 
     r"st.session_state['auth_user']['\1']"),
     
    # Replace other session_state dot notation
    (r"st\.session_state\.([a-zA-Z0-9_]+)(?!\[)", 
     r"st.session_state['\1']")
]

# Process each Python file in the pages directory
for filename in os.listdir(pages_dir):
    if filename.endswith('.py'):
        file_path = os.path.join(pages_dir, filename)
        
        # Read the current content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Apply all replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f"Updated {filename}")

print("All files have been updated.")