def calculate_risk(rainfall, slope, soil_moisture, vegetation, river_distance):

    risk_score = 0

    # Rainfall
    if rainfall > 200:
        risk_score += 30
    elif rainfall > 100:
        risk_score += 15

    # Slope
    if slope > 45:
        risk_score += 30
    elif slope > 30:
        risk_score += 15

    # Soil moisture
    if soil_moisture > 70:
        risk_score += 20
    elif soil_moisture > 50:
        risk_score += 10

    # Vegetation
    if vegetation < 30:
        risk_score += 15

    # Distance from river
    if river_distance < 100:
        risk_score += 10

    # Maximum score = 100
    risk_score = min(risk_score, 100)

    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH 🔴"
    elif risk_score >= 40:
        risk_level = "MODERATE 🟠"
    else:
        risk_level = "LOW 🟢"

    return risk_score, risk_level