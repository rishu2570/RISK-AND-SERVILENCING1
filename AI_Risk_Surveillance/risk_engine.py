def calculate_risk(person_count, restricted):
    score = 0
    reasons = []

    if person_count >= 8:
        score += 50
        reasons.append("Large Crowd")
    elif person_count >= 5:
        score += 40
        reasons.append("Crowd")
    elif person_count >= 3:
        score += 20

    if restricted:
        score += 50
        reasons.append("Restricted Area Entry")

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    event = " + ".join(reasons) if reasons else "Normal Activity"
    return score, level, event
