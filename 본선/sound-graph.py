import matplotlib.pyplot as plt
import numpy as np

# 시간 (0~24시)
time = list(range(25))

# 한강의 평상시 소음
normal_noise = np.random.uniform(50, 60, 25)

# 사람이 떨어진 시간 (예: 15시)
fall_time = 15
normal_noise[fall_time:fall_time+2] = np.random.uniform(80, 90, 2)

plt.figure(figsize=(10,6))
plt.plot(time, normal_noise, label='Noise Level', color='blue', marker='o')
plt.axhline(y=80, color='r', linestyle='--', label='Threshold (80 dB)')
plt.xlabel('Time (Hour)')
plt.ylabel('Noise (dB)')
plt.title('Noise Level in Han River')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

