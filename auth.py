import streamlit as st
import re
import uuid
from datetime import datetime

# Hard-coded demo user for testing
DEMO_USER = {
    "demo@example.com": {
        'uid': "demo123",
        'email': "demo@example.com",
        'password': "password123",
        'name': "Demo User",
        'role': 'user',
        'created_at': datetime.now(),
        'settings': {
            'notifications_enabled': True,
            'theme': 'green'
        }
    }
}

def initialize():
    """Initialize all authentication related session state variables"""
    # Using explicit dictionary keys instead of attributes
    if 'auth_users' not in st.session_state:
        st.session_state['auth_users'] = DEMO_USER.copy()
    
    if 'auth_user' not in st.session_state:
        st.session_state['auth_user'] = None
    
    if 'auth_status' not in st.session_state:
        st.session_state['auth_status'] = False
        
    # Add your credentials as an additional user
    if 'saranshyam2006@gmail.com' not in st.session_state['auth_users']:
        st.session_state['auth_users']['saranshyam2006@gmail.com'] = {
            'uid': "user123",
            'email': "saranshyam2006@gmail.com",
            'password': "Shyni@1602",
            'name': "Saranshyam",
            'role': 'user',
            'created_at': datetime.now(),
            'settings': {
                'notifications_enabled': True,
                'theme': 'green'
            }
        }

def create_user(email, password, name):
    """Create a new user in the session-based user storage."""
    try:
        # Check if user already exists
        if email in st.session_state['auth_users']:
            raise Exception("User with this email already exists")
        
        # Create a new user
        user_id = str(uuid.uuid4())
        
        # Store user data
        st.session_state['auth_users'][email] = {
            'uid': user_id,
            'email': email,
            'password': password,  # Note: In a real app, we would hash this
            'name': name,
            'role': 'user',
            'created_at': datetime.now(),
            'settings': {
                'notifications_enabled': True,
                'theme': 'green'
            }
        }
        
        # Return user data (excluding password)
        return {
            'uid': user_id,
            'email': email,
            'name': name,
            'role': 'user'
        }
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")

def get_user_by_email(email, password):
    """Authenticate a user by email and password."""
    # Initialize session state if needed
    initialize()
    
    try:
        # Check if the user exists
        if email in st.session_state['auth_users']:
            user_data = st.session_state['auth_users'][email]
            
            # Verify password
            if user_data['password'] == password:
                # Return user data (excluding password)
                return {
                    'uid': user_data['uid'],
                    'email': user_data['email'],
                    'name': user_data['name'],
                    'role': user_data['role']
                }
        
        return None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None

def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    # At least 8 characters with at least one number and allowing special characters
    pattern = r'^(?=.*[A-Za-z])(?=.*\d).{8,}$'
    return re.match(pattern, password) is not None

def render_login_signup():
    """Render login/signup form in the sidebar."""
    # Add welcome message with animation
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .welcome-text {
        animation: fadeIn 1s ease-out;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .login-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        border-left: 4px solid #4caf50;
    }
    .form-header {
        color: #2e7d32;
        margin-bottom: 10px;
        font-weight: bold;
        text-align: center;
    }
    .stTabs {
        background-color: white;
        border-radius: 10px;
        padding: 5px;
    }
    </style>
    <div class="welcome-text">Welcome to AQUAMIND</div>
    """, unsafe_allow_html=True)
    
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    
    with login_tab:
        st.markdown('<div class="form-header">Sign In</div>', unsafe_allow_html=True)
        
        email = st.text_input("Email", key="login_email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        # Hint for demo account
        st.caption("Demo account: demo@example.com / password123")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        
        if st.button("Login", key="login_button", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Logging in..."):
                    # Initialize session state before trying to log in
                    initialize()
                    user = get_user_by_email(email, password)
                    if user:
                        st.session_state['auth_user'] = user
                        st.session_state['auth_status'] = True
                        st.balloons()  # Add fun animation on successful login
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                        
    with signup_tab:
        st.markdown('<div class="form-header">Create Account</div>', unsafe_allow_html=True)
        
        name = st.text_input("Full Name", key="signup_name", placeholder="Enter your full name")
        email = st.text_input("Email", key="signup_email", placeholder="Enter your email address")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", key="signup_password", placeholder="Create password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password", placeholder="Confirm password")
        
        st.caption("Password must be at least 8 characters with at least one number. Special characters are allowed.")
        
        terms = st.checkbox("I agree to the Terms and Conditions")
        
        if st.button("Create Account", key="signup_button", use_container_width=True):
            if not name or not email or not password or not confirm_password:
                st.error("Please fill in all fields")
            elif not validate_email(email):
                st.error("Please enter a valid email address")
            elif not validate_password(password):
                st.error("Password must be at least 8 characters and include at least one number. Special characters are allowed.")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not terms:
                st.error("You must agree to the Terms and Conditions")
            else:
                with st.spinner("Creating account..."):
                    try:
                        # Initialize session state before creating user
                        initialize()
                        user = create_user(email, password, name)
                        st.session_state['auth_user'] = user
                        st.session_state['auth_status'] = True
                        st.balloons()  # Add fun animation on successful signup
                        st.success("Account created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")

def logout():
    """Log out the current user."""
    initialize()  # Make sure session state is initialized
    st.session_state['auth_user'] = None
    st.session_state['auth_status'] = False
