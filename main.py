from flask import Flask, render_template, request, flash, url_for, redirect, Response, jsonify
import json
import datetime
import time
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():  
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video', methods = ['GET', 'POST'])
def video():
    if request.method == 'POST':
        print("working")
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=2248 ,debug=True)