import numpy as np
import matplotlib.pyplot as plt

# 가상의 데이터 생성
hours = 24
minutes_per_hour = 60
seconds_per_minute = 60

total_seconds = hours * minutes_per_hour * seconds_per_minute

# 기본 배경 소음 (50dB ~ 70dB)으로 변경
noise = np.random.uniform(50, 70, total_seconds)

# 비가 오는 시간대 (예: 18시 ~ 24시)에 빗방울 소음 추가
rain_start = 18 * minutes_per_hour * seconds_per_minute
rain_end = 24 * minutes_per_hour * seconds_per_minute
rain_noise = np.random.uniform(5, 10, rain_end - rain_start)  # 5dB ~ 10dB의 빗소리 추가
noise[rain_start:rain_end] += rain_noise

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
plt.title('Hydrophone Detection over 24 Hours with Rain Noise')
plt.legend()
plt.tight_layout()
plt.show()
