import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

class DecibelApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Decibel Monitoring")
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.alert_triggered = False
        self.reset_data()
        self.update_graph()

    def reset_data(self):
        self.start_time = time.time()
        self.decibel_data = []
        self.time_data = []
        self.alert_triggered = False
        
    def generate_decibel(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time > 40 and len(self.time_data) > 0 and self.time_data[-1] < 40:
            return 100
        else:
            return np.random.uniform(50, 65)
        
    def update_graph(self):
        decibel = self.generate_decibel()
        elapsed_time = time.time() - self.start_time
        
        self.decibel_data.append(decibel)
        self.time_data.append(elapsed_time)
        
        self.ax.clear()

        if decibel == 100 and not self.alert_triggered:
            self.alert_triggered = True
            # 그래프를 빨간색으로 변경
            self.ax.plot(self.time_data, self.decibel_data, '-o', color='r')
            self.ax.set_xlim(0, 240)
            self.ax.set_ylim(0, 110)
            self.ax.set_xlabel('Time (S)')
            self.ax.set_ylabel('Decibel')
            self.canvas.draw()
            messagebox.showwarning("경보", "데시벨이 100dB로 급격히 증가하였습니다!")
        else:
            color = 'r' if decibel == 100 else 'b'
            self.ax.plot(self.time_data, self.decibel_data, '-o', color=color)
            self.ax.set_xlim(0, 240)
            self.ax.set_ylim(0, 110)
            self.ax.set_xlabel('Time (S)')
            self.ax.set_ylabel('Decibel')
            self.canvas.draw()
            if self.alert_triggered and decibel != 100:
                self.alert_triggered = False
        
        if elapsed_time >= 240:
            self.reset_data()
        self.master.after(1000, self.update_graph)  # 1초마다 업데이트

root = tk.Tk()
app = DecibelApp(root)
root.mainloop()
