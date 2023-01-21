import torch
import numpy as np
import cv2
import time
from threading import Thread
from queue import Queue


class ObjectDetection:
    def __init__(self):
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nDevice Used:",self.device)



    def load_model(self):
        model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'model.pt')
        model.conf = 0.4

        return model


    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
     
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        if len(cord.tolist()) != 0:
            self.potholedetected = True
        return labels, cord


    def class_to_label(self, x):
        return self.classes[int(x)]


    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame


    def run(self, cap):
        start_time = time.perf_counter()
        ret, frame = cap.read()
        results = self.score_frame(frame)
        frame = self.plot_boxes(results, frame)
        end_time = time.perf_counter()
        fps = 1 / np.round(end_time - start_time, 3)
        return [frame, ret, self.potholedetected]