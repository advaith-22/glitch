from flask import Flask, render_template, request, flash, url_for, redirect, Response, jsonify
import json
import datetime
import time
import detect
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(1)


@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():  
    detector = detect.ObjectDetection()
    cap = cv2.VideoCapture("test.mp4")

    while 1:
        im = detector.run(cap)
        if not im[1]:
            break
        else:
            im[1], buffer = cv2.imencode('.jpg', im[0])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video', methods = ['GET', 'POST'])
def video():
    print("working")
    my_id = request.form.get("#myVidPlayer")
    print(my_id)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=2248 ,debug=True, host = "0.0.0.0")