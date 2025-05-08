import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

# ----------------------------
# PARAMETERS (Hyperparameters)
# ----------------------------
image_size = (224, 224)      # Input image size required by MobileNetV2
batch_size = 16              # Number of images processed together per step
num_classes = 2              # 'sleeping' and 'not_sleeping'
epochs = 10                  # How many full passes over the dataset

# ----------------------------
# DATA LOADING + SCALING
# ----------------------------
# This rescales all pixel values from [0, 255] → [0, 1]
train_gen = ImageDataGenerator(rescale=1./255)
test_gen = ImageDataGenerator(rescale=1./255)

# The folder names become labels automatically
train_data = train_gen.flow_from_directory(
    "train_dataset",
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'  # Outputs one-hot encoded vectors (e.g., [1,0] or [0,1])
)

test_data = test_gen.flow_from_directory(
    "test_dataset",
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# ----------------------------
# MODEL SETUP
# ----------------------------
# Load pretrained MobileNetV2 without the classification head
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,        # Drop the original classifier
    weights='imagenet'        # Use pre-trained weights
)
base_model.trainable = False  # Freeze all layers so we don’t change them

# Add our custom classifier on top
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),  # Flattens the output while keeping spatial structure
    Dense(128, activation='relu'),  # Fully connected layer
    Dense(num_classes, activation='softmax')  # Final output layer (2 outputs)
])

# ----------------------------
# COMPILE + TRAIN
# ----------------------------
model.compile(
    optimizer=Adam(learning_rate=0.0001),  # Use Adam optimizer, slower learning
    loss='categorical_crossentropy',       # Use this for one-hot outputs
    metrics=['accuracy']
)

# Train the model
model.fit(
    train_data,
    validation_data=test_data,
    epochs=epochs
)

# Save the model to a file
model.save("sleep_classifier_model.h5")
