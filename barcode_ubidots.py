import cv2
from pyzbar.pyzbar import decode
import requests

TOKEN = "BBFF-HRGwpx4IeRlvLnblG1tRny0YehPjWz"
DEVICE_LABEL = "demo"
BARCODE_LABEL = "barcode"

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (usually the laptop's built-in camera)

def send_barcode_to_ubidots(barcode_data):
    payload = {
        BARCODE_LABEL: barcode_data
    }

    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Barcode sent to Ubidots: {barcode_data}")
        else:
            print("Failed to send barcode to Ubidots. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode the barcode in the frame
    barcodes = decode(frame)

    # Loop through all detected barcodes
    for barcode in barcodes:
        # Extract the data from the barcode
        barcode_data = barcode.data.decode('utf-8')

        # Send the detected barcode data to Ubidots
        send_barcode_to_ubidots(barcode_data)

    # Display the frame with detected barcodes
    cv2.imshow('Barcode Reader', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
