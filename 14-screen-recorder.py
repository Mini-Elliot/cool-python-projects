import pyautogui
import cv2
import numpy as np

resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"X264")
filename = "Recording.avi"
fps = "30.0"
out = cv2.VideoWriter(filename, codec, fps, resolution)

while True:
    img = pyautogui.screenshot()

    # convert the screenshots into numpy array
    frame = np.array(img)

    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Blue, Green)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write it to output file
    out.write(frame)

    # Optional: Display the recording screen
    cv2.imshow("Live", frame)

    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break
# Release the video writer
out.release()

cv2.DestroyAllWindows()
