import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def plot_parameter_trends(df, parameter, variety="All", rolling_window=7):
    """Plot trends of a parameter over time."""
    if df is None or df.empty:
        return None
    
    # Filter by variety if specified
    if variety != "All":
        filtered_df = df[df["Variety"] == variety]
    else:
        filtered_df = df
    
    # Group by date and calculate the mean of the parameter for each day
    daily_df = filtered_df.groupby("Date")[parameter].mean().reset_index()
    
    # Add a rolling average
    if len(daily_df) >= rolling_window:
        daily_df[f"{parameter}_rolling"] = daily_df[parameter].rolling(window=rolling_window).mean()
    
    # Create the plot
    fig = px.line(
        daily_df, 
        x="Date", 
        y=parameter,
        title=f"{parameter} Trend Over Time" + (f" - {variety}" if variety != "All" else ""),
        labels={parameter: get_parameter_label(parameter), "Date": "Date"},
        template="plotly_white"
    )
    
    # Add rolling average if available
    if len(daily_df) >= rolling_window:
        fig.add_scatter(
            x=daily_df["Date"], 
            y=daily_df[f"{parameter}_rolling"], 
            mode="lines", 
            name=f"{rolling_window}-Day Rolling Average",
            line=dict(color="red", width=2)
        )
    
    # Add optimal range if available
    optimal_ranges = get_optimal_ranges()
    if parameter in optimal_ranges:
        min_val, max_val = optimal_ranges[parameter]
        fig.add_hrect(
            y0=min_val, 
            y1=max_val,
            line_width=0, 
            fillcolor="green", 
            opacity=0.1,
            annotation_text="Optimal Range",
            annotation_position="top right"
        )
    
    # Customize the layout
    fig.update_layout(
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_parameter_distribution(df, parameter, variety="All"):
    """Plot distribution of a parameter."""
    if df is None or df.empty:
        return None
    
    # Filter by variety if specified
    if variety != "All":
        filtered_df = df[df["Variety"] == variety]
    else:
        filtered_df = df
    
    # Create the histogram
    fig = px.histogram(
        filtered_df, 
        x=parameter,
        title=f"Distribution of {parameter}" + (f" - {variety}" if variety != "All" else ""),
        labels={parameter: get_parameter_label(parameter)},
        template="plotly_white",
        marginal="box",
        color_discrete_sequence=["#e53935"]
    )
    
    # Add optimal range if available
    optimal_ranges = get_optimal_ranges()
    if parameter in optimal_ranges:
        min_val, max_val = optimal_ranges[parameter]
        fig.add_vrect(
            x0=min_val, 
            x1=max_val,
            line_width=0, 
            fillcolor="green", 
            opacity=0.1,
            annotation_text="Optimal Range",
            annotation_position="top right"
        )
    
    # Customize the layout
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_variety_comparison(df, parameter):
    """Plot comparison of a parameter across different varieties."""
    if df is None or df.empty:
        return None
    
    # Group by variety and calculate the mean, min, and max of the parameter
    variety_stats = df.groupby("Variety")[parameter].agg(["mean", "min", "max"]).reset_index()
    variety_stats.columns = ["Variety", "Mean", "Min", "Max"]
    variety_stats = variety_stats.sort_values("Mean", ascending=False)
    
    # Create the bar chart
    fig = go.Figure()
    
    # Add mean values as bars
    fig.add_trace(go.Bar(
        x=variety_stats["Variety"],
        y=variety_stats["Mean"],
        name="Mean",
        error_y=dict(
            type="data",
            symmetric=False,
            array=variety_stats["Max"] - variety_stats["Mean"],
            arrayminus=variety_stats["Mean"] - variety_stats["Min"]
        ),
        marker_color="#e53935"
    ))
    
    # Add optimal range if available
    optimal_ranges = get_optimal_ranges()
    if parameter in optimal_ranges:
        min_val, max_val = optimal_ranges[parameter]
        fig.add_hline(
            y=min_val,
            line_dash="dash",
            line_color="green",
            annotation_text="Optimal Min",
            annotation_position="bottom right"
        )
        fig.add_hline(
            y=max_val,
            line_dash="dash",
            line_color="green",
            annotation_text="Optimal Max",
            annotation_position="top right"
        )
    
    # Customize the layout
    fig.update_layout(
        title=f"{parameter} Comparison by Variety",
        xaxis_title="Variety",
        yaxis_title=get_parameter_label(parameter),
        template="plotly_white",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_correlation_heatmap(df, variety="All"):
    """Plot correlation heatmap between different parameters."""
    if df is None or df.empty:
        return None
    
    # Filter by variety if specified
    if variety != "All":
        filtered_df = df[df["Variety"] == variety]
    else:
        filtered_df = df
    
    # Select numerical columns
    numeric_cols = ["pH", "EC_mS_cm", "Humidity_pct", "Water_Temp_C", "Air_Temp_C"]
    
    # Calculate correlation matrix
    corr_matrix = filtered_df[numeric_cols].corr()
    
    # Create the heatmap
    fig = px.imshow(
        corr_matrix,
        title=f"Parameter Correlation" + (f" - {variety}" if variety != "All" else ""),
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        text_auto=".2f"
    )
    
    # Customize the layout
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_seasonal_patterns(df, parameter, variety="All"):
    """Plot seasonal patterns of a parameter by month."""
    if df is None or df.empty:
        return None
    
    # Extract month and year from the date
    df_copy = df.copy()
    df_copy["Month"] = df_copy["Date"].dt.month
    df_copy["Year"] = df_copy["Date"].dt.year
    
    # Filter by variety if specified
    if variety != "All":
        filtered_df = df_copy[df_copy["Variety"] == variety]
    else:
        filtered_df = df_copy
    
    # Group by year and month, calculate the mean of the parameter
    monthly_df = filtered_df.groupby(["Year", "Month"])[parameter].mean().reset_index()
    
    # Create month names for better readability
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    monthly_df["MonthName"] = monthly_df["Month"].map(month_names)
    
    # Create the plot
    fig = px.line(
        monthly_df, 
        x="Month", 
        y=parameter,
        color="Year",
        title=f"Seasonal Pattern of {parameter}" + (f" - {variety}" if variety != "All" else ""),
        labels={parameter: get_parameter_label(parameter), "Month": "Month"},
        template="plotly_white",
        markers=True
    )
    
    # Add optimal range if available
    optimal_ranges = get_optimal_ranges()
    if parameter in optimal_ranges:
        min_val, max_val = optimal_ranges[parameter]
        fig.add_hrect(
            y0=min_val, 
            y1=max_val,
            line_width=0, 
            fillcolor="green", 
            opacity=0.1,
            annotation_text="Optimal Range",
            annotation_position="top right"
        )
    
    # Customize x-axis ticks to display month names
    fig.update_xaxes(
        tickvals=list(month_names.keys()),
        ticktext=list(month_names.values())
    )
    
    # Customize the layout
    fig.update_layout(
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_parameter_radar(df, variety):
    """Plot radar chart of mean parameters for a specific variety."""
    if df is None or df.empty:
        return None
    
    # Filter by variety
    filtered_df = df[df["Variety"] == variety]
    
    if filtered_df.empty:
        return None
    
    # Calculate mean of each parameter
    params = ["pH", "EC_mS_cm", "Humidity_pct", "Water_Temp_C"]
    means = [filtered_df[param].mean() for param in params]
    
    # Get optimal ranges
    optimal_ranges = get_optimal_ranges()
    optimal_means = [(optimal_ranges[param][0] + optimal_ranges[param][1])/2 for param in params]
    
    # Normalize values to 0-1 scale for radar chart
    max_values = [7.0, 3.0, 100.0, 30.0]  # Maximum possible values for each parameter
    norm_means = [means[i]/max_values[i] for i in range(len(params))]
    norm_optimal = [optimal_means[i]/max_values[i] for i in range(len(params))]
    
    # Create radar chart
    param_labels = [get_parameter_label(param) for param in params]
    
    fig = go.Figure()
    
    # Add variety values
    fig.add_trace(go.Scatterpolar(
        r=norm_means,
        theta=param_labels,
        fill='toself',
        name=variety,
        line=dict(color='#e53935')
    ))
    
    # Add optimal values
    fig.add_trace(go.Scatterpolar(
        r=norm_optimal,
        theta=param_labels,
        fill='toself',
        name='Optimal',
        line=dict(color='green', dash='dash')
    ))
    
    # Customize layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title=f"Parameter Profile - {variety} vs Optimal",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def plot_time_of_day_comparison(df, parameter, variety="All"):
    """Plot comparison of a parameter between morning and evening readings."""
    if df is None or df.empty:
        return None
    
    # Filter by variety if specified
    if variety != "All":
        filtered_df = df[df["Variety"] == variety]
    else:
        filtered_df = df
    
    # Group by date and time of day, calculate the mean of the parameter
    time_df = filtered_df.groupby(["Date", "Time"])[parameter].mean().reset_index()
    
    # Pivot the data to have separate columns for Morning and Evening
    pivot_df = time_df.pivot(index="Date", columns="Time", values=parameter).reset_index()
    
    # Create the plot
    fig = make_subplots(rows=1, cols=2, 
                      subplot_titles=("Time Series Comparison", "Morning vs Evening Distribution"),
                      specs=[[{"type": "scatter"}, {"type": "scatter"}]])
    
    # Add time series lines
    if "Morning" in pivot_df.columns:
        fig.add_trace(
            go.Scatter(x=pivot_df["Date"], y=pivot_df["Morning"], mode="lines", name="Morning", line=dict(color="orange")),
            row=1, col=1
        )
    
    if "Evening" in pivot_df.columns:
        fig.add_trace(
            go.Scatter(x=pivot_df["Date"], y=pivot_df["Evening"], mode="lines", name="Evening", line=dict(color="blue")),
            row=1, col=1
        )
    
    # Add scatter plot of Morning vs Evening
    if "Morning" in pivot_df.columns and "Evening" in pivot_df.columns:
        fig.add_trace(
            go.Scatter(x=pivot_df["Morning"], y=pivot_df["Evening"], mode="markers", 
                      marker=dict(color="#e53935", size=8, opacity=0.6),
                      name="Morning vs Evening"),
            row=1, col=2
        )
        
        # Add diagonal line (x=y)
        max_val = max(pivot_df["Morning"].max(), pivot_df["Evening"].max())
        min_val = min(pivot_df["Morning"].min(), pivot_df["Evening"].min())
        
        fig.add_trace(
            go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode="lines", 
                      line=dict(color="black", dash="dash"), name="Equal Line"),
            row=1, col=2
        )
    
    # Customize layout
    fig.update_layout(
        title=f"Morning vs Evening {parameter} Comparison" + (f" - {variety}" if variety != "All" else ""),
        height=500,
        template="plotly_white",
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Update axis labels
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text=get_parameter_label(parameter), row=1, col=1)
    
    if "Morning" in pivot_df.columns:
        fig.update_xaxes(title_text=f"Morning {get_parameter_label(parameter)}", row=1, col=2)
    
    if "Evening" in pivot_df.columns:
        fig.update_yaxes(title_text=f"Evening {get_parameter_label(parameter)}", row=1, col=2)
    
    return fig

def get_parameter_label(parameter):
    """Get display label for a parameter."""
    labels = {
        "pH": "pH",
        "EC_mS_cm": "EC (mS/cm)",
        "Humidity_pct": "Humidity (%)",
        "Water_Temp_C": "Water Temperature (°C)",
        "Air_Temp_C": "Air Temperature (°C)"
    }
    return labels.get(parameter, parameter)

def get_optimal_ranges():
    """Get optimal parameter ranges for strawberry growth."""
    return {
        "pH": (5.8, 6.2),
        "EC_mS_cm": (1.5, 2.0),
        "Humidity_pct": (65, 75),
        "Water_Temp_C": (18, 22),
        "Air_Temp_C": (20, 25)
    }

