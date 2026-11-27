from roles import ROLES, gap, plan, readiness

def test_gap_and_readiness():
    matched, missing = gap("Data Analyst", ["SQL"])
    assert matched == ["SQL"] and "SQL" not in missing and missing[0] == "Statistics"
    assert readiness("Data Analyst", []) == 0
    assert readiness("Data Analyst", list(ROLES["Data Analyst"])) == 100

def test_plan_respects_hours():
    _, missing = gap("Backend Developer", [])
    weeks = plan("Backend Developer", missing, 20)
    assert sum(len(w) for w in weeks) == len(missing)
    assert all(sum(ROLES["Backend Developer"][s][1] for s in w) <= 20 or len(w) == 1 for w in weeks)
