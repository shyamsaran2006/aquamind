import streamlit as st
import pandas as pd

def get_disease_info():
    """Get information about common strawberry diseases."""
    return {
        "anthracnose": {
            "name": "Anthracnose",
            "symptoms": [
                "Dark, water-soaked lesions on fruit",
                "Sunken, dark brown to black lesions on stolons and petioles",
                "Wilting and death of younger leaves",
                "Orange or salmon-colored spore masses in lesions during wet weather"
            ],
            "causes": [
                "Fungal pathogen: Colletotrichum species",
                "High temperature (75-80°F, 24-27°C) and high humidity",
                "Prolonged leaf wetness",
                "Overhead irrigation"
            ],
            "prevention": [
                "Use disease-free transplants",
                "Plant resistant varieties",
                "Avoid overhead irrigation",
                "Maintain good air circulation",
                "Mulch to reduce soil splashing"
            ],
            "treatment": [
                "Remove and destroy infected plants",
                "Apply fungicides preventatively during early bloom",
                "Ensure proper plant spacing for air circulation",
                "Maintain ideal pH between 6.0-6.5",
                "Control humidity levels in greenhouse systems"
            ],
            "optimal_conditions": {
                "pH": (6.0, 6.5),
                "EC_mS_cm": (1.2, 1.8),
                "Humidity_pct": (40, 60),
                "Water_Temp_C": (18, 21)
            },
            "severity_by_param": {
                "pH": lambda x: "High" if x < 5.5 or x > 7.0 else "Medium" if x < 6.0 or x > 6.5 else "Low",
                "Humidity_pct": lambda x: "High" if x > 80 else "Medium" if x > 65 else "Low",
                "Water_Temp_C": lambda x: "High" if x > 25 else "Medium" if x > 22 else "Low"
            }
        },
        "botrytis": {
            "name": "Botrytis Fruit Rot (Gray Mold)",
            "symptoms": [
                "Gray fuzzy mold on fruit",
                "Brown lesions on fruit that enlarge rapidly",
                "Soft, light brown rot on ripening fruit",
                "Light brown lesions on petals and flower parts"
            ],
            "causes": [
                "Fungal pathogen: Botrytis cinerea",
                "Cool, wet weather (65-75°F, 18-24°C)",
                "High humidity above 80%",
                "Poor air circulation",
                "Extended periods of leaf wetness"
            ],
            "prevention": [
                "Maintain good air circulation",
                "Ensure proper plant spacing",
                "Remove old leaves, flowers, and fruit",
                "Avoid overhead irrigation",
                "Use drip irrigation"
            ],
            "treatment": [
                "Remove and destroy infected plant material",
                "Apply fungicides during flowering",
                "Maintain humidity below 80%",
                "Install fans to improve air circulation",
                "Reduce irrigation frequency but maintain adequate water levels"
            ],
            "optimal_conditions": {
                "pH": (5.8, 6.2),
                "EC_mS_cm": (1.5, 2.0),
                "Humidity_pct": (60, 70),
                "Water_Temp_C": (18, 22)
            },
            "severity_by_param": {
                "pH": lambda x: "Medium" if x < 5.5 or x > 6.5 else "Low",
                "Humidity_pct": lambda x: "High" if x > 80 else "Medium" if x > 70 else "Low",
                "Water_Temp_C": lambda x: "Medium" if x < 16 or x > 24 else "Low"
            }
        },
        "powdery_mildew": {
            "name": "Powdery Mildew",
            "symptoms": [
                "White powdery growth on upper and lower leaf surfaces",
                "Upward curling of leaf edges",
                "Reddish or purplish patches on leaves",
                "Stunted plant growth",
                "Reduced fruit size and quality"
            ],
            "causes": [
                "Fungal pathogen: Podosphaera aphanis",
                "Warm days (60-80°F, 15-27°C) and cool nights",
                "High humidity but dry leaf surfaces",
                "Poor air circulation",
                "Excessive nitrogen fertilization"
            ],
            "prevention": [
                "Plant resistant varieties",
                "Ensure proper plant spacing",
                "Maintain good air circulation",
                "Avoid excessive nitrogen application",
                "Keep leaf surfaces dry"
            ],
            "treatment": [
                "Apply fungicides at first sign of disease",
                "Remove and destroy heavily infected leaves",
                "Use potassium bicarbonate sprays",
                "Maintain balanced fertilization",
                "Increase silicon in nutrient solution"
            ],
            "optimal_conditions": {
                "pH": (5.8, 6.2),
                "EC_mS_cm": (1.4, 1.8),
                "Humidity_pct": (50, 65),
                "Water_Temp_C": (18, 22)
            },
            "severity_by_param": {
                "pH": lambda x: "Medium" if x > 6.5 else "Low",
                "EC_mS_cm": lambda x: "Medium" if x > 2.2 else "Low",
                "Humidity_pct": lambda x: "High" if x > 80 else "Medium" if x > 70 else "Low"
            }
        },
        "leaf_spot": {
            "name": "Common Leaf Spot",
            "symptoms": [
                "Small purple spots on leaves",
                "Spots enlarge to form tan centers with purple margins",
                "Severely infected leaves may turn brown and die",
                "Can reduce photosynthesis and plant vigor"
            ],
            "causes": [
                "Fungal pathogen: Mycosphaerella fragariae",
                "Cool, wet conditions (65-75°F, 18-24°C)",
                "Splashing water spreading spores",
                "Overhead irrigation",
                "Poor air circulation"
            ],
            "prevention": [
                "Use disease-free transplants",
                "Plant resistant varieties",
                "Use drip irrigation",
                "Remove old leaves after harvest",
                "Maintain good air circulation"
            ],
            "treatment": [
                "Remove and destroy infected leaves",
                "Apply fungicides preventatively",
                "Ensure proper spacing between plants",
                "Maintain ideal pH levels",
                "Avoid overhead irrigation"
            ],
            "optimal_conditions": {
                "pH": (5.8, 6.2),
                "EC_mS_cm": (1.5, 2.0),
                "Humidity_pct": (60, 70),
                "Water_Temp_C": (18, 21)
            },
            "severity_by_param": {
                "pH": lambda x: "Medium" if x < 5.5 or x > 6.5 else "Low",
                "Humidity_pct": lambda x: "High" if x > 80 else "Medium" if x > 70 else "Low"
            }
        },
        "root_rot": {
            "name": "Root and Crown Rot",
            "symptoms": [
                "Wilting despite adequate moisture",
                "Stunted growth",
                "Brown or black roots",
                "Reddish-brown discoloration of crown",
                "Plant collapse and death"
            ],
            "causes": [
                "Fungal pathogens: Phytophthora, Pythium, Rhizoctonia species",
                "Overwatering",
                "Poor drainage",
                "Water temperatures above 24°C (75°F)",
                "Low oxygen levels in nutrient solution"
            ],
            "prevention": [
                "Use disease-free transplants",
                "Maintain proper water temperature (18-22°C)",
                "Ensure adequate oxygenation in nutrient solution",
                "Maintain EC within recommended range",
                "Disinfect hydroponic systems between crops"
            ],
            "treatment": [
                "Remove and destroy infected plants",
                "Improve oxygenation of nutrient solution",
                "Decrease water temperature to 18-20°C",
                "Apply beneficial microorganisms (Trichoderma)",
                "Adjust pH to 5.8-6.2"
            ],
            "optimal_conditions": {
                "pH": (5.8, 6.2),
                "EC_mS_cm": (1.5, 1.8),
                "Water_Temp_C": (18, 20),
                "Dissolved_Oxygen": "Above 6 mg/L"
            },
            "severity_by_param": {
                "pH": lambda x: "High" if x < 5.5 or x > 6.5 else "Medium" if x < 5.8 or x > 6.2 else "Low",
                "EC_mS_cm": lambda x: "High" if x > 2.2 else "Medium" if x > 2.0 else "Low",
                "Water_Temp_C": lambda x: "High" if x > 24 else "Medium" if x > 22 else "Low"
            }
        }
    }

