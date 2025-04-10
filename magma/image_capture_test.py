import cv2

# Replace 'your_stream_url' with the actual URL of your MJPG stream
stream_url = 'https://robotcopilotstream.smtoctolabs.com/mjpg/video.mjpg?videocodec=h264&resolution=320x240'

# Initialize the VideoCapture object with the stream URL
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
else:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the resulting frame
        cv2.imshow('MJPG Stream', frame)

        # Press 'q' to exit the video stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
