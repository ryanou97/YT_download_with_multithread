# YouTube Downloader

YouTube 影片下載器，以 Python 撰寫。使用 tkinter 模組做為操作介面、BeautifulSoup 實現網路爬蟲和 pytube 模組做到Youtube下載估能。可以下載單一影片或是整個播放清單裡的所有影片

## 系統需求
- Python 3.x
- 安裝以下模組：
  ```bash
  pip install requests
  pip install beautifulsoup4
  pip install pytube
  ```

## 如何使用
1. 在終端中執行以下命令：
    ```bash
    python YT_Downloader.py
    ```
2. 在視窗上的輸入框貼上要下載的youtuber網址
3. 按下 "download" 按鈕
    - 如果輸入的是單一影片的 URL，將會啟動一個執行緒進行影片下載。
    - 如果輸入的是包含播放列表的 URL，將會彈出一個確認對話框，詢問是否下載該列表中的所有影片。如果確認，將啟動多個執行緒同時下載所有影片。 
4. 完成下載後，清單框會更新顯示 "finished"。

## 如何運作
該程式使用 pytube 模組實現 youtube 下載的主要功能，輔以 Thinter 模組實現操作介面方便操作，requests 模組做到url get功能，beautifulsoup4 模組做到對播放請單內的影片進行爬蟲，便能下載多個影片。並且用到 multithread 同時處理多個影片，並用到 lock 避免資源不一致或錯誤。

## 備註
可與我的另一個 [Project : mp4_to_mp3]('https://github.com/ryanou97/mp4_to_mp3') 結合，將下載的影片直接轉為 mp3 音樂。

## 聲明
此專案僅以練習為目的，請尊重智慧財產權。
