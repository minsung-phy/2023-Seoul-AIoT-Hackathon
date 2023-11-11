import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# 가상의 데이터 생성
hours = 24
minutes_per_hour = 60
seconds_per_minute = 60

total_seconds = hours * minutes_per_hour * seconds_per_minute

# 기본 배경 소음 (40dB ~ 60dB)
noise = np.random.uniform(40, 60, total_seconds)

# 22시 30분에 사람이 떨어지는 소리 (100dB) 가정
fall_time = 22 * minutes_per_hour * seconds_per_minute + 30 * seconds_per_minute
noise[fall_time:fall_time + 1] = 100

# 시간 배열 생성
time = np.arange(total_seconds) / (minutes_per_hour * seconds_per_minute)

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(time, noise, label='Detected Sound Level', color='blue')
plt.axvline(x=22.5, color='red', linestyle='--', label='Person Falls')
plt.xlabel('Time (hours)')
plt.ylabel('Decibel (dB)')
plt.title('Hydrophone Detection over 24 Hours')
plt.legend()
plt.tight_layout()
plt.show()
