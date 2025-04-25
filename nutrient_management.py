import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def get_growth_stages():
    """Get information about strawberry growth stages."""
    return {
        "propagation": {
            "name": "Propagation",
            "description": "The initial stage where runners develop into new plants.",
            "duration": "2-3 weeks",
            "key_indicators": [
                "Root development",
                "Initial leaf formation"
            ]
        },
        "vegetative": {
            "name": "Vegetative Growth",
            "description": "Plants focus on leaf and root development.",
            "duration": "4-6 weeks",
            "key_indicators": [
                "Rapid leaf production",
                "Crown development",
                "No flowering yet"
            ]
        },
        "flowering": {
            "name": "Flowering",
            "description": "Plants produce flowers that will become fruits.",
            "duration": "2-3 weeks",
            "key_indicators": [
                "White flowers appear",
                "Reduced leaf growth",
                "Increased nutrient demand"
            ]
        },
        "fruiting": {
            "name": "Fruiting",
            "description": "Flowers develop into fruits, requiring high energy.",
            "duration": "4-6 weeks",
            "key_indicators": [
                "Green fruits developing",
                "Color change as fruits ripen",
                "Peak nutrient demand"
            ]
        },
        "post_harvest": {
            "name": "Post-Harvest",
            "description": "Plants recover and prepare for the next production cycle.",
            "duration": "2-4 weeks",
            "key_indicators": [
                "Decreased nutrient demand",
                "Renewal of vegetative growth",
                "Runner production (in some varieties)"
            ]
        }
    }

def get_nutrient_recommendations():
    """Get nutrient recommendations for different growth stages."""
    return {
        "propagation": {
            "pH": (5.8, 6.2),
            "EC_mS_cm": (0.8, 1.2),
            "N_ppm": (70, 100),
            "P_ppm": (30, 50),
            "K_ppm": (80, 120),
            "Ca_ppm": (80, 120),
            "Mg_ppm": (30, 50),
            "S_ppm": (40, 60),
            "Fe_ppm": (2.0, 4.0),
            "Mn_ppm": (0.3, 0.5),
            "Zn_ppm": (0.1, 0.3),
            "Cu_ppm": (0.05, 0.1),
            "B_ppm": (0.2, 0.4),
            "Mo_ppm": (0.02, 0.05)
        },
        "vegetative": {
            "pH": (5.8, 6.2),
            "EC_mS_cm": (1.2, 1.6),
            "N_ppm": (100, 150),
            "P_ppm": (40, 60),
            "K_ppm": (120, 150),
            "Ca_ppm": (120, 160),
            "Mg_ppm": (40, 60),
            "S_ppm": (50, 70),
            "Fe_ppm": (3.0, 5.0),
            "Mn_ppm": (0.4, 0.8),
            "Zn_ppm": (0.3, 0.5),
            "Cu_ppm": (0.1, 0.2),
            "B_ppm": (0.3, 0.5),
            "Mo_ppm": (0.03, 0.06)
        },
        "flowering": {
            "pH": (5.8, 6.2),
            "EC_mS_cm": (1.4, 1.8),
            "N_ppm": (120, 150),
            "P_ppm": (50, 70),
            "K_ppm": (150, 180),
            "Ca_ppm": (140, 180),
            "Mg_ppm": (45, 65),
            "S_ppm": (60, 80),
            "Fe_ppm": (4.0, 6.0),
            "Mn_ppm": (0.5, 1.0),
            "Zn_ppm": (0.4, 0.6),
            "Cu_ppm": (0.15, 0.25),
            "B_ppm": (0.4, 0.6),
            "Mo_ppm": (0.04, 0.08)
        },
        "fruiting": {
            "pH": (5.8, 6.2),
            "EC_mS_cm": (1.8, 2.2),
            "N_ppm": (120, 150),
            "P_ppm": (60, 80),
            "K_ppm": (180, 220),
            "Ca_ppm": (150, 200),
            "Mg_ppm": (50, 70),
            "S_ppm": (65, 85),
            "Fe_ppm": (4.0, 6.0),
            "Mn_ppm": (0.5, 1.0),
            "Zn_ppm": (0.4, 0.6),
            "Cu_ppm": (0.15, 0.25),
            "B_ppm": (0.5, 0.7),
            "Mo_ppm": (0.05, 0.1)
        },
        "post_harvest": {
            "pH": (5.8, 6.2),
            "EC_mS_cm": (1.0, 1.4),
            "N_ppm": (80, 120),
            "P_ppm": (40, 60),
            "K_ppm": (100, 140),
            "Ca_ppm": (100, 140),
            "Mg_ppm": (35, 55),
            "S_ppm": (45, 65),
            "Fe_ppm": (2.5, 4.5),
            "Mn_ppm": (0.3, 0.6),
            "Zn_ppm": (0.2, 0.4),
            "Cu_ppm": (0.1, 0.2),
            "B_ppm": (0.3, 0.5),
            "Mo_ppm": (0.03, 0.06)
        }
    }

