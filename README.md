# Dockerized-RTSP-Inference
This repository contains a Dockerized solution for real-time object detection and inference using RTSP streams

# Dockerized RTSP Inference

This repository contains a Dockerized solution for performing object detection inference on an RTSP video stream using YOLOv5 and Flask. The solution includes three Docker containers:

1. **RTSP Server Container**: Simulates a surveillance camera by streaming a video as an RTSP stream using the `aler9/rtsp-simple-server` image.

2. **FFmpeg Converter Container**: Converts an MP4 video file to an RTSP stream and streams it to the RTSP server container using the `ffmpeg` command.

3. **Flask App Container**: Runs a Flask web application with an endpoint for performing object detection inference on frames from the RTSP stream using YOLOv5.

## Setup

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/nourhansowar/Dockerized-RTSP-Inference.git
   ```

2. Navigate to the cloned repository directory:

  ```
  cd Dockerized-RTSP-Inference
  ```
3. Start the Docker Compose environment:

  ```
  docker-compose up --build
  ```
  This command will build and start the Docker containers defined in the docker-compose.yml file.

4. Feel free to use the generated flask endpoint.
