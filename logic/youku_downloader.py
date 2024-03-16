# youku_downloader.py
import os
import re
import subprocess
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class YoukuVideoDownloader:
    def __init__(self):
        pass

    def extract_id_from_url(self, url):
        """从优酷URL中提取视频ID"""
        pattern = r'id_([^\.]+)\.html'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    def merge_videos(self, video_files, output_filename):
        """合并视频文件"""
        # 将视频文件路径写入到一个文本文件中
        with open('input_files.txt', 'w') as f:
            for file in video_files:
                f.write("file '{}'\n".format(file))
        
        print(output_filename)
        # 构建 ffmpeg 命令
        ffmpeg_command = [
            'ffmpeg.exe',      # ffmpeg 可执行文件的路径（假设在当前目录下）
            '-y',                # 覆盖输出文件而不询问
            '-f', 'concat',      # 指定输入文件格式为 concat（连接多个文件）
            '-safe', '0',        # 禁用安全模式，允许使用任意文件名
            '-i', 'input_files.txt',  # 指定包含输入文件列表的文件（每行一个文件名）
            '-c', 'copy',        # 使用 copy 编解码器，快速拷贝视频和音频流而不重新编码
            output_filename      # 输出文件名
        ]

        # 执行ffmpeg命令
        result = subprocess.run(ffmpeg_command, shell=True)


        # 删除临时文本文件
        os.remove('input_files.txt')

        # 删除原始视频文件
        for file in video_files:
            os.remove(file)

    def download_and_merge(self, url, progress_callback):
        # 获取视频 ID
        video_id = self.extract_id_from_url(url)
        if not video_id:
            progress_callback("无法获取视频ID，请检查URL是否正确", "error")
            return

        # 创建下载目录
        download_dir = "download"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # 自定义浏览器位置
        firefox_executable_path = "firefox-1440"

        # 创建 Playwright 的浏览器实例
        with sync_playwright() as p:
            # 设置浏览器启动参数
            browser = p.firefox.launch(headless=True)  # 设置 headless 参数为 True，无头模式
            page = browser.new_page()

            # 打开网页
            page.goto('https://player.youku.com/embed/' + video_id)

            # 等待一段时间，以确保动态内容加载完成
            page.wait_for_timeout(5000)

            # 获取页面的 HTML 内容
            html_content = page.content().encode('utf-8')

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'lxml')

            # 从页面源码中提取mp4链接
            video_divs = soup.find_all('video')
            if video_divs:
                video_files = []
                # 遍历视频标签
                for index, video_div in enumerate(video_divs):
                    mp4_url = video_div.get('src') or video_div.get('data-orginal-src')  # 获取视频链接
                    if mp4_url:
                        response = requests.get(mp4_url, stream=True)
                        total_length = int(response.headers.get('content-length'))
                        filename = os.path.join(download_dir, f"video_{video_id}_{index}.mp4")
                        with open(filename, 'wb') as f:
                            downloaded = 0
                            for chunk in response.iter_content(chunk_size=4096):  # 限制块的大小
                                if chunk:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    progress_callback(downloaded, total_length)

                        video_files.append(filename)

                if video_files:
                    # 合并视频
                    output_filename = os.path.join(download_dir, f"video_{video_id}_merged.mp4")
                    self.merge_videos(video_files, output_filename)
                    progress_callback(f"合并后的视频已保存为 {output_filename}", "success")
                else:
                    progress_callback("没有可用的视频链接，无法合并视频", "error")
            else:
                progress_callback("未找到可用的视频标签或此视频需要VIP", "error")

            # 关闭浏览器
            browser.close()
