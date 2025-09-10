import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
LOG_FILE = DATA_DIR / "workout_log.csv"

DATA_DIR.mkdir(exist_ok=True)

def load_profile() -> dict:
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE) as f:
            data = json.load(f)
    else:
        data = {}

    raw_workouts = data.get("workouts", {})
    workouts: dict[str, list[dict]] = {}
    for day, w in raw_workouts.items():
        if isinstance(w, list):
            workouts[day] = w
        else:
            # backwards compatibility for old single-workout structure
            workouts[day] = [w]

    return {
        "name": data.get("name", ""),
        "workout_days": data.get("workout_days", []),
        "workouts": workouts,
        "rest_seconds": data.get("rest_seconds", 0),
    }

def save_profile(profile: dict) -> None:
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f)

def load_logs() -> pd.DataFrame:
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "exercise", "weight", "reps"])

def save_logs(df: pd.DataFrame) -> None:
    df.to_csv(LOG_FILE, index=False)