def get_deficiency_symptoms():
    """Get symptoms of nutrient deficiencies in strawberries."""
    return {
        "N": {
            "name": "Nitrogen",
            "symptoms": [
                "Older leaves turn pale green or yellow",
                "Stunted growth",
                "Reduced fruit size and yield",
                "Early leaf senescence"
            ],
            "correction": [
                "Increase nitrogen in nutrient solution",
                "Apply calcium nitrate or potassium nitrate",
                "Ensure pH is in optimal range for nitrogen uptake (5.8-6.2)"
            ]
        },
        "P": {
            "name": "Phosphorus",
            "symptoms": [
                "Stunted root and shoot growth",
                "Older leaves develop purple or reddish color",
                "Delayed flowering and fruiting",
                "Dull green leaves with necrotic spots"
            ],
            "correction": [
                "Add monopotassium phosphate (MKP) to nutrient solution",
                "Lower pH slightly if above 6.5 to improve phosphorus availability",
                "Ensure water temperature is at least 18°C for proper uptake"
            ]
        },
        "K": {
            "name": "Potassium",
            "symptoms": [
                "Marginal leaf scorching (brown edges)",
                "Interveinal chlorosis in older leaves",
                "Weak stems and poor fruit development",
                "Increased susceptibility to disease and stress"
            ],
            "correction": [
                "Add potassium sulfate or potassium nitrate to nutrient solution",
                "Balance calcium levels, as high calcium can compete with potassium",
                "Increase frequency of nutrient solution changes"
            ]
        },
        "Ca": {
            "name": "Calcium",
            "symptoms": [
                "Distorted young leaves with hooked tips",
                "Necrosis at growing points",
                "Soft, water-soaked areas on fruits (tip burn)",
                "Poor fruit firmness and shelf life"
            ],
            "correction": [
                "Add calcium nitrate to nutrient solution",
                "Maintain steady water supply to ensure calcium transport",
                "Avoid high humidity which reduces transpiration and calcium movement",
                "Ensure pH is not too high (above 6.5)"
            ]
        },
        "Mg": {
            "name": "Magnesium",
            "symptoms": [
                "Interveinal chlorosis in older leaves",
                "Reddish-purple leaf margins",
                "Leaves may become brittle and fall prematurely",
                "Reduced photosynthesis and growth"
            ],
            "correction": [
                "Add magnesium sulfate (Epsom salt) to nutrient solution",
                "Balance with calcium and potassium levels",
                "Maintain pH between 5.8-6.2 for optimal magnesium uptake"
            ]
        },
        "S": {
            "name": "Sulfur",
            "symptoms": [
                "Younger leaves turn pale green or yellow",
                "Stunted growth with thin stems",
                "Small leaves with reduced photosynthesis",
                "Delayed fruit ripening"
            ],
            "correction": [
                "Add magnesium sulfate or potassium sulfate to nutrient solution",
                "Ensure water pH is below 7.0 for better sulfur availability",
                "Check for proper aeration in root zone"
            ]
        },
        "Fe": {
            "name": "Iron",
            "symptoms": [
                "Interveinal chlorosis in young leaves",
                "New leaves appear yellow with green veins",
                "Stunted growth and reduced yield",
                "In severe cases, leaves may become completely white"
            ],
            "correction": [
                "Add iron chelate (EDDHA or DTPA) to nutrient solution",
                "Lower pH to 5.8-6.0 to improve iron availability",
                "Avoid excessive phosphorus which can precipitate iron",
                "Ensure proper aeration of nutrient solution"
            ]
        },
        "Mn": {
            "name": "Manganese",
            "symptoms": [
                "Interveinal chlorosis similar to iron deficiency but less pronounced",
                "Gray speck on leaves (tiny necrotic spots)",
                "Reduced leaf size and distortion",
                "Poor flowering and fruiting"
            ],
            "correction": [
                "Add manganese sulfate to nutrient solution",
                "Lower pH if above 6.2 to improve manganese availability",
                "Avoid excessive iron which can compete with manganese uptake"
            ]
        },
        "Zn": {
            "name": "Zinc",
            "symptoms": [
                "Interveinal chlorosis with mottled appearance",
                "Small, narrow leaves clustered at shoot tips",
                "Shortened internodes leading to rosette appearance",
                "Reduced fruit size and quality"
            ],
            "correction": [
                "Add zinc sulfate or zinc chelate to nutrient solution",
                "Maintain pH below 6.5 for better zinc availability",
                "Avoid excessive phosphorus which can reduce zinc uptake"
            ]
        },
        "Cu": {
            "name": "Copper",
            "symptoms": [
                "Young leaves appear dark green and twisted",
                "Necrotic spots on leaf margins",
                "Wilting despite adequate moisture",
                "Poor fruit development and reduced pollen viability"
            ],
            "correction": [
                "Add copper sulfate or copper chelate in very small amounts",
                "Maintain pH between 5.5-6.5 for optimal copper availability",
                "Be cautious with copper as toxicity can occur easily"
            ]
        },
        "B": {
            "name": "Boron",
            "symptoms": [
                "Deformed young leaves with brittle texture",
                "Death of growing points (terminal buds)",
                "Hollow or discolored fruit (hollow heart)",
                "Poor pollen development and fruit set"
            ],
            "correction": [
                "Add boric acid or sodium borate in very small amounts",
                "Maintain consistent moisture as boron moves with water",
                "Be very cautious with application as toxicity occurs easily"
            ]
        },
        "Mo": {
            "name": "Molybdenum",
            "symptoms": [
                "Older leaves develop interveinal chlorosis",
                "Leaf margins appear scorched or burned",
                "Stunted growth with reduced nitrogen utilization",
                "Poor fruit development"
            ],
            "correction": [
                "Add sodium molybdate in very small amounts",
                "Raise pH slightly if below 5.5 to improve molybdenum availability",
                "Ensure proper nitrogen metabolism by balancing nutrients"
            ]
        }
    }

