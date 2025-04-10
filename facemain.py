import cv2
import numpy as np
import os 
from gaze_tracking import GazeTracking
from plyer import notification
import time
import streamlit as st

def run_facemain(waktu_ujian):
    cheat_report = []
    # Load YOLO model and configurations
    yolo_net = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")
    layer_names = yolo_net.getUnconnectedOutLayersNames()
    with open("models/classes.TXT", "r") as f:
        classes = f.read().strip().split("\n")

    gaze = GazeTracking()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0
    names = ['None', 'Raff', 'Dyah', 'Yusuf'] 
    name_ = names[id]
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    # Initialize gaze timeout variables
    last_gaze_on_screen_time = time.time()  # Initialize the time when gaze was last on the screen
    gaze_timeout_threshold = 15  # Set the threshold for gaze timeout
    frame_placeholder = st.empty()
    placeholder = st.empty()

    secs = waktu_ujian # Exam Time in Secs
    mm, ss = 0, 0 # Initiate minute and seconds
    notification_title = "" # Initiate nofification person

    while True:
        ret, img =cam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(img)
        img = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Berkedip"
            cheat_report.append([name_, f"{mm:02d}:{ss:02d}", text, notification_title, img, ""]) # append time, look cheat, person cheat, and image
        elif gaze.is_right():
            text = "Lihat ke Kanan"
            cheat_report.append([name_, f"{mm:02d}:{ss:02d}", text, notification_title, img, ""])
        elif gaze.is_left():
            text = "Lihat ke Kiri"
            cheat_report.append([name_, f"{mm:02d}:{ss:02d}", text, notification_title, img, ""])
        elif gaze.is_center():
            text = "Lihat ke Tengah"
            cheat_report.append([name_, f"{mm:02d}:{ss:02d}", text, notification_title, img, ""])
        
        with placeholder.container():
            st.subheader(f"Status Saat Ini: {text}")
            mm, ss = secs//60, secs%60
            st.subheader(f"Waktu Ujian Tersisa: {mm:02d}:{ss:02d}")
            secs = secs - 1 
        
        if secs == -1:
            return cheat_report # return cheat report when time finished


        #cv2.putText(img, text, (320, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(img, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)
        cv2.putText(img, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)

        # img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less them 100 ==> "0" : perfect match 
            if (confidence < 100):
                id = names[id]
                name_ = id
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                name_ = id
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(
                        img, 
                        str(id), 
                        (x+5,y-5), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                    )
            cv2.putText(
                        img, 
                        str(confidence), 
                        (x+5,y+h-5), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                    )
        
        # Detect objects using YOLO
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(blob)
        outs = yolo_net.forward(layer_names)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5 and class_id == 0 or class_id == 67:  # Class ID 0 corresponds to person in COCO dataset
                    # Object detected is a person
                    x, y, w, h = detection[0:4] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
                    x = int(x - w / 2)
                    y = int(y - h / 2)
                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                

        # Non-maxima suppression to remove duplicate detections
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Inisialisasi number of person detected
        num_persons = 0
        
        for i in range(len(boxes)):
            if i in indices:
                x, y, w, h = boxes[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if class_ids[i] == 0:
                    cv2.putText(img, 'Person', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    num_persons += 1

                elif class_ids[i] == 67:
                    cv2.putText(img, 'Cell Phone', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # Notify that a phone is detected
                    print('Mobile Phone detected!')
                    notification_title = 'Mobile Phone detected'
                    notification_text = 'The device (mobile phone) has been detected, please turn off your mobile phone immediately.'
                    notification.notify(
                        title=notification_title,
                        message=notification_text,
                        timeout=5  # Notification will disappear after 5 seconds
                    )
        # Check if gaze is on the screen
        if gaze.is_center():
            last_gaze_on_screen_time = time.time()  # Update the last time gaze was on the screen
        
        # Calculate time since last gaze on the screen
        time_since_last_gaze = time.time() - last_gaze_on_screen_time
        
        # Display a warning if time exceeds the threshold
        if time_since_last_gaze > gaze_timeout_threshold:
            cv2.putText(img, 'You are not focused on the screen', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Notify that the user is not focused on the screen
            # notification_title = 'Not Focused on Screen'
            # notification_text = 'You are not focusing on the screen, please keep your eyes focused on the screen.'
            # notification.notify(
            #     title=notification_title,
            #     message=notification_text,
            #     timeout=30
            # )

        # Display a message based on the number of detected persons
        if num_persons == 0:
            cv2.putText(img, 'No person detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            notification_title = 'No person detected'
        elif num_persons == 1:
            cv2.putText(img, 'One person detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            notification_title = 'One person detected'
        else:
            cv2.putText(img, f'{num_persons} persons detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Notify when more one person detected
            print('More then one person detected')
            notification_text = f'There are {num_persons} persons detected.'
            notification_title = 'Multiple Persons Detected'
            notification.notify(
                title=notification_title,
                message=notification_text,
                timeout=5  # Notification will disappear after 5 seconds
            )

        if ret == False:
            break

        frame_placeholder.image(img,channels="RGB")
        # cv2.imshow('camera', img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    return cheat_report