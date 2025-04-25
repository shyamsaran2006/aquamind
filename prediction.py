import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def train_prediction_model(df, target_param, prediction_days=30):
    """
    Train a prediction model for a specific parameter.

    Args:
        df: DataFrame containing historical data
        target_param: Parameter to predict (pH, EC_mS_cm, etc.)
        prediction_days: Number of days to predict into the future

    Returns:
        model: Trained model
        preprocessor: Data preprocessor
        features: List of feature names
        future_dates: List of future dates
        predictions: Predicted values
        r2: R-squared value of the model
        rmse: Root mean squared error of the model
    """
    if df is None or df.empty:
        return None, None, None, None, None, None, None

    # Make a copy of the dataframe to avoid modifying the original
    data = df.copy()

    # Extract date features
    data['year'] = data['Date'].dt.year
    data['month'] = data['Date'].dt.month
    data['day'] = data['Date'].dt.day
    data['dayofweek'] = data['Date'].dt.dayofweek

    # Create lag features (previous days' values)
    # For each parameter, create a 1-day, 3-day, and 7-day lag feature
    parameters = ['pH', 'EC_mS_cm', 'Humidity_pct', 'Water_Temp_C', 'Air_Temp_C']

    # Group by variety and time of day for lag features
    for variety in data['Variety'].unique():
        for time in ['Morning', 'Evening']:
            mask = (data['Variety'] == variety) & (data['Time'] == time)

            for param in parameters:
                for lag in [1, 3, 7]:
                    # Create lag features
                    lag_col = f'{param}_lag{lag}'
                    data.loc[mask, lag_col] = data.loc[mask, param].shift(lag)

    # Drop rows with NaN values (these will be the first 7 days for each variety/time combo)
    data = data.dropna()

    # Split the dataframe into features and target
    features = ['year', 'month', 'day', 'dayofweek', 'Variety', 'Time']
    # Add lag features for the target parameter
    for lag in [1, 3, 7]:
        features.append(f'{target_param}_lag{lag}')

    X = data[features]
    y = data[target_param]

    # Define preprocessor
    categorical_features = ['Variety', 'Time']
    numeric_features = [f for f in features if f not in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    # Define model
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Calculate model metrics
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Generate predictions for the future
    future_dates = [data['Date'].max() + timedelta(days=i+1) for i in range(prediction_days)]

    # Create a dataframe for future predictions
    future_data = []

    for variety in data['Variety'].unique():
        for time in ['Morning', 'Evening']:
            # Get the most recent data for this variety and time
            recent_data = data[(data['Variety'] == variety) & (data['Time'] == time)].iloc[-1]

            # For each future date, create a row
            for future_date in future_dates:
                row = {
                    'Date': future_date,
                    'Variety': variety,
                    'Time': time,
                    'year': future_date.year,
                    'month': future_date.month,
                    'day': future_date.day,
                    'dayofweek': future_date.weekday()
                }

                # Add lag features (initially from the recent data)
                for lag in [1, 3, 7]:
                    row[f'{target_param}_lag{lag}'] = recent_data[f'{target_param}_lag{lag}']

                future_data.append(row)

    future_df = pd.DataFrame(future_data)

    # Make predictions for each future date, using the predictions from previous dates as lag features
    predictions = []

    for i in range(prediction_days):
        day_predictions = []

        for variety in data['Variety'].unique():
            for time in ['Morning', 'Evening']:
                mask = (future_df['Date'] == future_dates[i]) & (future_df['Variety'] == variety) & (future_df['Time'] == time)
                day_features = future_df.loc[mask, features].copy()

                # Make prediction
                pred = model.predict(day_features)[0]

                # Store prediction
                day_predictions.append({
                    'Date': future_dates[i],
                    'Variety': variety,
                    'Time': time,
                    target_param: pred
                })

                # Update lag features for future predictions if needed
                if i + 1 < prediction_days:
                    next_day_mask = (future_df['Date'] == future_dates[i+1]) & (future_df['Variety'] == variety) & (future_df['Time'] == time)

                    # Update 1-day lag with current prediction
                    future_df.loc[next_day_mask, f'{target_param}_lag1'] = pred

                    # Update 3-day lag if we have enough history
                    if len(day_predictions) >= 3 * len(data['Variety'].unique()) * len(['Morning', 'Evening']):
                        idx = -(3 * len(data['Variety'].unique()) * len(['Morning', 'Evening']))
                        three_days_ago = day_predictions[idx][target_param]
                        future_df.loc[next_day_mask, f'{target_param}_lag3'] = three_days_ago

                    # Update 7-day lag if we have enough history
                    if len(day_predictions) >= 7 * len(data['Variety'].unique()) * len(['Morning', 'Evening']):
                        idx = -(7 * len(data['Variety'].unique()) * len(['Morning', 'Evening']))
                        seven_days_ago = day_predictions[idx][target_param]
                        future_df.loc[next_day_mask, f'{target_param}_lag7'] = seven_days_ago

        predictions.extend(day_predictions)

    return model, preprocessor, features, future_dates, pd.DataFrame(predictions), r2, rmse

def plot_predictions(historical_df, predictions_df, target_param, variety="All"):
    """Plot the historical data and predictions for a specific parameter."""
    if historical_df is None or predictions_df is None:
        return None

    # Filter historical data by variety if specified
    if variety != "All":
        historical_filtered = historical_df[historical_df["Variety"] == variety]
    else:
        historical_filtered = historical_df

    # Filter predictions by variety if specified
    if variety != "All":
        predictions_filtered = predictions_df[predictions_df["Variety"] == variety]
    else:
        # For 'All', calculate the mean across all varieties
        predictions_filtered = predictions_df.groupby(["Date", "Time"])[target_param].mean().reset_index()

    # Create figure
    fig = go.Figure()

    # Plot historical data (last 60 days)
    last_60_days = historical_filtered[historical_filtered["Date"] >= historical_filtered["Date"].max() - timedelta(days=60)]

    for time in ["Morning", "Evening"]:
        # Historical data
        historical_time = last_60_days[last_60_days["Time"] == time]
        if not historical_time.empty:
            # Calculate daily average if variety = "All"
            if variety == "All":
                historical_time = historical_time.groupby("Date")[target_param].mean().reset_index()
                fig.add_trace(go.Scatter(
                    x=historical_time["Date"],
                    y=historical_time[target_param],
                    mode="lines+markers",
                    name=f"Historical ({time})",
                    line=dict(color="blue" if time == "Morning" else "orange")
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=historical_time["Date"],
                    y=historical_time[target_param],
                    mode="lines+markers",
                    name=f"Historical ({time})",
                    line=dict(color="blue" if time == "Morning" else "orange")
                ))

        # Predictions
        predictions_time = predictions_filtered[predictions_filtered["Time"] == time] if "Time" in predictions_filtered.columns else predictions_filtered

        if not predictions_time.empty:
            fig.add_trace(go.Scatter(
                x=predictions_time["Date"],
                y=predictions_time[target_param],
                mode="lines+markers",
                name=f"Predicted ({time})",
                line=dict(color="lightblue" if time == "Morning" else "gold", dash="dash")
            ))

    # Add vertical line separating historical and predicted data
    if not historical_filtered.empty:
        last_historical_date = pd.to_datetime(historical_filtered["Date"].max())

        fig.add_vline(
            x=last_historical_date.timestamp() * 1000,  # Convert to milliseconds timestamp
            line_dash="dash",
            line_color="gray",
            annotation_text="Prediction Start",
            annotation_position="top right"
        )

    # Add optimal range if available
    optimal_ranges = get_optimal_ranges()
    if target_param in optimal_ranges:
        min_val, max_val = optimal_ranges[target_param]
        fig.add_hrect(
            y0=min_val, 
            y1=max_val,
            line_width=0, 
            fillcolor="green", 
            opacity=0.1,
            annotation_text="Optimal Range",
            annotation_position="top right"
        )

    # Customize layout
    fig.update_layout(
        title=f"{target_param} Forecast" + (f" - {variety}" if variety != "All" else ""),
        xaxis_title="Date",
        yaxis_title=get_parameter_label(target_param),
        template="plotly_white",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0)
    )

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

