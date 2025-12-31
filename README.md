# Streakly 🧠🔥

Streakly is a habit-tracking web application built with Django.
Users can track daily habits, maintain streaks, receive book recommendations,
and use a Pomodoro timer to focus on habit-building sessions.

## Key Features
- Habit creation and daily check-ins
- Weekly habit overview and streak logic
- Personalized book recommendations
- Personal reading library with notes and ratings
- Pomodoro focus timer integrated into the dashboard

## Demo Access
The app includes a demo user to allow full access without authentication.

## Authors
- Iris Kosmerlj
- Jan Allenspach
- David Xue

## Setup (for graders / professor)

After cloning the repository, please run:

```bash
python3 manage.py migrate
python3 manage.py loaddata books/fixtures/books.json
python3 manage.py runserver
