import os
import sys
import cv2
import copy
import json
import numpy as np

import time
import shutil
from datetime import datetime

from multiprocessing import Process

from email_sender import send_email


def run(instant, frequency, sender_email, sender_password, receiver_email):
    while True:
        ret, frame = capture.read()
        image = copy.deepcopy(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        captured_face = None

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            captured_face = image

        cv2.imshow('Face detector', frame)

        if captured_face is not None:
            instant = send_notification(captured_face, instant, frequency, sender_email, sender_password, receiver_email)
            captured_face = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def send_notification(frame, instant, frequency, sender_email, sender_password, receiver_email):
    if instant < 0 or time.time() - instant >= 60 * frequency:

        instant = time.time()

        print 'Face detected. Sending notification.'

        if not os.path.exists('history'):
            os.makedirs('history')

        filename = 'history/{}.jpg'.format(
            datetime.now().strftime('%d-%m-%Y_%H-%M-%S'))

        cv2.imwrite(filename, frame)

        process = Process(target=send_email, args=(sender_email, sender_password, receiver_email))
        process.start()

        return instant
    return instant


if __name__ == '__main__':
    if os.path.exists('history'):
        shutil.rmtree('history')

    frequency = 3  # minutes
    instant = -1

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    capture = cv2.VideoCapture(0)

    if not os.path.isfile('config.json'):
        print 'Configuration file not found.'
    else:
        with open('config.json') as configuration:
            parameters = json.load(configuration)

            sender_email = parameters.get('sender_email')
            sender_password = parameters.get('sender_password')
            receiver_email = parameters.get('receiver_email')

            run(instant, frequency, sender_email,
                sender_password, receiver_email)
