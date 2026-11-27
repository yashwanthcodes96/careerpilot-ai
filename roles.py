"""Role data and pure logic (no Streamlit), so it is easy to test."""
# skill: (importance 1-5, hours to reach working level)
ROLES = {
    "Data Analyst": {"SQL": (5, 20), "Excel": (3, 10), "Python": (4, 25), "Statistics": (4, 20),
                     "Tableau": (3, 12), "Data Cleaning": (3, 10), "Storytelling": (2, 8)},
    "Backend Developer": {"Python": (4, 25), "APIs": (5, 15), "SQL": (4, 18), "Git": (3, 6),
                          "Docker": (3, 10), "Testing": (4, 12), "System Design": (3, 20)},
    "Frontend Developer": {"HTML/CSS": (5, 15), "JavaScript": (5, 30), "React": (4, 25), "Git": (3, 6),
                           "Accessibility": (3, 8), "Testing": (3, 10), "Performance": (2, 10)},
    "ML Engineer": {"Python": (5, 25), "Statistics": (4, 20), "scikit-learn": (4, 15), "Deep Learning": (4, 30),
                    "SQL": (3, 15), "MLOps": (3, 20), "Math": (3, 25)},
    "Product Manager": {"User Research": (5, 12), "Roadmapping": (4, 10), "Metrics": (4, 12), "SQL": (2, 15),
                        "Communication": (5, 8), "Prioritisation": (4, 8), "Experimentation": (3, 10)},
    "UX Designer": {"Figma": (5, 15), "User Research": (5, 12), "Wireframing": (4, 10), "Prototyping": (3, 10),
                    "Visual Design": (3, 20), "Usability Testing": (4, 10), "Accessibility": (3, 8)},
}


def gap(role: str, have: list[str]):
    """Return (matched, missing); missing is sorted most important first, then quickest."""
    skills = ROLES[role]
    matched = [s for s in skills if s in have]
    missing = sorted((s for s in skills if s not in have), key=lambda s: (-skills[s][0], skills[s][1]))
    return matched, missing


def readiness(role: str, known: list[str]) -> int:
    """Importance-weighted percentage of the role's skills already covered."""
    skills = ROLES[role]
    total = sum(w for w, _ in skills.values())
    return round(100 * sum(skills[s][0] for s in known if s in skills) / total)


def plan(role: str, missing: list[str], hours_per_week: int) -> list[list[str]]:
    """Pack missing skills into weeks without exceeding the weekly hours (a big skill gets its own week)."""
    weeks, week, used = [], [], 0
    for skill in missing:
        hours = ROLES[role][skill][1]
        if week and used + hours > hours_per_week:
            weeks.append(week)
            week, used = [], 0
        week.append(skill)
        used += hours
    return weeks + ([week] if week else [])
