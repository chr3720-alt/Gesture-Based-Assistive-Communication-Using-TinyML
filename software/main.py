import numpy as np

X = []
y = []

def generate_sequence(label):
    sequence = []

    for t in range(50):  # 50 time steps
        if label == 0:  # WAVE
            ax = np.sin(t/5) + np.random.normal(0, 0.1)
            ay = np.cos(t/5) + np.random.normal(0, 0.1)
            az = 9.8 + np.random.normal(0, 0.2)
            gx = np.sin(t/3)
            gy = np.cos(t/3)
            gz = np.random.normal(0, 0.1)

        elif label == 1:  # HELP
            ax = np.random.normal(1.5, 0.3)
            ay = np.random.normal(1.2, 0.3)
            az = 9.5 + np.random.normal(0, 0.2)
            gx = np.random.normal(2.0, 0.3)
            gy = np.random.normal(1.5, 0.3)
            gz = np.random.normal(0.5, 0.2)

        elif label == 2:  # STOP
            ax = np.random.normal(0, 0.05)
            ay = np.random.normal(0, 0.05)
            az = 9.8
            gx = 0
            gy = 0
            gz = 0

        elif label == 3:  # WATER
            ax = np.sin(t/6) + 0.5
            ay = np.cos(t/6) + 0.3
            az = 9.6 + np.random.normal(0, 0.2)
            gx = np.random.normal(1.5, 0.2)
            gy = np.random.normal(0.8, 0.2)
            gz = np.random.normal(0.3, 0.1)

        sequence.append([ax, ay, az, gx, gy, gz])

    return sequence


# Generate dataset
for label in range(4):  # 4 gestures
    for _ in range(200):  # 200 samples each
        X.append(generate_sequence(label))
        y.append(label)

X = np.array(X)
y = np.array(y)

print(X.shape)  # (800, 50, 6)

from sklearn.model_selection import train_test_split
import tensorflow as tf

# Normalize data (important for neural networks)
X = X / np.max(np.abs(X), axis=(0,1))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, 3, activation='relu', input_shape=(50,6)),
    tf.keras.layers.MaxPooling1D(2),

    tf.keras.layers.Conv1D(64, 3, activation='relu'),
    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))


# 👉 ADD THIS BELOW 👇

def predict_gesture(sample):
    sample = sample.reshape(1, 50, 6)
    pred = model.predict(sample)
    return np.argmax(pred)

labels = ["WAVE", "HELP", "STOP", "WATER"]

sample = X_test[0]
prediction = predict_gesture(sample)

print("Predicted:", labels[prediction])
print("Actual:", labels[y_test[0]])

model.save("gesture_model.keras")