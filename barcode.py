import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (usually the laptop's built-in camera)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode the barcode in the frame
    barcodes = decode(frame)

    # Loop through all detected barcodes
    for barcode in barcodes:
        # Extract the data from the barcode
        barcode_data = barcode.data.decode('utf-8')

        # Store the barcode data in a variable
        detected_barcode = barcode_data

        # Convert the barcode's corner points to a NumPy array
        points = np.array(barcode.polygon, dtype=np.int32)

        # Draw a rectangle around the barcode
        cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the barcode data
        cv2.putText(frame, barcode_data, (points[0][0], points[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Print the detected barcode data to the terminal
        print("Detected Barcode:", detected_barcode)

    # Display the frame with detected barcodes
    cv2.imshow('Barcode Reader', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
