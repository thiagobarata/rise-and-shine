import cv2
import os
import time

time.sleep(1)
print("Going to take photos in 10 seconds")
time.sleep(10)

label = "test2_not_sleeping_photos"  # Change this to "sleeping" as needed
output_dir = label
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
time.sleep(2)
if not cap.isOpened():
    print("Error: Camera not accessible")
    exit()

print(f"Starting image capture for: {label}")
count = 0
max_images = 25

while count < max_images:
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
        break

    img_path = os.path.join(output_dir, f"{label}_{count:03d}.jpg")
    cv2.imwrite(img_path, frame)
    print(f"Saved: {img_path}")
    count += 1

    cv2.imshow("Capture", frame)
    if cv2.waitKey(2000) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Done.")
