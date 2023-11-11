import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

x = [2018, 2019, 2020, 2021, 2022]
y = [430, 504, 474, 626, 1000] # 자살 시도 횟수

plt.plot(x, y)
plt.title("최근 5년간 한강 교량 투신 자살 시도 횟수")
plt.xlabel("년도")
plt.ylabel("자살 시도 횟수")
plt.xticks(np.arange(min(x), max(x)+1, 1.0)) # x축 눈금 설정
plt.show()
