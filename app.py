"""CareerPilot Roadmap. Run:  streamlit run app.py"""
import json

import streamlit as st

from roles import ROLES, gap, plan, readiness

st.set_page_config(page_title="CareerPilot", page_icon="🌅", layout="centered")
st.markdown("""<style>
.card{background:#fff;border:1px solid #F0D5BE;border-left:6px solid #C8553D;border-radius:14px;padding:.7rem 1rem;margin:.4rem 0}
.tag{display:inline-block;background:#FBE9D7;color:#8A3A28;border-radius:999px;padding:.1rem .7rem;margin:.15rem;font-size:.85rem}
</style>""", unsafe_allow_html=True)

st.title("🌅 CareerPilot")
st.caption("Pick a role, tick what you already know, and get a week-by-week plan to close the gap.")

t_target, t_gap, t_road = st.tabs(["1 · Target", "2 · Gap", "3 · Roadmap"])

with t_target:
    role = st.selectbox("Target role", list(ROLES), key="role")
    have = st.multiselect("Skills you already have", list(ROLES[role]), key=f"have_{role}")
    hours = st.slider("Hours you can study per week", 2, 30, 6, key="hours")

matched, missing = gap(role, have)
weeks = plan(role, missing, hours)
done = [s for s in missing if st.session_state.get(f"done_{role}_{s}")]

with t_gap:
    score = readiness(role, have + done)
    st.metric("Readiness", f"{score}%", help="Weighted by how important each skill is for the role.")
    st.progress(score / 100)
    st.markdown("**You have:** " + (" ".join(f'<span class="tag">{s}</span>' for s in matched) or "nothing ticked yet"), unsafe_allow_html=True)
    st.subheader("Biggest gaps first")
    for s in missing:
        weight, hrs = ROLES[role][s]
        st.markdown(f'<div class="card"><b>{s}</b> · importance {"★" * weight} · ~{hrs} h</div>', unsafe_allow_html=True)
    if not missing:
        st.success("No gaps left. Time to apply! 🎉")

with t_road:
    if not weeks:
        st.info("Nothing to plan: you already cover every skill for this role.")
    for n, week in enumerate(weeks, 1):
        st.markdown(f"##### Week {n} · {sum(ROLES[role][s][1] for s in week)} h")
        for s in week:
            st.checkbox(f"{s} (~{ROLES[role][s][1]} h)", key=f"done_{role}_{s}")
    if missing:
        st.progress(len(done) / len(missing), text=f"{len(done)} of {len(missing)} skills learned")
    st.download_button("Download my plan (JSON)", json.dumps({"role": role, "have": have, "weeks": weeks}, indent=2),
                       file_name="careerpilot_plan.json", mime="application/json")
