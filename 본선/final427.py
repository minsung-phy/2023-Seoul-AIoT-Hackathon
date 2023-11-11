import tkinter as tk
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import cv2
from PIL import Image, ImageTk
import threading
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


class BridgeSelection:
    def __init__(self, master):
        self.master = master
        self.master.title("현재 한강의 데시벨")
        
        self.bridges = ["성산대교","양화대교","서강대교","월드컵대교", "동호대교", "잠실대교", "청담대교", "가양대교", 
                        "동작대교", "원효대교", "마포대교", "한강대교", "반포대교(잠수교)",
                        "한남대교", "성수대교", "영동대교", "잠실철교", "올림픽대교", "천호대교", "광진교"]

        rows = 5

        for idx, bridge in enumerate(self.bridges):
            btn = tk.Button(self.master, text=bridge, command=lambda b=bridge: self.open_decibel_graph(b), width=20, height=2)
            btn.grid(row=idx % rows, column=idx // rows, pady=6, padx=6)  # Note the use of grid instead of pack

    def open_decibel_graph(self, bridge):
        top = Toplevel(self.master)
        app = DecibelApp(top, bridge)
        top.title(bridge + " Decibel Monitoring")

class MenuScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("메뉴 선택")
        
        # 버튼 크기와 여백 조절
        self.btn_decibel = tk.Button(self.master, text="현재 한강의 데시벨", command=self.open_decibel_monitoring, width=30, height=2)
        self.btn_decibel.pack(pady=20, padx=20) # padx를 추가하여 좌우 여백도 조절
        
        self.btn_records = tk.Button(self.master, text="이상 감지 기록", command=self.open_anomaly_records, width=30, height=2)
        self.btn_records.pack(pady=20, padx=20) # padx를 추가하여 좌우 여백도 조절
        
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

        self.buttons = []  # 버튼을 저장할 리스트를 생성합니다.
        
        button_width = 60  # 버튼의 너비를 지정합니다.
        button_height = 3  # 버튼의 높이를 지정합니다.
        for row, record in enumerate(records):
            # lambda 함수에서는 'r=record'를 사용하여 현재 레코드에 대한 참조를 저장합니다.
            btn = tk.Button(self.master, text=record, 
                            width=button_width, height=button_height,
                            command=lambda r=record: self.show_graph_for_record(r))
            btn.grid(row=row, column=0, padx=10, pady=2)  # padx와 pady로 버튼 사이의 여백을 설정합니다.
            self.buttons.append(btn)  # 버튼을 리스트에 추가합니다.

        self.master.grid_columnconfigure(0, weight=1)  # 열 너비가 내용에 따라 조정되도록 설정합니다.


    def extract_hour_from_record(self, record):
        # 기록에서 시간 정보를 추출하는 함수
        # 예: "2023년 11월 3일 3시 25분 30초" -> 3 (시간만 반환)
        time_segment = record.split()[-3]
        return int(time_segment.replace('시', ''))

    def generate_anomaly_data(self, anomaly_hour):
        x = np.linspace(0, 24, 25)  # 24시간 데이터 생성
        y = np.random.uniform(50, 60, len(x))  # 대부분의 데이터는 50-60 dB 범위
        y[anomaly_hour] = 100
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

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.logo_image = ImageTk.PhotoImage(file="C:\\Users\ADMIN\Desktop\학교\서울시해커톤대회\image file\KakaoTalk_20231103_105035121.png")
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

        icon_image = ImageTk.PhotoImage(file="C:\\Users\ADMIN\Desktop\학교\서울시해커톤대회\image file\스크린샷 2023-11-04 014205.png")
        self.master.iconphoto(False, icon_image)

    def check_credentials(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # username: 서빙고, password: 119
        if username == '서빙고' and password == '119':
            self.master.destroy()  # 현재 로그인 창 닫기
            root = tk.Tk()
            app = MenuScreen(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Wrong username or password")

class DecibelApp:
    def __init__(self, master, bridge_name):
        self.master = master
        self.bridge_name = bridge_name
        # 각 다리에 따른 경보 발생 시점과 랜덤 값 범위
        self.bridge_alert_times = {
            "동작대교": 10,  # 10초
            "동호대교": 20,  # 20초
            "잠실대교": 13,
            "청담대교": 2,
            "가양대교": 8,
            "성산대교": 100,
            "양화대교": 100,
            "서강대교": 25,
            "월드컵대교": 100,
            "원효대교": 17,
            "반포대교(잠수교)": 30, ################################
            "마포대교": 30,
            "한강대교": 12,
            "한남대교": 15,
            "성수대교": 43,
            "영동대교": 31,
            "잠실철교": 39,
            "올림픽대교": 12,
            "천호대교": 15,
            "광진교": 22
        }
        self.bridge_db_ranges = {
            "동작대교": (60, 65),
            "동호대교": (55, 60),
            "잠실대교": (60, 63),
            "청담대교": (52, 61),
            "가양대교": (50, 61),
            "성산대교": (54, 63),
            "양화대교": (53, 62),
            "서강대교": (55, 60),
            "월드컵대교": (44, 60),
            "원효대교": (51, 60),
            "마포대교": (40, 60),
            "한강대교": (55, 58),
            "성수대교": (57, 60),
            "영동대교": (53, 60),
            "잠실철교": (55, 60),
            "올림픽대교": (55, 57),
            "천호대교": (52, 55),
            "광진교": (57, 60),
            "한남대교":(50,60),
            "반포대교(잠수교)":(52,60)
        }
        self.master.title("Decibel Monitoring")
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
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
        alert_time = self.bridge_alert_times.get(self.bridge_name, 30)  # 기본값 30초
        if elapsed_time > alert_time and len(self.time_data) > 0 and self.time_data[-1] < alert_time:
            return 100
        else:
            # 다리 이름에 따른 데시벨 범위 참조
            min_db, max_db = self.bridge_db_ranges.get(self.bridge_name, (50, 65))
            return np.random.uniform(min_db, max_db)


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
             # 영상 크기 조절
            frame = cv2.resize(frame, (int(frame.shape[1]*1.1), int(frame.shape[0]*0.5)))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            label.config(image=photo)
            label.image = photo
            top.after(delay, update_video)

        update_video()


    def show_alert(self):
        messagebox.showwarning("경보", f"{self.bridge_name}에서 데시벨이 100dB로 급격히 증가하였습니다! CCTV 영상을 송출합니다")


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

            # 경보 메시지와 동영상을 별도의 스레드에서 플레이합니다.
            def alert_and_play_video():
                self.show_alert()
                self.play_video("C:\\Users\ADMIN\Desktop\학교\서울시해커톤대회\image file\KakaoTalk_20231102_223014960.mp4")
            threading.Thread(target=alert_and_play_video).start()

        else:
            self.update_graph_color()

        if elapsed_time >= 60:
            self.reset_data()
        self.master.after(1000, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()