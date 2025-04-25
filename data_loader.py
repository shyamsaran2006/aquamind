import streamlit as st
import pandas as pd
import os
import database

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_strawberry_data():
    """Load strawberry data from CSV file or database."""
    # First try to load from database
    latest_readings = database.get_latest_readings()
    if latest_readings is not None and not latest_readings.empty:
        return process_dataframe(latest_readings)
    
    # If database is empty or error, load from CSV
    csv_path = "attached_assets/strawberry_dataset_3years.csv"
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return process_dataframe(df)
        except Exception as e:
            st.error(f"Error loading data from CSV: {str(e)}")
            return None
    else:
        st.error(f"Data file not found: {csv_path}")
        return None

def process_dataframe(df):
    """Process the dataframe for consistent column names and data types."""
    # Ensure consistent column names
    if "date" in df.columns:
        df.rename(columns={
            "date": "Date",
            "variety": "Variety",
            "time_of_day": "Time",
            "ph": "pH",
            "ec_ms_cm": "EC_mS_cm",
            "humidity_pct": "Humidity_pct",
            "water_temp_c": "Water_Temp_C",
            "air_temp_c": "Air_Temp_C"
        }, inplace=True)
    
    # Convert date column to datetime if it's not already
    if df["Date"].dtype != 'datetime64[ns]':
        df["Date"] = pd.to_datetime(df["Date"])
    
    return df

def filter_data(df, variety="All", start_date=None, end_date=None, time_of_day=None):
    """Filter data based on variety, date range, and time of day."""
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    # Filter by variety
    if variety != "All":
        filtered_df = filtered_df[filtered_df["Variety"] == variety]
    
    # Filter by date range
    if start_date is not None and end_date is not None:
        filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & 
                                 (filtered_df["Date"] <= end_date)]
    
    # Filter by time of day
    if time_of_day is not None:
        filtered_df = filtered_df[filtered_df["Time"] == time_of_day]
    
    return filtered_df

def get_optimal_ranges():
    """Get optimal parameter ranges for strawberry growth."""
    return {
        "pH": (5.8, 6.2),
        "EC_mS_cm": (1.5, 2.0),
        "Humidity_pct": (65, 75),
        "Water_Temp_C": (18, 22)
    }

def get_variety_info():
    """Get information about different strawberry varieties."""
    return {
        "Camarosa": {
            "origin": "University of California, 1992",
            "characteristics": "Large, firm, dark red berries with good flavor",
            "growth_habit": "Vigorous with large crowns",
            "ph_preference": (5.9, 6.1),
            "water_temp_preference": (18, 20),
            "ec_preference": (1.5, 1.7)
        },
        "Chandler": {
            "origin": "University of California, 1983",
            "characteristics": "Medium to large berries, good flavor, high yield",
            "growth_habit": "Moderately vigorous with multiple crowns",
            "ph_preference": (6.0, 6.2),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.8)
        },
        "Honeoye": {
            "origin": "Cornell University, 1979",
            "characteristics": "Medium-large, bright red berries with good flavor",
            "growth_habit": "Very vigorous with strong crowns",
            "ph_preference": (6.2, 6.6),
            "water_temp_preference": (18, 20),
            "ec_preference": (1.4, 1.6)
        },
        "Seascape": {
            "origin": "University of California, 1991",
            "characteristics": "Medium-sized, firm berries with excellent flavor",
            "growth_habit": "Compact with moderate vigor",
            "ph_preference": (5.8, 6.0),
            "water_temp_preference": (20, 22),
            "ec_preference": (1.7, 2.0)
        },
        "Sweet Charlie": {
            "origin": "University of Florida, 1992",
            "characteristics": "Medium-sized, sweet berries",
            "growth_habit": "Moderate vigor with good crown production",
            "ph_preference": (6.0, 6.2),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.7)
        },
        "Ozark Beauty": {
            "origin": "University of Arkansas, 1955",
            "characteristics": "Medium-sized, sweet berries with good aroma",
            "growth_habit": "Moderate vigor, everbearing",
            "ph_preference": (6.2, 6.5),
            "water_temp_preference": (18, 20),
            "ec_preference": (1.4, 1.6)
        },
        "Quinault": {
            "origin": "Washington State University, 1967",
            "characteristics": "Medium-sized, soft berries with good flavor",
            "growth_habit": "Moderate vigor, everbearing",
            "ph_preference": (5.9, 6.1),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.7)
        },
        "Ogallala": {
            "origin": "USDA, Nebraska, 1978",
            "characteristics": "Small to medium, very sweet berries",
            "growth_habit": "Hardy with moderate vigor",
            "ph_preference": (6.0, 6.3),
            "water_temp_preference": (18, 20),
            "ec_preference": (1.3, 1.5)
        },
        "Albion": {
            "origin": "University of California, 2006",
            "characteristics": "Large, firm, dark red berries with excellent flavor",
            "growth_habit": "Upright with moderate vigor, day-neutral",
            "ph_preference": (5.8, 6.0),
            "water_temp_preference": (20, 22),
            "ec_preference": (1.6, 1.9)
        },
        "San Andreas": {
            "origin": "University of California, 2009",
            "characteristics": "Large, firm, red berries with good flavor",
            "growth_habit": "Upright with good vigor, day-neutral",
            "ph_preference": (5.8, 6.0),
            "water_temp_preference": (20, 22),
            "ec_preference": (1.6, 1.8)
        },
        "Monterey": {
            "origin": "University of California, 2009",
            "characteristics": "Large, flavorful berries",
            "growth_habit": "Vigorous with multiple crowns, day-neutral",
            "ph_preference": (5.9, 6.1),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.7)
        },
        "Evie-2": {
            "origin": "Edward Vinson Ltd, UK, 2006",
            "characteristics": "Medium to large berries with good flavor",
            "growth_habit": "Moderately vigorous, day-neutral",
            "ph_preference": (6.0, 6.2),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.7)
        },
        "Tribute": {
            "origin": "University of Maryland, 1981",
            "characteristics": "Medium-sized, firm berries with good flavor",
            "growth_habit": "Moderate vigor, day-neutral",
            "ph_preference": (6.0, 6.2),
            "water_temp_preference": (19, 21),
            "ec_preference": (1.5, 1.7)
        }
    }
