import cv2
from ultralytics import YOLO
from risk_engine import calculate_risk
from database import save_event

MODEL_NAME = "yolo11n.pt"

class RiskDetector:
    def __init__(self):
        self.model = YOLO(MODEL_NAME)
        self.last_event = {}
        self.cooldown_frames = 90
        self.frame_no = 0

    def process(self, frame):
        self.frame_no += 1

        h, w = frame.shape[:2]

        # Demo restricted zone: right-middle area.
        zx1, zy1 = int(w * 0.62), int(h * 0.20)
        zx2, zy2 = int(w * 0.95), int(h * 0.85)

        cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), (0, 0, 255), 2)
        cv2.putText(frame, "RESTRICTED ZONE",
                    (zx1, max(25, zy1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

        results = self.model(frame, verbose=False)
        person_count = 0
        restricted = False

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = self.model.names[cls]

                if conf < 0.35:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if label == "person":
                    person_count += 1
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
                        restricted = True
                        box_color = (0, 0, 255)
                    else:
                        box_color = (0, 255, 0)
                else:
                    box_color = (255, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.putText(frame, f"{label} {conf:.2f}",
                            (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, box_color, 2)

        score, level, event = calculate_risk(person_count, restricted)

        if event != "Normal Activity":
            key = event
            last = self.last_event.get(key, -999999)
            if self.frame_no - last > self.cooldown_frames:
                save_event(event, score, level)
                self.last_event[key] = self.frame_no

        cv2.putText(frame, f"People: {person_count}",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, f"Risk: {level}  Score: {score}/100",
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255) if level == "HIGH" else (0,165,255), 2)

        if event != "Normal Activity":
            cv2.putText(frame, f"ALERT: {event}",
                        (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (0,0,255), 2)

        return frame, {
            "people": person_count,
            "restricted": restricted,
            "score": score,
            "level": level,
            "event": event
        }
