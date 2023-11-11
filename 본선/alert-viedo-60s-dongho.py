import tkinter as tk
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import cv2
from PIL import Image, ImageTk
import threading

class BridgeSelection:
    def __init__(self, master):
        self.master = master
        self.master.title("Bridge Selection")
        
        self.btn_dongjak = tk.Button(self.master, text="동작대교", command=self.open_decibel_graph)
        self.btn_dongjak.pack(pady=20)
        
    def open_decibel_graph(self):
        top = Toplevel(self.master)
        app = DecibelApp(top)
    
class MenuScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Selection")
        
        self.btn_decibel = tk.Button(self.master, text="현재 한강의 데시벨", command=self.open_decibel_monitoring)
        self.btn_decibel.pack(pady=20)
        
        self.btn_records = tk.Button(self.master, text="이상 감지 기록", command=self.open_anomaly_records)
        self.btn_records.pack(pady=20)
        
    def open_decibel_monitoring(self):
        top = Toplevel(self.master)
        app = BridgeSelection(top)

    # Corrected the function name here
    def open_anomaly_records(self):
        top = Toplevel(self.master)  
        app = AnomalyRecordsApp(top)

class AnomalyRecordsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("이상 감지 기록")
        
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
            tk.Label(self.master, text=record).pack(pady=10)

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

    def check_credentials(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # 예시로 'admin'과 'password'를 올바른 아이디와 비밀번호로 설정
        if username == 'admin' and password == 'password':
            self.master.destroy()  # 현재 로그인 창 닫기
            root = tk.Tk()
            app = MenuScreen(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Wrong username or password")

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
        if elapsed_time > 30 and len(self.time_data) > 0 and self.time_data[-1] < 30:
            return 100
        else:
            return np.random.uniform(50, 65)

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
        messagebox.showwarning("경보", "데시벨이 100dB로 급격히 증가하였습니다!")

    def update_graph_color(self, color='b'):
        self.ax.clear()
        self.ax.plot(self.time_data, self.decibel_data, '-o', color=color)
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 110)
        self.ax.set_xlabel('Time (S)')
        self.ax.set_ylabel('Decibel')
        self.canvas.draw()

    def update_graph(self):
        decibel = self.generate_decibel()
        elapsed_time = time.time() - self.start_time

        self.decibel_data.append(decibel)
        self.time_data.append(elapsed_time)
        
        if decibel == 100 and not self.alert_triggered:
            self.alert_triggered = True

            # 그래프를 빨간색으로 변경합니다.
            self.update_graph_color('red')

            # 경보 메시지와 동영상을 별도의 스레드에서 플레이합니다.
            def alert_and_play_video():
                self.show_alert()
                self.play_video('/Users/minsung/Documents/2학년 2학기/서울 지능형 사물인터넷 해커톤/본선/DEV/cctv.mp4')

            threading.Thread(target=alert_and_play_video).start()

            # 별도의 스레드에서 4초 후에 그래프 색상을 파란색으로 변경합니다.
            threading.Thread(target=lambda: (time.sleep(4), self.update_graph_color('blue'))).start()
        else:
            self.update_graph_color()

        if elapsed_time >= 60:
            self.reset_data()
        self.master.after(1000, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()