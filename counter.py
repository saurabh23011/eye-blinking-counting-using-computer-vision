import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture('Video.mp4')
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

# Include landmarks for both the left and right eyes
idList = [
    # Left eye landmarks
    22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243,
    # Right eye landmarks
    263, 362, 385, 387, 373, 380, 374, 386, 249, 466, 388, 390
]

ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        # Left eye landmarks for eye aspect ratio calculation
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVerLeft, _ = detector.findDistance(leftUp, leftDown)
        lengthHorLeft, _ = detector.findDistance(leftLeft, leftRight)

        # Right eye landmarks for eye aspect ratio calculation
        rightUp = face[386]
        rightDown = face[374]
        rightLeft = face[263]
        rightRight = face[362]
        lengthVerRight, _ = detector.findDistance(rightUp, rightDown)
        lengthHorRight, _ = detector.findDistance(rightLeft, rightRight)

        # Draw lines on both eyes
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 2)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 2)
        cv2.line(img, rightUp, rightDown, (0, 200, 0), 2)
        cv2.line(img, rightLeft, rightRight, (0, 200, 0), 2)

        # Calculate the eye aspect ratios
        ratioLeft = (lengthVerLeft / lengthHorLeft) * 100
        ratioRight = (lengthVerRight / lengthHorRight) * 100
        ratio = (ratioLeft + ratioRight) / 2  # Average ratio of both eyes

        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Blink detection logic
        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 200, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (50, 100),
                           colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    cv2.waitKey(25)



# this code for using live webcam 




# import cv2
# import cvzone
# from cvzone.FaceMeshModule import FaceMeshDetector
# import numpy as np

# # Initialize the webcam
# cap = cv2.VideoCapture(0)  # 0 is the default webcam
# cap.set(3, 1280)  # Set the width of the frame
# cap.set(4, 720)   # Set the height of the frame

# detector = FaceMeshDetector(maxFaces=1)

# # Include landmarks for both the left and right eyes
# leftEyeIds = [159, 23, 130, 243]
# rightEyeIds = [386, 374, 263, 362]

# # Variables for blink detection
# ratioList = []
# blinkCounter = 0
# color = (255, 0, 255)

# # Blink detection variables
# blink_detected = False
# frames_below_threshold = 0
# frames_required = 3  # Number of consecutive frames EAR should be below threshold

# # Calibration variables
# calibration_frames = 50
# open_ear_values = []
# calibrated = False
# mean_open_ear = 0
# open_threshold = 0
# close_threshold = 0

# print("Calibration started. Please keep your eyes open...")

# while True:
#     success, img = cap.read()
#     if not success:
#         break  # If the frame is not captured properly, exit the loop

#     # Flip the image horizontally for a later selfie-view display
#     img = cv2.flip(img, 1)
#     img, faces = detector.findFaceMesh(img, draw=False)

#     if faces:
#         face = faces[0]

#         # Get the eye landmarks
#         leftUp = face[159]
#         leftDown = face[23]
#         leftLeft = face[130]
#         leftRight = face[243]

#         rightUp = face[386]
#         rightDown = face[374]
#         rightLeft = face[263]
#         rightRight = face[362]

#         # Calculate distances for left eye
#         lengthVerLeft, _ = detector.findDistance(leftUp, leftDown)
#         lengthHorLeft, _ = detector.findDistance(leftLeft, leftRight)

#         # Calculate distances for right eye
#         lengthVerRight, _ = detector.findDistance(rightUp, rightDown)
#         lengthHorRight, _ = detector.findDistance(rightLeft, rightRight)

#         # Calculate the eye aspect ratios
#         ratioLeft = lengthVerLeft / lengthHorLeft
#         ratioRight = lengthVerRight / lengthHorRight
#         ratio = (ratioLeft + ratioRight) / 2  # Average ratio of both eyes

#         # Draw lines on both eyes
#         cv2.line(img, leftUp, leftDown, (0, 200, 0), 2)
#         cv2.line(img, leftLeft, leftRight, (0, 200, 0), 2)
#         cv2.line(img, rightUp, rightDown, (0, 200, 0), 2)
#         cv2.line(img, rightLeft, rightRight, (0, 200, 0), 2)

#         # Draw circles on eye landmarks
#         for id in leftEyeIds + rightEyeIds:
#             cv2.circle(img, face[id], 5, color, cv2.FILLED)

#         # Calibration
#         if not calibrated:
#             open_ear_values.append(ratio)
#             cv2.putText(img, "Calibrating... Keep your eyes open", (50, 100),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#             if len(open_ear_values) == calibration_frames:
#                 mean_open_ear = np.mean(open_ear_values)
#                 open_threshold = mean_open_ear * 0.9  # 90% of open EAR
#                 close_threshold = mean_open_ear * 0.7  # 70% of open EAR
#                 calibrated = True
#                 print("Calibration complete.")
#                 print(f"Open eye EAR: {mean_open_ear:.3f}")
#                 print(f"Blink threshold set at: {close_threshold:.3f}")
#                 print("You can start blinking now.")
#         else:
#             ratioList.append(ratio)
#             if len(ratioList) > 3:
#                 ratioList.pop(0)
#             ratioAvg = sum(ratioList) / len(ratioList)

#             # Display the EAR value
#             cv2.putText(img, f"EAR: {ratioAvg:.2f}", (50, 150),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#             # Blink detection logic
#             if ratioAvg < close_threshold:
#                 frames_below_threshold += 1
#                 if frames_below_threshold >= frames_required and not blink_detected:
#                     blinkCounter += 1
#                     blink_detected = True
#                     color = (0, 200, 0)
#                     print(f"Blink detected. Blink count: {blinkCounter}")
#             else:
#                 frames_below_threshold = 0
#                 blink_detected = False
#                 color = (255, 0, 255)

#             cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (50, 100),
#                                colorR=color)
#     else:
#         cv2.putText(img, "Face not detected", (50, 100),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     cv2.imshow("Blink Detection", img)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break  # Press 'q' to exit the loop

# cap.release()
# cv2.destroyAllWindows()