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
            return json.load(f)
    return {"name": "", "weekly_plan": ""}

def save_profile(profile: dict) -> None:
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f)

def load_logs() -> pd.DataFrame:
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "exercise", "weight", "reps"])

def save_logs(df: pd.DataFrame) -> None:
    df.to_csv(LOG_FILE, index=False)
