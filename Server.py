from flask import Flask, Response
import cv2
import numpy as np
import pyautogui

app = Flask(__name__)
# Set the desired screen size (width, height)
SCREEN_WIDTH = 1850
SCREEN_HEIGHT = 900

def generate_frames():
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()  # Convert to bytes

        # Yield the output in the format expected by the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """<h1 style="color:red;">&#x2022;Live</h1>
    <img src='/video_feed' width={} height={}>""".format(SCREEN_WIDTH, SCREEN_HEIGHT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on all interfaces
    