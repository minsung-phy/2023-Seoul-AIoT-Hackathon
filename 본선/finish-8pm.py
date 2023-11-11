import tkinter as tk
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import cv2
from PIL import Image, ImageTk
import threading
from matplotlib import rc

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

class BridgeSelection:
    def __init__(self, master, clear_master_func):
        self.master = master
        self.master.title("Bridge Selection")
        self.clear_master_func = clear_master_func
        
        self.bridges = ["동작대교", "동호대교", "잠실철교", "청담대교", "가양대교", "성산대교", "양화대교", 
                        "서강대교", "월드컵대교", "원효대교", "마포대교", "한강대교", "반포대교(잠수교)",
                        "한남대교", "성수대교", "영동대교", "잠실대교", "올림픽대교", "천호대교", "광진교"]

        rows = 5
        cols = 4

        for idx, bridge in enumerate(self.bridges):
            btn = tk.Button(self.master, text=bridge, command=lambda b=bridge: self.open_decibel_graph(b), width=20, height=2)
            btn.grid(row=idx % rows, column=idx // rows, pady=5, padx=5)  # Note the use of grid instead of pack

        self.back_button = tk.Button(self.master, text="뒤로", command=self.goBack, width=20, height=2)
        self.back_button.grid(row=rows, columnspan=cols, pady=20)


    def goBack(self):
        self.clear_master_func(self.master)
        MenuScreen(self.master)

    def open_decibel_graph(self, bridge):
        self.clear_master(self.master)
        app = DecibelApp(self.master, self.clear_master)
        self.master.title(bridge + " Decibel Monitoring")

    def clear_master(self, master):
        for widget in master.winfo_children():
            widget.destroy()

class MenuScreen:
    def __init__(self, master):
        self.clear_master(master)
        self.master = master
        self.master.title("Menu Selection")
        
        # 버튼 크기와 여백 조절
        self.btn_decibel = tk.Button(self.master, text="현재 한강의 데시벨", command=self.open_decibel_monitoring, width=30, height=2)
        self.btn_decibel.pack(pady=20, padx=20) # padx를 추가하여 좌우 여백도 조절
        
        self.btn_records = tk.Button(self.master, text="이상 감지 기록", command=self.open_anomaly_records, width=30, height=2)
        self.btn_records.pack(pady=20, padx=20) # padx를 추가하여 좌우 여백도 조절

    def clear_master(self, master):
        # 모든 위젯 제거
        for widget in master.winfo_children():
            widget.destroy()

    def open_decibel_monitoring(self):
        self.clear_master(self.master)
        app = BridgeSelection(self.master, self.clear_master)

    def open_anomaly_records(self):
        self.clear_master(self.master)
        app = AnomalyRecordsApp(self.master, self.clear_master)

class AnomalyRecordsApp:
    def __init__(self, master, clear_master_func):
        self.master = master
        self.master.title("이상 감지 기록")
        self.clear_master_func = clear_master_func
        
        records = [
            "반포대교 12번 : 2023년 11월 3일 3시 25분 30초",
            "한강대교 7번  : 2023년 11월 3일 5시 22분 17초",
            "한남대교 2번  : 2023년 11월 3일 8시 23분 22초",
            "마포대교 4번  : 2023년 11월 3일 11시 25분 09초", 
            "동작대교 1번  : 2023년 11월 3일 13시 20분 00초", 
            "동호대교 11번 : 2023년 11월 3일 17시 21분 19초",    
            "성산대교 9번  : 2023년 11월 3일 18시 01분 23초", 
            "영동대교 3번  : 2023년 11월 3일 19시 03분 32초", 
            "성수대교 1번  : 2023년 11월 3일 21시 48분 01초", 
            "원효대교 12번  : 2023년 11월 3일 23시 12분 08초"       
        ]
        
        for record in records:
            btn = tk.Button(self.master, text=record, command=lambda r=record: self.show_graph_for_record(r))
            btn.pack(pady=10)

        self.back_button = tk.Button(self.master, text="뒤로", command=self.goBack)
        self.back_button.pack(pady=20)

    def extract_hour_from_record(self, record):
        # 기록에서 시간 정보를 추출하는 함수
        # 예: "2023년 11월 3일 3시 25분 30초" -> 3 (시간만 반환)
        time_segment = record.split()[-3]
        return int(time_segment.replace('시', ''))

    def generate_anomaly_data(self, anomaly_hour):
        x = np.linspace(0, 24, 25)  # 24시간 데이터 생성
        y = np.random.uniform(50, 60, len(x))  # 대부분의 데이터는 50-60 dB 범위
        y[anomaly_hour] = 100  # 기록된 시간에 100dB로 설정
        return x, y

    def show_graph_for_record(self, record):
        top = Toplevel(self.master)
        top.title(f"{record}")

        anomaly_hour = self.extract_hour_from_record(record)
        x, y = self.generate_anomaly_data(anomaly_hour)
        
        fig, ax = plt.subplots()
        ax.plot(x, y, '-o')
        ax.set_title(f"{record}")
        ax.set_xlabel('Time (Hours)')
        ax.set_ylabel('Decibel')
        ax.set_ylim(0, 110)
        ax.set_xlim(0, 24)
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def goBack(self):
        self.clear_master_func(self.master)
        MenuScreen(self.master)
        
class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.logo_image = ImageTk.PhotoImage(file="/Users/minsung/Documents/2학년 2학기/서울 지능형 사물인터넷 해커톤/본선/DEV/HRRS-logo.png")
        self.logo_label = tk.Label(self.master, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, columnspan=2)

        self.label_username = tk.Label(self.master, text="Username")
        self.label_password = tk.Label(self.master, text="Password")

        self.entry_username = tk.Entry(self.master)
        self.entry_password = tk.Entry(self.master, show="*")

        self.label_username.grid(row=1, column=0)
        self.label_password.grid(row=2, column=0)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.login_button = tk.Button(self.master, text="Login", command=self.check_credentials)
        self.login_button.grid(row=3, column=0, columnspan=2)

        icon_image = ImageTk.PhotoImage(file="/Users/minsung/Documents/2학년 2학기/서울 지능형 사물인터넷 해커톤/본선/Dev/HRRS-logo-icon.png")
        self.master.iconphoto(False, icon_image)

    def check_credentials(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == 'admin' and password == 'password':
            self.clear_master(self.master)
            app = MenuScreen(self.master)
        else:
            messagebox.showerror("Error", "Wrong username or password")

    def clear_master(self, master):
        # 모든 위젯 제거
        for widget in master.winfo_children():
            widget.destroy()

class DecibelApp:
    def __init__(self, master, clear_master_func):
        self.master = master
        self.master.title("Decibel Monitoring")

        self.fig, self.ax = plt.subplots(3, 4, figsize=(15, 12))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.back_button = tk.Button(self.master, text="Back", command=self.goBack)
        self.back_button.pack(pady=20)
        
        self.alert_triggered = [False for _ in range(12)]
        self.reset_data()
        self.update_graph()
    
    def goBack(self):
        self.clear_master(self.master)
        BridgeSelection(self.master, self.clear_master)

    def reset_data(self):
        self.start_time = time.time()
        self.decibel_data = [[] for _ in range(12)]
        self.time_data = [[] for _ in range(12)]

    def generate_decibel(self, idx):
        if idx == 6:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 30 and len(self.time_data[idx]) > 0 and self.time_data[idx][-1] < 30:
                return 100
            else:
                return np.random.uniform(50, 65)
        else:
            return np.random.uniform(50, 60)

    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        top = Toplevel(self.master)
        label = tk.Label(top)
        label.pack()

        frames_per_second = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / frames_per_second)

        def update_video():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                top.destroy()
                return
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            label.config(image=photo)
            label.image = photo
            top.after(delay, update_video)

        update_video()


    def show_alert(self):
        messagebox.showwarning("경보", "7번 Hydrophone에서 데시벨이 100dB로 급격히 증가하였습니다!")

    def update_graph_color(self, idx, color='b'):
        ax = self.ax[idx // 4, idx % 4]
        ax.clear()
        ax.plot(self.time_data[idx], self.decibel_data[idx], '-o', color=color)
        ax.set_xlim(0, 60)
        ax.set_ylim(0, 110)
        
        # Set the title inside the plot at the top center.
        # We remove the previous set_title method and replace it with ax.text method.
        x_center = (ax.get_xlim()[1] - ax.get_xlim()[0]) / 2
        ax.text(x_center, 105, f"Graph {idx + 1}", ha='center', va='center') # Adjust y-value (105) as per requirement
        
        ax.set_xlabel('Time (S)')
        ax.set_ylabel('Decibel')
        self.canvas.draw()

    def update_graph(self):
        for idx in range(12):
            decibel = self.generate_decibel(idx)
            elapsed_time = time.time() - self.start_time

            self.decibel_data[idx].append(decibel)
            self.time_data[idx].append(elapsed_time)

            if idx == 6 and decibel == 100 and not self.alert_triggered[idx]:
                self.alert_triggered[idx] = True
                self.update_graph_color(idx, 'red')

                def alert_and_play_video():
                    self.show_alert()
                    self.play_video('/Users/minsung/Documents/2학년 2학기/서울 지능형 사물인터넷 해커톤/본선/DEV/cctv.mp4')

                threading.Thread(target=alert_and_play_video).start()
                threading.Thread(target=lambda: (time.sleep(4), self.update_graph_color(idx, 'blue'))).start()
            else:
                self.update_graph_color(idx)

        if elapsed_time >= 60:
            self.reset_data()
        self.master.after(1000, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()