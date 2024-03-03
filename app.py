import cv2
import torch
import time
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

# Load YOLOv5 model for inference
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Replace with your container's mounted volume path
output_dir = "output"

# Check if output directory exists, create it if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Construct the RTSP URL using the service name
    rtsp_url = 'rtsp://rtsp-server:8554/live.stream'

    # Read frame from RTSP stream
    try:
        cap = cv2.VideoCapture(rtsp_url)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return jsonify({'error': 'Failed to read frame from stream'}), 500
    except Exception as e:
        print(f"Error reading frame: {e}")
        return jsonify({'error': 'Failed to read frame from stream'}), 500

    # Perform object detection with YOLOv5
    results = model(frame)
    results_df = results.xyxy[0]  # Access first element directly

    # Draw bounding boxes
    for element in results_df:
        x1, y1, x2, y2, conf, name = element.cpu().numpy()
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({conf:.2f})", (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save annotated frame to output directory
    filename = f"annotated_{time.strftime('%Y_%m_%d_%H_%M_%S')}.jpg"
    cv2.imwrite(os.path.join(output_dir, filename), frame)

    # Return path of annotated frame
    return jsonify({'annotated_frame_path': os.path.join(output_dir, filename)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

