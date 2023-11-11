import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D

# 가상의 데이터 생성
fall_sound = np.random.normal(0.5, 0.1, (1000, 100))
rain_sound = np.random.normal(0.3, 0.05, (1000, 100))
typhoon_sound = np.random.normal(0.1, 0.02, (1000, 100))

X = np.vstack([fall_sound, rain_sound, typhoon_sound])
y = np.array([0] * 1000 + [1] * 1000 + [2] * 1000)  # 0: fall, 1: rain, 2: typhoon

# 데이터 섞기 및 훈련/테스트 세트 분리
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1D CNN 모델 생성
model = Sequential()
model.add(Conv1D(64, kernel_size=3, activation="relu", input_shape=(100, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(128, kernel_size=3, activation="relu"))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(3, activation="softmax"))

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# 모델 학습
model.fit(X_train[:,:,np.newaxis], y_train, epochs=10, batch_size=32, validation_split=0.1)

# 평가
accuracy = model.evaluate(X_test[:,:,np.newaxis], y_test, batch_size=32)[1]
print(f"Model Accuracy: {accuracy*100:.2f}%")
