import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def evaluate_system_status(ph, ec, humidity, water_temp):
    """Evaluate the overall system status based on parameters."""
    # Define optimal ranges
    optimal_ranges = {
        "pH": (5.8, 6.2),
        "EC_mS_cm": (1.5, 2.0),
        "Humidity_pct": (65, 75),
        "Water_Temp_C": (18, 22)
    }
    
    # Check if parameters are within optimal range
    issues = []
    
    # Check pH
    if ph < optimal_ranges["pH"][0]:
        issues.append(f"pH is too low ({ph:.2f})")
    elif ph > optimal_ranges["pH"][1]:
        issues.append(f"pH is too high ({ph:.2f})")
    
    # Check EC
    if ec < optimal_ranges["EC_mS_cm"][0]:
        issues.append(f"EC is too low ({ec:.2f} mS/cm)")
    elif ec > optimal_ranges["EC_mS_cm"][1]:
        issues.append(f"EC is too high ({ec:.2f} mS/cm)")
    
    # Check humidity
    if humidity < optimal_ranges["Humidity_pct"][0]:
        issues.append(f"Humidity is too low ({humidity:.1f}%)")
    elif humidity > optimal_ranges["Humidity_pct"][1]:
        issues.append(f"Humidity is too high ({humidity:.1f}%)")
    
    # Check water temperature
    if water_temp < optimal_ranges["Water_Temp_C"][0]:
        issues.append(f"Water temperature is too low ({water_temp:.1f}°C)")
    elif water_temp > optimal_ranges["Water_Temp_C"][1]:
        issues.append(f"Water temperature is too high ({water_temp:.1f}°C)")
    
    # Determine system status
    if len(issues) == 0:
        return "Optimal", "#4CAF50"  # Green color
    elif len(issues) <= 2:
        return "Needs Attention", "#FFC107"  # Yellow/amber color
    else:
        return "Critical", "#F44336"  # Red color

def format_date_range(start_date, end_date):
    """Format a date range for display."""
    if start_date is None or end_date is None:
        return "All Time"
    
    # Format dates
    start_str = start_date.strftime("%b %d, %Y")
    end_str = end_date.strftime("%b %d, %Y")
    
    return f"{start_str} to {end_str}"

def get_date_periods():
    """Get common date periods for filtering data."""
    today = datetime.now().date()
    
    return {
        "Last 7 Days": (today - timedelta(days=7), today),
        "Last 30 Days": (today - timedelta(days=30), today),
        "Last 90 Days": (today - timedelta(days=90), today),
        "Last 6 Months": (today - timedelta(days=180), today),
        "Last Year": (today - timedelta(days=365), today),
        "All Time": (None, None)
    }

def generate_download_links(dataframe, filename="data.csv"):
    """Generate download links for a dataframe in different formats."""
    # CSV download
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
    
    # Excel download (if openpyxl is installed)
    try:
        buffer = pd.ExcelWriter(f"{filename.replace('.csv', '.xlsx')}", engine='openpyxl')
        dataframe.to_excel(buffer, index=False)
        buffer.save()
        with open(buffer.path, 'rb') as f:
            excel_data = f.read()
        
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name=filename.replace('.csv', '.xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except:
        st.write("Excel download not available. Install openpyxl for Excel support.")

def get_formatted_time():
    """Get the current time formatted for display."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
