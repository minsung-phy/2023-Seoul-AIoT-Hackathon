import numpy as np
import matplotlib.pyplot as plt

# 시간 배열 생성 (0부터 1까지, 1000개의 점)
t = np.linspace(0, 1, 1000, endpoint=False)

# 2Hz의 사인 함수 (주파수 = 2)
f = 2
y = np.sin(2 * np.pi * f * t)

# 그래프 그리기
plt.plot(t, y)
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.title('2Hz sine wave graph')
plt.show()
