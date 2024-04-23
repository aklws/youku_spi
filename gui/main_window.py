import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from logic.youku_downloader import YoukuVideoDownloader

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Youku Video Downloader")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 使用Frame来分组URL输入和下载按钮
        self.url_frame = tk.Frame(self, padx=20, pady=20)
        self.url_frame.pack(fill="x")
        
        self.url_label = tk.Label(self.url_frame, text="请输入 Youku 视频 URL:")
        self.url_label.grid(row=0, column=0, sticky="ew", padx=10)

        self.url_entry = tk.Entry(self.url_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=10)

        self.download_button = tk.Button(self.url_frame, text="获取集数并下载", command=self.download)
        self.download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def download(self):
        url = self.url_entry.get()
        downloader = YoukuVideoDownloader()
        episodes = downloader.download_and_merge(url)
        if episodes:
            self.show_episode_selection(episodes)

    def download_selected_episode(self, episode_info):
        # episode_info 是一个元组，包含了m3u8_url和episode_name
        m3u8_url, episode_name = episode_info
        downloader = YoukuVideoDownloader()
        downloader.download_video_from_m3u8(m3u8_url, "download", episode_name)

    def show_episode_selection(self, episodes):
        selection_window = tk.Toplevel(self.master)
        selection_window.title("选择集数")
        selection_window.geometry("500x400")  # 可以调整大小以适应内容

        scrollbar = ttk.Scrollbar(selection_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(selection_window, yscrollcommand=scrollbar.set, width=50, height=15)
        for episode in episodes:
            # 将m3u8_url和episode_name打包成元组
            self.listbox.insert(tk.END, (episode['url'], episode['name']))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox.yview)

        select_button = tk.Button(selection_window, text="选择并下载", command=lambda: self.download_selected_episode(self.listbox.get(tk.ANCHOR)))
        select_button.pack(pady=10)
