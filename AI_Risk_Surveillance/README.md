# AI-Based Risk & Surveillance System

A working B.Tech project using Python, Flask, OpenCV, YOLO and SQLite.

## Features
- Live webcam surveillance
- Uploaded video analysis
- YOLO object detection
- Person counting
- Demo restricted-zone detection
- Rule-based risk score from 0 to 100
- LOW / MEDIUM / HIGH risk levels
- Automatic event logging in SQLite
- Web dashboard

## Step 1: Install Python
Python 3.10+ is recommended.

## Step 2: Open this project folder
```bash
cd AI_Risk_Surveillance
```

## Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Run
```bash
python app.py
```

Open:
http://127.0.0.1:5000

## First run
Ultralytics may download the `yolo11n.pt` model automatically. Internet access is required for this first download unless you already have the model file.

## Risk rules
- 0–39: LOW
- 40–69: MEDIUM
- 70–100: HIGH
- 5+ people adds crowd risk
- 8+ people adds higher crowd risk
- Person inside the red restricted zone adds 50 points

## Notes
This is an academic safety-monitoring prototype. It detects observable events; it does not infer that a person is inherently suspicious based on appearance or identity.

## Suggested extensions
- Object tracking with persistent IDs
- Abandoned-object detection
- Fire/smoke model
- Fall/action recognition
- Login/authentication
- Analytics charts
- Email/SMS notifications
- Model evaluation with precision, recall, F1 and FPS
