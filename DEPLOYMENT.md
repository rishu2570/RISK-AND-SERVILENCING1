# Deployment Guide - Render

## Overview
This AI-Based Risk & Surveillance System is configured for deployment on **Render**.

## Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)

## Step-by-Step Deployment

### 1. Connect Repository to Render
1. Go to [https://render.com](https://render.com)
2. Sign in with your GitHub account
3. Click **New +** → **Web Service**
4. Select **Build and deploy from a Git repository**
5. Search for `rishu2570/RISK-AND-SERVILENCING1` and connect it

### 2. Configure Deployment
- **Name**: `ai-risk-surveillance` (or your preferred name)
- **Environment**: Docker
- **Region**: Oregon (or your preferred region)
- **Plan**: Free
- **Branch**: main
- **Dockerfile**: `./Dockerfile`
- **Build Command**: (leave empty - uses Dockerfile)
- **Start Command**: (leave empty - uses Dockerfile CMD)

### 3. Add Environment Variables (Optional)
In the Render dashboard under **Environment**:
```
PORT=10000
PYTHONUNBUFFERED=1
```

### 4. Deploy
Click **Deploy** and wait for the build to complete (~3-5 minutes).

## Features Available After Deployment

✅ **Uploaded Video Analysis** - Upload videos for risk analysis  
✅ **Web Dashboard** - View detection results and event logs  
✅ **SQLite Event Logging** - Automatic event recording  
✅ **YOLO Object Detection** - Person counting and detection  
✅ **Risk Scoring** - LOW/MEDIUM/HIGH risk levels  

⚠️ **Camera Access** - Not available on Render (no hardware camera)

## Access Your Application
Once deployed, Render will provide a URL like:
```
https://ai-risk-surveillance-xxxxx.onrender.com
```

Use this URL to access your dashboard.

## Troubleshooting

### Service won't build
- Check Build Logs in Render dashboard
- Ensure all Python dependencies are in `requirements.txt`
- Verify `Dockerfile` syntax

### Service crashes on startup
- Check Logs in Render dashboard
- Ensure `app.run(host='0.0.0.0', port=port)` is in `app.py`
- Verify database initialization doesn't require writable permissions

### Slow startup
- Free tier has limited resources
- YOLO model downloads on first run (~50MB)
- Subsequent runs will be faster

## File Uploads
Video uploads are stored in `/app/uploads/` which is ephemeral on Render.
For persistent storage, integrate with Render Disks or external cloud storage.

## Notes
- The application uses SQLite database stored on the container filesystem
- Database will reset when the service restarts (use PostgreSQL add-on for persistence)
- Free tier services auto-pause after 15 minutes of inactivity

## Need Help?
- Render Docs: https://docs.render.com
- GitHub Issues: Create an issue in the repository
