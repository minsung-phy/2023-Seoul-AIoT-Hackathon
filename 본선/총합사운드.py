import numpy as np
import matplotlib.pyplot as plt

# 시간 벡터 생성
t = np.linspace(0, 250, 44100 * 250 // 10)  # 250초 동안의 시간 벡터

# 사람이 떨어지는 소음 시뮬레이션
def simulate_impact_sound(t, impact_time=30.0):
    return 20 * np.exp(-((t - impact_time)**4) / (2 * (0.5**2)))

# 배가 지나가는 소음 시뮬레이션
def simulate_ship_passing_sound(t, start_time=20, duration=20, amplitude=40):
    end_time = start_time + duration
    magnitude = np.where((t >= start_time) & (t <= end_time), 1, 0)
    return amplitude * magnitude

# 비가 내리는 소음 시뮬레이션
def simulate_rain_sound(t):
    return 0.5 * np.sin(0.1 * np.pi * t)

# 자연재해 상황 소음 시뮬레이션
def simulate_disaster_sound(t, start_time=50, duration=40, amplitude=60):
    end_time = start_time + duration
    magnitude = np.where((t >= start_time) & (t <= end_time), 1, 0)
    return amplitude * magnitude

# 평상시 소음 시뮬레이션 (맑은 날의 배경소음)
def simulate_clear_day_sound(t):
    return 0.2 * np.sin(0.002 * np.pi * t)

# 평균 60dB에서의 데시벨 생성
background_noise_dB = np.ones_like(t) * 60
impact_increase_dB = simulate_impact_sound(t)
ship_passing_increase_dB = simulate_ship_passing_sound(t)
rain_increase_dB = simulate_rain_sound(t)
disaster_increase_dB = simulate_disaster_sound(t)
clear_day_increase_dB = simulate_clear_day_sound(t)

total_impact_sound_dB = background_noise_dB + impact_increase_dB + rain_increase_dB
total_ship_passing_sound_dB = background_noise_dB + ship_passing_increase_dB + rain_increase_dB
total_disaster_sound_dB = background_noise_dB + disaster_increase_dB
total_clear_day_sound_dB = background_noise_dB + clear_day_increase_dB

# 결과 시각화
plt.figure(figsize=(12, 6))
plt.plot(t, total_impact_sound_dB, label='Person Impact')
plt.plot(t, total_ship_passing_sound_dB, label='Ship Passing', linestyle='--')
plt.plot(t, total_disaster_sound_dB, label='Natural Disaster', linestyle='-.')
plt.plot(t, background_noise_dB + rain_increase_dB, label='Rain', linestyle=':')
plt.plot(t, total_clear_day_sound_dB, label='Clear Day', linestyle='-')
plt.title("Simulated Sound Level Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Level (dB)")
plt.legend()
plt.ylim(50, 150)  # y축 범위 설정
plt.tight_layout()
plt.show()