def plot_feature_importance(model, features, target_param):
    """Plot feature importance for the prediction model."""
    if model is None or features is None:
        return None

    # Get feature importance from the random forest model
    if hasattr(model['regressor'], 'feature_importances_'):
        # Get feature names after preprocessing
        preprocessor = model['preprocessor']

        # Get the column transformer
        cat_transformer = preprocessor.named_transformers_['cat']
        num_transformer = preprocessor.named_transformers_['num']

        # Get categorical feature names after one-hot encoding
        cat_features = preprocessor.transformers_[1][2]  # ['Variety', 'Time']
        cat_feature_names = []
        for i, feature in enumerate(cat_features):
            # Get the categories from the encoder
            categories = cat_transformer.categories_[i]
            # Create feature names
            for category in categories:
                cat_feature_names.append(f"{feature}_{category}")

        # Get numeric feature names
        num_features = preprocessor.transformers_[0][2]  # numeric features

        # Combine all feature names
        all_feature_names = num_features + cat_feature_names

        # Get feature importances
        importances = model['regressor'].feature_importances_

        # Create a DataFrame for plotting
        importance_df = pd.DataFrame({
            'Feature': all_feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)

        # Plot the top 15 features
        fig = px.bar(
            importance_df.head(15),
            x='Importance',
            y='Feature',
            orientation='h',
            title=f"Feature Importance for {target_param} Prediction",
            template="plotly_white"
        )

        # Customize layout
        fig.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=50, b=0),
            yaxis=dict(title=''),
            xaxis=dict(title='Relative Importance')
        )

        return fig

    return None