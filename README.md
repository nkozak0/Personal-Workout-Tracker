# Personal Workout Tracker

Simple Streamlit app for logging workouts and visualizing progress. The app uses
Streamlit's multipage feature to separate profile setup, workout logging and
progress visualization into dedicated pages.

## Features

- User setup storing name, workout days, and multiple planned workouts per day with sets and reps
- Daily workout logging that automatically loads today's exercises and reveals each one as you complete it
- Progress page showing weight over time for each exercise

## Running
1. Install dependencies: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`

Data is stored locally in the `data` directory.
