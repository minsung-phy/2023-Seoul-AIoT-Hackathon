import tkinter as tk
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import cv2
from PIL import Image, ImageTk
import threading

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
            app = DecibelApp(root)
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

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            label.config(image=photo)
            label.image = photo
            top.update()
            time.sleep(delay / 1000.0)

        cap.release()
        top.destroy()

    def show_alert(self):
        messagebox.showwarning("경보", "데시벨이 100dB로 급격히 증가하였습니다!")

    def update_graph(self):
        decibel = self.generate_decibel()
        elapsed_time = time.time() - self.start_time

        self.decibel_data.append(decibel)
        self.time_data.append(elapsed_time)
        
        self.ax.clear()

        if decibel == 100 and not self.alert_triggered:
            self.alert_triggered = True
            self.ax.plot(self.time_data, self.decibel_data, '-o', color='r')
            self.ax.set_xlim(0, 60)
            self.ax.set_ylim(0, 110)
            self.ax.set_xlabel('Time (S)')
            self.ax.set_ylabel('Decibel')
            self.canvas.draw()

            threading.Thread(target=self.show_alert).start()  # 별도의 스레드에서 경보 메시지 출력
            self.play_video('/Users/minsung/Documents/2학년 2학기/서울 지능형 사물인터넷 해커톤/본선/DEV/IMG_0145.mp4')

        else:
            color = 'r' if decibel == 100 else 'b'
            self.ax.plot(self.time_data, self.decibel_data, '-o', color=color)
            self.ax.set_xlim(0, 60)
            self.ax.set_ylim(0, 110)
            self.ax.set_xlabel('Time (S)')
            self.ax.set_ylabel('Decibel')
            self.canvas.draw()
            if self.alert_triggered and decibel != 100:
                self.alert_triggered = False
        
        if elapsed_time >= 60:
            self.reset_data()
        self.master.after(1000, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()

root = tk.Tk()
app = DecibelApp(root)
root.mainloop()
