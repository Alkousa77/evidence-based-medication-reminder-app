# Medication Adherence App
Prototype medication adherence app developed with React Native Expo and a Python Flask backend.

## Project Structure
- backend/   Flask backend API, database, tests, seed data

- frontend-new/  React Native Expo frontend

## Prerequisites
- Python 3.13.13
- Node.js v22.19.0
- npm 10.9.3
- Expo Go app on a mobile device
- ngrok (used via npx)

**All commands below are written for Git bash terminal**

## Backend Setup
- cd backend
- python -m venv .venv
- source .venv/Scripts/activate 
- python -m pip install --upgrade pip
- pip install -r requirements.txt

# Create/reset the database:
- python create_db.py

# Run the backend:
- python run.py

# Run ngrok to expose backend to frontned
- npx ngrok http 5000

## Frontend Setup
- cd frontend-new
- npm install

# Run the frontend
- npx expo start

*type w for web*
OR
*to open the app on mobile*:
- type s to switch to expo go build
- ensure expo go app is installed
- open the phone's camera and scan QR code
- when prompted how to open the project select expo go

Notes: 
**some features dont work fully on web such as notification and datetimepicker.**

## Run Tests
- cd backend
- source .venv/Scripts/activate 
- python -m pytest app/tests/INSERT_TEST_NAME.py

## Seed Test Data
- cd backend
- source .venv/Scripts/activate 
*Risk-mode test data:*
python -m app.tests.feed_data_test
**OR**
*Non-risk test data:*
python -m app.tests.feed_data_test false

**Seed data user info**
Email: test@test.com 
Password: pass





