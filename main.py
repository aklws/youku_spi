from gui.main_window import Application
from logic.youku_downloader import YoukuVideoDownloader
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Youku Video Downloader")
    root.geometry("700x200")  # 设置窗口初始大小

    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()