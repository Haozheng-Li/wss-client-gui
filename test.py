# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/26
#
# A PyQt-based GUI library for WSS projects
# ============================================
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Copyright (c) 2023 Haozheng Li. All rights reserved.


import cv2
import imutils
import numpy as np

def detect_human(frame, net):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])

            if class_id == 15:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    return frame

def main():
    prototxt = 'wss/models/deploy.prototxt'
    model = 'wss/models/mobilenet_iter_73000.caffemodel'
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = imutils.resize(frame, width=500)

        fg_mask = bg_subtractor.apply(frame)

        _, fg_mask_bin = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        fg_mask_bin = cv2.erode(fg_mask_bin, kernel, iterations=1)
        fg_mask_bin = cv2.dilate(fg_mask_bin, kernel, iterations=2)

        contours, _ = cv2.findContours(fg_mask_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) < 500:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            roi = frame[y:y+h, x:x+w]
            roi = detect_human(roi, net)
            frame[y:y+h, x:x+w] = roi

        cv2.imshow("Intruder Detection", frame)

        key = cv2.waitKey(1) & 0xff
        if key == 27:  # Esc
            break


if __name__ == '__main__':
    main()