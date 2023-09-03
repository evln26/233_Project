import cv2
from pyzbar.pyzbar import decode
import requests

TOKEN = "BBFF-HRGwpx4IeRlvLnblG1tRny0YehPjWz"
DEVICE_LABEL = "demo"
BARCODE_LABEL = "barcode"
COUNT_LABEL_PREFIX1 = "1111_count"
COUNT_LABEL_PREFIX2 = "2222_count"
COUNT_LABEL_PREFIX3 = "3333_count"
COUNT_LABEL_PREFIX4 = "4444_count"
COUNT_LABEL_PREFIX5 = "5555_count"

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (usually the laptop's built-in camera)

# Dictionary to store individual barcode counts
barcode_counts = {
    "1111": 0,
    "2222": 0,
    "3333": 0,
    "4444": 0,
    "5555": 0
}

# Function to get the current count values from Ubidots
def get_initial_counts():
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
    headers = {"X-Auth-Token": TOKEN}
    
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for barcode in barcode_counts.keys():
                count_variable_name = COUNT_LABEL_PREFIX1 if barcode == "1111" else \
                                     COUNT_LABEL_PREFIX2 if barcode == "2222" else \
                                     COUNT_LABEL_PREFIX3 if barcode == "3333" else \
                                     COUNT_LABEL_PREFIX4 if barcode == "4444" else \
                                     COUNT_LABEL_PREFIX5
                if count_variable_name in data:
                    barcode_counts[barcode] = data[count_variable_name]
                    print(f"Initial count for {count_variable_name}: {data[count_variable_name]}")
        else:
            print("Failed to get initial counts from Ubidots. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

# Get the initial counts from Ubidots
get_initial_counts()

# Function to send data to Ubidots
def send_data_to_ubidots(barcode_data):
    # Send the barcode data to the respective variable
    barcode_payload = {
        BARCODE_LABEL: barcode_data
    }

    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=barcode_payload)
        if response.status_code == 200:
            print(f"Barcode sent to Ubidots: {barcode_data}")
        else:
            print("Failed to send barcode to Ubidots. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

# Rest of the code remains the same...
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode the barcode in the frame
    barcodes = decode(frame)

    # Loop through all detected barcodes
    for barcode in barcodes:
        # Extract the data from the barcode
        barcode_data = barcode.data.decode('utf-8')
        
        # Check if the scanned barcode is one of the fixed barcodes
        if barcode_data in barcode_counts:
            # Update the count for the barcode
            barcode_counts[barcode_data] += 1
            
            # Send both barcode data and count data to Ubidots
            send_data_to_ubidots(barcode_data)

    # Display the frame with detected barcodes
    cv2.imshow('Barcode Reader', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
