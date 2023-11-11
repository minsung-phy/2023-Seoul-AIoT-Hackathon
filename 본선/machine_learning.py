import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 가상의 데이터 생성 (실제 사용 시 현장에서 수집한 데이터로 대체)
# 여기서는 sklearn의 make_classification 함수를 사용하여 가상의 데이터셋을 생성
X, y = datasets.make_classification(n_samples=1000, n_features=20, n_redundant=0, n_informative=2, random_state=42)

# 데이터 전처리
# SVM은 특성의 스케일에 민감하므로 스케일링을 적용
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 데이터를 학습 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# SVM 분류기 생성 및 학습
clf = SVC(kernel='linear', C=1)
clf.fit(X_train, y_train)

# 예측 및 정확도 평가
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# 가상의 2D 데이터 생성
X, y = datasets.make_classification(n_samples=1000, n_features=2, n_redundant=0, n_informative=2, random_state=42)

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

clf = SVC(kernel='linear', C=1)
clf.fit(X_train, y_train)

# 결정 경계 시각화
plt.figure(figsize=(10, 7))
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='autumn')
ax = plt.gca()
xlim = ax.get_xlim()

# 결정 함수 생성
xx = np.linspace(xlim[0], xlim[1])
yy = -(clf.coef_[0][0] * xx + clf.intercept_[0]) / clf.coef_[0][1]

plt.plot(xx, yy, 'k-')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('SVM Decision Boundary')
plt.show()
