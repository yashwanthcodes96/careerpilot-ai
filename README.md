# CareerPilot Roadmap (Sunrise edition)
A different take on CareerPilot: instead of an agent that hunts jobs, this is a **skill-gap coach**.
Pick a target role, tick the skills you have, and get a gap analysis plus a week-by-week study plan with a progress tracker.

- **Theme:** warm cream and terracotta, serif type (see `.streamlit/config.toml`)
- **Aspect:** learning and readiness, not applications. No API keys, no database, works offline.
- **Files:** `roles.py` holds the data and pure logic, `app.py` is the Streamlit UI.

```bash
pip install -r requirements.txt
streamlit run app.py
```
Add a role by adding an entry to `ROLES` in `roles.py`: `skill: (importance 1-5, hours)`.
