"""
Stress Calculator Module
Estimates student stress based on:
  - total assignment workload
  - number of pending assignments
  - proximity of nearest exam

Returns: { level: "Low" | "Medium" | "High", score: int, reasons: [] }
"""

from datetime import datetime


def _days_until(date_str):
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - datetime.today().date()).days
    except Exception:
        return 999


def calculate_stress(assignments, exams):
    score = 0
    reasons = []

    # Factor 1: Total workload from pending assignments
    total_workload = sum(
        a["difficulty"] * a["size"]
        for a in assignments
        if _days_until(a["deadline"]) >= 0
    )
    if total_workload > 20:
        score += 3
        reasons.append("Very high total assignment workload")
    elif total_workload > 10:
        score += 2
        reasons.append("Moderate assignment workload")
    elif total_workload > 0:
        score += 1

    # Factor 2: Number of pending assignments
    pending = [a for a in assignments if _days_until(a["deadline"]) >= 0]
    if len(pending) >= 5:
        score += 2
        reasons.append(f"{len(pending)} assignments pending")
    elif len(pending) >= 3:
        score += 1

    # Factor 3: Exam proximity
    upcoming_exams = [e for e in exams if _days_until(e["exam_date"]) >= 0]
    if upcoming_exams:
        nearest = min(_days_until(e["exam_date"]) for e in upcoming_exams)
        if nearest <= 2:
            score += 3
            reasons.append("Exam in 2 days or less!")
        elif nearest <= 5:
            score += 2
            reasons.append("Exam coming up within 5 days")
        elif nearest <= 10:
            score += 1

    # Classify
    if score >= 5:
        level = "High"
    elif score >= 3:
        level = "Medium"
    else:
        level = "Low"

    return {
        "level": level,
        "score": score,
        "reasons": reasons if reasons else ["Workload is manageable"],
    }
