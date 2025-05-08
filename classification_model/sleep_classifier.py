from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import time
import cv2

# Labels
labels = ['not sleeping', 'sleeping']

# Load model
model = load_model("sleep_classifier_model-filtered.h5")

def preprocess_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_sleep_state(img_path):
    # Load image using OpenCV instead of keras.image (so it matches webcam behavior)
    frame = cv2.imread(img_path)
    if frame is None:
        raise ValueError(f"Image not found: {img_path}")
    
    input_img = preprocess_frame(frame)
    pred = model.predict(input_img)
    predicted_class = np.argmax(pred[0])
    return labels[predicted_class]

# Example call
#result = predict_sleep_state("test_dataset/test_not_sleeping_photos/test_not_sleeping_photos_130.jpg")
#print("Prediction:", result)


def classify_from_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    print("Warming up camera...")
    time.sleep(2)

    print("Starting classification...")

    recent_predictions = []

    while True:
        time.sleep(2)
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        input_img = preprocess_frame(frame)
        pred = model.predict(input_img)
        predicted_class = np.argmax(pred[0])
        label = labels[predicted_class]

        # Add to sliding window of last 10 predictions
        recent_predictions.append(label)
        if len(recent_predictions) > 10:
            recent_predictions.pop(0)

        # Display prediction
        print("Prediction:", label)
        cv2.putText(frame, f"Prediction: {label}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Live Classification", frame)

        # Check for 9/10 "not sleeping"
        awake_count = recent_predictions.count("not sleeping")
        if awake_count >= 9:
            print("User confirmed awake. Exiting classification.")
            break

        # Allow manual quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Interrupted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    classify_from_video()

