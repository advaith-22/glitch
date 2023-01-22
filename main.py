from flask import Flask, render_template, request, flash, url_for, redirect, Response, jsonify
import json
import datetime
import time
import beepy
import detect
import cv2
import threading

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/vid/<id>')
def vid(id):
    return render_template('vid.html')

@app.route('/vid', methods=['GET', 'POST', 'PUT'])
def vidc():
    id = request.form.get("id")
    return redirect(f"http://localhost:2248/vid/{id}")

def gen_frames():  
    detector = detect.ObjectDetection()
    cap = cv2.VideoCapture("test1.mp4")

    while 1:
        im = detector.run(cap)
        
        if im[2]:
            def beep():
                beepy.beep(sound=1)
            thread = threading.Thread(target = beep())
            thread.start()
            thread.join()
        else:
            potholer = "False"
        if not im[1]:
            break
        else:
            im[1], buffer = cv2.imencode('.jpg', im[0])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video', methods = ['GET', 'POST'])
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=2248 ,debug=True)