# youku_spi

一个简单的优酷视频下载器。

## 使用方法

1. 在输入框中输入优酷视频的URL。
2. 点击"下载视频"按钮。
3. 程序将开始下载和合并视频文件。

## 依赖项

- Python 3.12
- PyQt5
- Playwright
- requests
- BeautifulSoup

## 如何使用

1. 克隆该仓库：

```bash
git clone https://github.com/aklws/youku_spi.git
```

进入项目目录：
```bash
cd youku_spi
```
安装依赖项：
```bash
pip install -r requirements.txt
```
如果是通过git获取的源码，需要在根目录下放入ffmpeg的二进制包

使用示例
```python
python main.py
```

## 许可证
这个项目采用 GPLv3.0 许可证。查看 LICENSE 文件了解更多细节。
