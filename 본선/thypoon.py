import numpy as np
import matplotlib.pyplot as plt

# 가상의 데이터 생성
hours = 24
minutes_per_hour = 60
seconds_per_minute = 60

total_seconds = hours * minutes_per_hour * seconds_per_minute

# 기본 배경 소음 (60dB ~ 90dB)으로 증가
noise = np.random.uniform(60, 90, total_seconds)

# 태풍이 영향을 미치는 시간대 (예: 12시 ~ 24시)에 추가 소음을 넣습니다.
typhoon_start = 12 * minutes_per_hour * seconds_per_minute
typhoon_end = 24 * minutes_per_hour * seconds_per_minute
typhoon_noise = np.random.uniform(10, 20, typhoon_end - typhoon_start)  # 10dB ~ 20dB의 태풍 소음 추가
noise[typhoon_start:typhoon_end] += typhoon_noise

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
plt.title('Hydrophone Detection over 24 Hours during Typhoon')
plt.legend()
plt.tight_layout()
plt.show()