def calculate_nutrient_adjustment(current_stage, current_values, variety="General"):
    """Calculate nutrient adjustments based on current values and growth stage."""
    recommendations = get_nutrient_recommendations()
    
    # Get recommendations for the current stage
    stage_recs = recommendations.get(current_stage, recommendations["vegetative"])
    
    # Calculate adjustments
    adjustments = {}
    
    for param, value in current_values.items():
        if param in stage_recs:
            min_val, max_val = stage_recs[param]
            
            # Calculate percentage deviation from optimal range
            if value < min_val:
                # Below optimal - increase needed
                pct_change = ((min_val - value) / min_val) * 100
                adjustments[param] = {
                    "current": value,
                    "optimal": f"{min_val} - {max_val}",
                    "adjustment": "increase",
                    "percentage": min(pct_change, 50),  # Cap at 50% increase
                    "new_value": value * (1 + min(pct_change/100, 0.5))
                }
            elif value > max_val:
                # Above optimal - decrease needed
                pct_change = ((value - max_val) / max_val) * 100
                adjustments[param] = {
                    "current": value,
                    "optimal": f"{min_val} - {max_val}",
                    "adjustment": "decrease",
                    "percentage": min(pct_change, 50),  # Cap at 50% decrease
                    "new_value": value * (1 - min(pct_change/100, 0.5))
                }
            else:
                # Within optimal range - no adjustment needed
                adjustments[param] = {
                    "current": value,
                    "optimal": f"{min_val} - {max_val}",
                    "adjustment": "maintain",
                    "percentage": 0,
                    "new_value": value
                }
    
    return adjustments

def plot_nutrient_recommendations(stage):
    """Create a plot comparing nutrient recommendations across growth stages."""
    recommendations = get_nutrient_recommendations()
    
    # Create data for plotting
    stages = list(recommendations.keys())
    nutrients = ["N_ppm", "P_ppm", "K_ppm", "Ca_ppm", "Mg_ppm"]
    
    data = []
    for s in stages:
        for nutrient in nutrients:
            if nutrient in recommendations[s]:
                min_val, max_val = recommendations[s][nutrient]
                mid_val = (min_val + max_val) / 2
                
                # Add row for this stage and nutrient
                data.append({
                    "Stage": s,
                    "Nutrient": nutrient.split("_")[0],  # Remove _ppm suffix
                    "Value": mid_val,
                    "Min": min_val,
                    "Max": max_val,
                    "IsCurrentStage": s == stage
                })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create chart
    stage_order = ["propagation", "vegetative", "flowering", "fruiting", "post_harvest"]
    nutrient_order = ["N", "P", "K", "Ca", "Mg"]
    
    # Define color scale based on current stage
    color_scale = alt.condition(
        alt.datum.IsCurrentStage,
        alt.value('#e53935'),  # Highlight current stage
        alt.value('#7c7c7c')   # Other stages
    )
    
    # Create a grouped bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Stage:N', sort=stage_order, title='Growth Stage'),
        y=alt.Y('Value:Q', title='Concentration (ppm)'),
        color=color_scale,
        column=alt.Column('Nutrient:N', sort=nutrient_order),
        tooltip=[
            alt.Tooltip('Stage:N', title='Stage'),
            alt.Tooltip('Nutrient:N', title='Nutrient'),
            alt.Tooltip('Min:Q', title='Min (ppm)'),
            alt.Tooltip('Max:Q', title='Max (ppm)')
        ]
    ).properties(
        width=120,
        height=300,
        title='Nutrient Recommendations by Growth Stage'
    )
    
    return chart

def get_parameter_label(parameter):
    """Get display label for a parameter."""
    labels = {
        "pH": "pH",
        "EC_mS_cm": "EC (mS/cm)",
        "N_ppm": "Nitrogen (ppm)",
        "P_ppm": "Phosphorus (ppm)",
        "K_ppm": "Potassium (ppm)",
        "Ca_ppm": "Calcium (ppm)",
        "Mg_ppm": "Magnesium (ppm)",
        "S_ppm": "Sulfur (ppm)",
        "Fe_ppm": "Iron (ppm)",
        "Mn_ppm": "Manganese (ppm)",
        "Zn_ppm": "Zinc (ppm)",
        "Cu_ppm": "Copper (ppm)",
        "B_ppm": "Boron (ppm)",
        "Mo_ppm": "Molybdenum (ppm)"
    }
    return labels.get(parameter, parameter)