def evaluate_disease_risk(ph, ec, humidity, water_temp):
    """Evaluate the risk of different diseases based on current parameters."""
    disease_info = get_disease_info()
    risk_assessment = {}
    
    for disease_id, disease in disease_info.items():
        risk_score = 0
        risk_factors = []
        
        # Check pH
        if "pH" in disease["severity_by_param"]:
            ph_severity = disease["severity_by_param"]["pH"](ph)
            if ph_severity == "High":
                risk_score += 3
                risk_factors.append(f"pH {ph} (High risk)")
            elif ph_severity == "Medium":
                risk_score += 2
                risk_factors.append(f"pH {ph} (Medium risk)")
        
        # Check EC
        if "EC_mS_cm" in disease["severity_by_param"]:
            ec_severity = disease["severity_by_param"]["EC_mS_cm"](ec)
            if ec_severity == "High":
                risk_score += 3
                risk_factors.append(f"EC {ec} mS/cm (High risk)")
            elif ec_severity == "Medium":
                risk_score += 2
                risk_factors.append(f"EC {ec} mS/cm (Medium risk)")
        
        # Check humidity
        if "Humidity_pct" in disease["severity_by_param"]:
            humidity_severity = disease["severity_by_param"]["Humidity_pct"](humidity)
            if humidity_severity == "High":
                risk_score += 3
                risk_factors.append(f"Humidity {humidity}% (High risk)")
            elif humidity_severity == "Medium":
                risk_score += 2
                risk_factors.append(f"Humidity {humidity}% (Medium risk)")
        
        # Check water temperature
        if "Water_Temp_C" in disease["severity_by_param"]:
            temp_severity = disease["severity_by_param"]["Water_Temp_C"](water_temp)
            if temp_severity == "High":
                risk_score += 3
                risk_factors.append(f"Water temp {water_temp}°C (High risk)")
            elif temp_severity == "Medium":
                risk_score += 2
                risk_factors.append(f"Water temp {water_temp}°C (Medium risk)")
        
        # Calculate risk level
        if risk_score >= 6:
            risk_level = "High"
        elif risk_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        risk_assessment[disease_id] = {
            "name": disease["name"],
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors
        }
    
    return risk_assessment

