import streamlit as st
import os
import pandas as pd
from PIL import Image
import time

# Import custom modules
import auth
import utils
from data_loader import load_strawberry_data

# Page configuration
st.set_page_config(
    page_title="AQUAMIND",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom green and white theme
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .stButton button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 4px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e8f5e9;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4caf50 !important;
        color: white !important;
    }
    .stSidebar .stButton button {
        width: 100%;
    }
    h1, h2, h3 {
        color: #2e7d32;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    div.stMetric {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize authentication session state
auth.initialize()

# Create additional session states if they don't exist
if 'strawberry_data' not in st.session_state:
    # Load the data once and store in session state
    st.session_state['strawberry_data'] = load_strawberry_data()
if 'selected_variety' not in st.session_state:
    st.session_state['selected_variety'] = "All"
if 'date_range' not in st.session_state:
    if st.session_state['strawberry_data'] is not None:
        # Convert pandas datetime to python datetime objects for consistent handling
        min_date = pd.to_datetime(st.session_state['strawberry_data']['Date'].min()).to_pydatetime()
        max_date = pd.to_datetime(st.session_state['strawberry_data']['Date'].max()).to_pydatetime()
        st.session_state['date_range'] = (min_date, max_date)
    else:
        st.session_state['date_range'] = (None, None)

def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
        
        .custom-font {
            font-family: 'Times New Roman', Times, serif !important;
            font-size: 16px !important;
            color: #555 !important;
        }
        
        .section-header {
            font-family: 'Times New Roman', Times, serif !important;
            font-size: 20px !important;
            font-weight: bold !important;
            margin-bottom: 1rem !important;
        }
        
        .about-container {
            background-color: white;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #eee;
            transition: all 0.3s ease;
        }
        
        .icon-container {
            font-size: 24px;
            margin-right: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .about-container {
                padding: 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # About section with custom styling
    with st.expander("ℹ️ About AQUAMIND"):
        st.markdown("""
        <div class="about-container">
            <div class="section-header">
                <i class="fas fa-info-circle icon-container"></i>About
            </div>
            <div class="custom-font">
                AQUAMIND is an intelligent monitoring and management system for strawberry aquaponics, combining real-time data analytics with AI-powered insights. Our platform enables precise control and optimization of growing conditions through advanced sensor technology and machine learning algorithms.
            </div>
            
            <div class="section-header">
                <i class="fas fa-star icon-container"></i>Key Features
            </div>
            <div class="custom-font">
                • <i class="fas fa-chart-line"></i> Real-time monitoring of critical growth parameters
                • <i class="fas fa-robot"></i> AI-powered predictions and trend analysis
                • <i class="fas fa-leaf"></i> Smart nutrient and disease management
                • <i class="fas fa-chart-bar"></i> Comprehensive data visualization
            </div>

            <div class="section-header">
                <i class="fas fa-flask icon-container"></i>Apparatus
            </div>
            <div class="custom-font">
                <table style="width:100%">
                    <tr>
                        <td><i class="fas fa-vial"></i> pH Sensor</td>
                        <td>Monitors water acidity/alkalinity</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-tint"></i> EC Sensor</td>
                        <td>Measures nutrient concentration</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-thermometer-half"></i> Temperature Probes</td>
                        <td>Track water and air temperature</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-cloud"></i> Humidity Sensor</td>
                        <td>Monitors moisture levels</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-database"></i> Data Logger</td>
                        <td>Captures sensor readings</td>
                    </tr>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar content
    with st.sidebar:
        st.title("🍓 AQUAMIND")
        
        # Authentication section
        if not st.session_state['auth_status']:
            auth.render_login_signup()
        else:
            st.success(f"Welcome, {st.session_state['auth_user']['name']}!")
            if st.button("Logout"):
                auth.logout()
                st.rerun()
        
        st.divider()
        
        # Only show data filters if authenticated
        if st.session_state['auth_status']:
            st.subheader("Data Filters")
            
            # Strawberry variety filter
            if st.session_state['strawberry_data'] is not None:
                varieties = ["All"] + sorted(st.session_state['strawberry_data']["Variety"].unique().tolist())
                selected_variety = st.selectbox("Strawberry Variety", varieties, index=0)
                if selected_variety != st.session_state['selected_variety']:
                    st.session_state['selected_variety'] = selected_variety
                    
                # Date range filter
                min_date = pd.to_datetime(st.session_state['strawberry_data']['Date'].min()).to_pydatetime()
                max_date = pd.to_datetime(st.session_state['strawberry_data']['Date'].max()).to_pydatetime()
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    st.session_state['date_range'] = date_range
                    
            else:
                st.warning("No data available. Please upload data file.")
    
    # Main content
    if not st.session_state['auth_status']:
        st.title("AQUAMIND Dashboard")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## Welcome to AQUAMIND!
            
            Your comprehensive solution for monitoring and optimizing strawberry growth in aquaponics systems.
            
            **Features:**
            - 📊 Real-time monitoring of pH, EC, humidity, and water temperature
            - 📈 Advanced data visualization and trend analysis
            - 🧠 AI-powered predictions for optimal growth conditions
            - 🔍 Disease identification and treatment recommendations
            - 🌱 Nutrient management for maximum yield
            
            Please login or signup to access the dashboard.
            """)
            
        with col2:
            st.markdown("""
            ### Getting Started
            
            1. Create an account or login
            2. Connect your sensor data
            3. Explore the dashboard
            4. Optimize your growing conditions
            
            Need help? Check out the documentation in the settings page.
            """)

    else:
        # Show welcome message
        st.title(f"Welcome to your AQUAMIND Dashboard")
        st.markdown("Use the sidebar to navigate between different sections of the application.")
        
        # Show quick stats
        st.subheader("📊 Quick Stats")
        
        if st.session_state['strawberry_data'] is not None:
            data = st.session_state['strawberry_data']
            
            # Filter data based on selected variety
            if st.session_state['selected_variety'] != "All":
                data = data[data["Variety"] == st.session_state['selected_variety']]
            
            # Filter data based on selected date range
            if st.session_state['date_range'][0] is not None and st.session_state['date_range'][1] is not None:
                # Convert pandas datetime to python datetime for proper comparison
                start_date = pd.to_datetime(st.session_state['date_range'][0]).to_pydatetime()
                end_date = pd.to_datetime(st.session_state['date_range'][1]).to_pydatetime()
                
                # Use the converted dates for filtering
                data = data[(data["Date"] >= start_date) & 
                           (data["Date"] <= end_date)]
            
            # Create metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_ph = data["pH"].mean()
                st.metric("Average pH", f"{avg_ph:.2f}")
                
            with col2:
                avg_ec = data["EC_mS_cm"].mean()
                st.metric("Average EC (mS/cm)", f"{avg_ec:.2f}")
                
            with col3:
                avg_humidity = data["Humidity_pct"].mean()
                st.metric("Average Humidity (%)", f"{avg_humidity:.1f}")
                
            with col4:
                avg_water_temp = data["Water_Temp_C"].mean()
                st.metric("Average Water Temp (°C)", f"{avg_water_temp:.1f}")
        
            # Add status section
            st.subheader("🚦 System Status")
            
            # Get the latest readings
            latest_date = data["Date"].max()
            latest_data = data[data["Date"] == latest_date]
            
            if not latest_data.empty:
                latest_entry = latest_data.iloc[0]
                
                status_col1, status_col2 = st.columns(2)
                
                with status_col1:
                    status_message, status_color = utils.evaluate_system_status(
                        latest_entry["pH"], 
                        latest_entry["EC_mS_cm"], 
                        latest_entry["Humidity_pct"], 
                        latest_entry["Water_Temp_C"]
                    )
                    
                    st.markdown(f"<div style='background-color:{status_color};padding:10px;border-radius:5px;'>"
                                f"<h3 style='color:white;margin:0;'>System Status: {status_message}</h3>"
                                f"</div>", unsafe_allow_html=True)
                
                with status_col2:
                    # Latest readings table
                    st.markdown("#### Latest Readings")
                    latest_readings = {
                        "Parameter": ["pH", "EC (mS/cm)", "Humidity (%)", "Water Temp (°C)"],
                        "Value": [
                            f"{latest_entry['pH']:.2f}",
                            f"{latest_entry['EC_mS_cm']:.2f}",
                            f"{latest_entry['Humidity_pct']:.1f}",
                            f"{latest_entry['Water_Temp_C']:.1f}"
                        ]
                    }
                    st.dataframe(pd.DataFrame(latest_readings), hide_index=True)
        
            # Add navigation section
            st.subheader("📱 Quick Navigation")
            
            nav_col1, nav_col2, nav_col3 = st.columns(3)
            
            with nav_col1:
                if st.button("📊 Data Explorer", use_container_width=True):
                    st.switch_page("pages/2_Data_Explorer.py")
                
                if st.button("🧠 Predictions", use_container_width=True):
                    st.switch_page("pages/3_Predictions.py")
            
            with nav_col2:
                if st.button("🦠 Disease Management", use_container_width=True):
                    st.switch_page("pages/4_Disease_Management.py")
                
                if st.button("🌿 Nutrient Management", use_container_width=True):
                    st.switch_page("pages/5_Nutrient_Management.py")
            
            with nav_col3:
                if st.button("🔄 Refresh Data", use_container_width=True):
                    st.session_state['strawberry_data'] = load_strawberry_data()
                    st.rerun()
                
                if st.button("⚙️ Settings", use_container_width=True):
                    st.switch_page("pages/6_Settings.py")
        
        else:
            st.error("No data available. Please check your data source or contact support.")

if __name__ == "__main__":
    main()
