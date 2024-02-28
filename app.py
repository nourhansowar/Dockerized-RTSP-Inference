'''from flask import Flask, request, jsonify
import cv2
#from yolov5.inference import YOLOv5Inference
import torch
app = Flask(__name__)

# Initialize YOLOv5 model for inference
#yolo = YOLOv5Inference()

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture('rtsp://localhost:8554/live.stream')
@app.route('/detect', methods=['POST'])
def detect_objects():
    # Read frame from RTSP stream
    
    ret, frame = cap.read()

    #frame = cv2.imread('rtsp://localhost:8554/live.stream')

    # Perform object detection using YOLOv5
    annotated_frame = model.detect(frame)

    # Save annotated frame
    cv2.imwrite('/annotated_frames/annotated_frame.jpg', annotated_frame)

    # Return path of annotated frame in the response
    return jsonify({'annotated_frame_path': '/annotated_frames/annotated_frame.jpg'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''
    
from flask import Flask, request, jsonify
import cv2
import torch
import time
import os

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
    # Read frame from RTSP stream
    try:
        ret, frame = cap.read()
        if not ret:
            return jsonify({'error': 'Failed to read frame from stream'}), 500
    except Exception as e:
        print(f"Error reading frame: {e}")
        return jsonify({'error': 'Failed to read frame from stream'}), 500

    # Perform object detection with YOLOv5
    results = model(frame)
    #if version.startswith("0."):  # Assuming version string starts with "0." for older versions
    #results_df = results.pandas().xyxy[0]  # Access first element as DataFrame (older versions)
    #else:
    results_df = results.xyxy[0]  # Access first element directly (newer versions)



    # Draw bounding boxes
    for element in results_df:
        # Convert each element to NumPy array for easier processing
        x1, y1, x2, y2, conf, name = element.cpu().numpy()

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({conf:.2f})", (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save annotated frame to output directory
    filename = f"annotated_{time.strftime('%Y_%m_%d_%H_%M_%S')}.jpg"
    cv2.imwrite(os.path.join(output_dir, filename), frame)

    # Return path of annotated frame
    return jsonify({'annotated_frame_path': os.path.join(output_dir, filename)}), 200  # Use 200 for success

if __name__ == '__main__':
    try:
        # Initialize RTSP video capture object (replace with your stream URL)
        #cap = cv2.VideoCapture('localhost:8554/live.stream')
        cap = cv2.VideoCapture('rtsp://192.168.1.43:8554/live.stream')

        # Check if stream is opened successfully
        if not cap.isOpened():
            print('Failed to open RTSP stream.')
            exit(1)

        app.run(host='0.0.0.0', port=5000)
    finally:
        # Release video capture object
        cap.release()


