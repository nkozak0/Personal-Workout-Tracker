# Personal Workout Tracker

Simple Streamlit app for logging workouts and visualizing progress. The app uses
Streamlit's multipage feature to separate profile setup, workout logging and
progress visualization into dedicated pages.

## Features

- User setup storing name, rest timer, workout days, and multiple planned workouts per day with sets and reps
- Setup page provides a button to clear all saved data for a fresh start
- Daily workout logging goes set-by-set with an optional rest timer between sets
- Progress page organized by workout day with charts for each exercise, including colored rep markers and connecting lines
- Daily workout logging goes set-by-set with an optional rest timer between sets
- Progress page organized by workout day with charts for each exercise, including colored rep markers and connecting lines
- Progress page showing weight over time for each exercise

## Running
1. Install dependencies: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`

Data is stored locally in the `data` directory.
