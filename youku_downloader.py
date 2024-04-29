import os
import re
import subprocess
import requests
from tkinter import messagebox


class YoukuVideoDownloader:
    def __init__(self):
        pass

    def download_and_merge(self, url):
        # 创建下载目录
        download_dir = "download"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        match = re.search(r'([^&]+)&', url)
        args='&s1ig=11399&g='
        if match:
            first_param = match.group(1)
            address = first_param + args
            headers = {
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'origin': 'https://m1-z2.cloud.nnpp.vip:2223',
                'priority': 'u=1, i',
                'referer': 'https://m1-z2.cloud.nnpp.vip:2223/',
                'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            }

            response = requests.get(
                f'https://m1-a1.cloud.nnpp.vip:2223/api/v/?z=924269ba54ab81a99a45abc5bab03192&jx={address}',
                headers=headers,
            )
            print(response.text)
            json_data = response.json()
            if 'data' in json_data and len(json_data['data']) > 0:
                episodes = json_data['data'][0]['source']['eps']
                return episodes
            else:
                messagebox.showinfo("错误", "没有找到 URL")
                return None
        else:
            messagebox.showinfo("错误", "没有找到参数")
            return None
    
    def download_video_from_m3u8(self, m3u8_url, download_dir, episode_name):
        # 确保下载目录是一个合法的路径
        download_dir = os.path.normpath(download_dir)
        
        # 创建视频下载目录
        video_dir = os.path.join(download_dir, "videos")
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

        # 使用ffmpeg下载m3u8文件
        print(m3u8_url)
        print(os.path.join(video_dir, f"{episode_name}.mp4"))
        subprocess.run(["ffmpeg", "-i", m3u8_url, os.path.join(video_dir, f"{episode_name}.mp4")])
        messagebox.showinfo("成功", f"视频已下载至: {video_dir}")


