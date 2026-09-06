from flask import Flask, render_template, Response, request, redirect, url_for, flash
import cv2
import os
import time
from detection import RiskDetector
from database import init_db, get_events, clear_events

app = Flask(__name__)
app.secret_key = "risk-surveillance-demo-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

detector = RiskDetector()
init_db()

camera = None
video_path = None
camera_stop_requested = False

def stop_camera():
    global camera, camera_stop_requested
    camera_stop_requested = True
    if camera is not None:
        try:
            camera.release()
        except Exception:
            pass
        camera = None


def frames_from_camera():
    global camera, camera_stop_requested
    camera_stop_requested = False
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera = None
        return
    while True:
        if camera_stop_requested:
            break
        ok, frame = camera.read()
        if not ok:
            break
        annotated, info = detector.process(frame)
        ok, buffer = cv2.imencode(".jpg", annotated)
        if ok:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                   buffer.tobytes() + b"\r\n")
    if camera is not None:
        try:
            camera.release()
        except Exception:
            pass
    camera = None
    camera_stop_requested = False

def frames_from_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        annotated, info = detector.process(frame)
        ok, buffer = cv2.imencode(".jpg", annotated)
        if ok:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                   buffer.tobytes() + b"\r\n")
        time.sleep(0.01)
    cap.release()

@app.route("/")
def index():
    return render_template("dashboard.html", events=get_events())

@app.route("/video_feed")
def video_feed():
    source = request.args.get("source", "camera")
    if source == "video":
        stop_camera()
        if video_path and os.path.exists(video_path):
            return Response(frames_from_video(video_path),
                            mimetype="multipart/x-mixed-replace; boundary=frame")
        flash("Please upload a video first.")
        return redirect(url_for("index"))
    if camera is not None:
        stop_camera()
    return Response(frames_from_camera(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.post("/stop_camera")
def stop_camera_route():
    stop_camera()
    flash("Camera stopped.")
    return redirect(url_for("index"))

@app.post("/upload")
def upload():
    global video_path
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("Please select a video file.")
        return redirect(url_for("index"))
    safe_name = os.path.basename(file.filename)
    video_path = os.path.join(UPLOAD_DIR, safe_name)
    file.save(video_path)
    flash("Video uploaded. Choose 'Uploaded Video' as the source.")
    return redirect(url_for("index"))

@app.post("/clear")
def clear():
    clear_events()
    flash("Event history cleared.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