def display_disease_details(disease_id):
    """Display detailed information about a specific disease."""
    disease_info = get_disease_info()
    
    if disease_id not in disease_info:
        st.error("Disease information not found.")
        return
    
    disease = disease_info[disease_id]
    
    # Display disease information
    st.subheader(disease["name"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display image
        st.image(f"assets/diseases/{disease_id}.svg", use_column_width=True)
    
    with col2:
        # Symptoms
        st.markdown("#### Symptoms")
        for symptom in disease["symptoms"]:
            st.markdown(f"- {symptom}")
        
        # Causes
        st.markdown("#### Causes")
        for cause in disease["causes"]:
            st.markdown(f"- {cause}")
    
    # Prevention and Treatment
    prevention_col, treatment_col = st.columns(2)
    
    with prevention_col:
        st.markdown("#### Prevention")
        for item in disease["prevention"]:
            st.markdown(f"- {item}")
    
    with treatment_col:
        st.markdown("#### Treatment")
        for item in disease["treatment"]:
            st.markdown(f"- {item}")
    
    # Optimal conditions
    st.markdown("#### Optimal Conditions for Prevention")
    
    optimal_cols = st.columns(len(disease["optimal_conditions"]))
    
    for i, (param, values) in enumerate(disease["optimal_conditions"].items()):
        with optimal_cols[i]:
            if isinstance(values, tuple):
                st.metric(get_parameter_label(param), f"{values[0]} - {values[1]}")
            else:
                st.metric(get_parameter_label(param), values)

def get_parameter_label(parameter):
    """Get display label for a parameter."""
    labels = {
        "pH": "pH",
        "EC_mS_cm": "EC (mS/cm)",
        "Humidity_pct": "Humidity (%)",
        "Water_Temp_C": "Water Temp (°C)",
        "Dissolved_Oxygen": "Dissolved O₂"
    }
    return labels.get(parameter, parameter)
