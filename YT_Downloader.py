from bs4 import BeautifulSoup
import requests
import threading
from pytube import YouTube
import tkinter as tk
from tkinter import messagebox


def get_urls(url):
    
    urls = []   # 影片清單網址
    if '&list=' not in url: # 判斷是否為單一影片 
        return urls    
    
    response = requests.get(url)    # 發送 GET 請求
    if response.status_code != 200:
        print('request failure')
        return
    
    # 播放清單爬蟲
    bs = BeautifulSoup(response.text, 'lxml')
    a_list = bs.find_all('a')
    base = 'https://www.youtube.com/'        
    
    for a in a_list:
        href = a.get('href')
        url = base + href
        if ('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls


# 下載清單影片的多執行緒函式 threading job
lock = threading.Lock()

def start_download(url, listbox):
    
    yt = YouTube(url)
    name = yt.title
    
    
    lock.acquire()              # lock
    no = listbox.size()     # 下載編號
    listbox.insert(tk.END, f'{no:02d}:{name}.....downloading')
    print('insert:', no, name)
    lock.release()              # release lock
    
    yt.streams.first().download('.//video')   # 開始下載到該目錄下
    
    
    lock.acquire()              # lock
    print('update:', no, name)
    listbox.delete(no)
    listbox.insert(no, f'{no:02d}:●{name}.....finished ')
    lock.release()              # release lock
    

# 按鈕事件
def click_func():
    
    url = yt_url.get()          # 取得文字輸入框的網址
    
    try:    #  pytube 是否支援該網址
        YouTube(url)
    except:
        messagebox.showerror('Error', 'pytube pytybe does not support this video or the URL is wrong')   
        return
    
    # 進行爬蟲
    urls = m.get_urls(url)
    
    # 輸入網址中有影片清單 
    if urls and messagebox.askyesno('Check', 
            'Do you want to downlaod all the videos in the list?') :
        
    # 下載清單中所有影片 
        print('download listt')    
        for u in urls:     # thread建立、啟動
            T = threading.Thread(target = m.start_download, 
                             args=(u, listbox))
            T.start()
   
    # 下載單一影片 
    else:   
        yt = YouTube(url)   
        
        if messagebox.askyesno('Check', 
                               f'Do you want to download {yt.title}？') :
            T = threading.Thread(target = m.start_download, 
                             args=(url, listbox))
            T.start()  
        else:
            print('cancel')
            

# 主視窗
window = tk.Tk()
window.geometry('640x480')         # 主視窗尺寸
window.title('YouTube Downloader')  # 主視窗標題

# Frame：上方輸入網址區域 
input_fm = tk.Frame(window, bg='blue',   # 建立 Frame
                    width=640, height=120)
input_fm.pack()

# Label
lb = tk.Label(input_fm, text='input YouTube URL', 
              bg='blue', fg='white',font=('標楷體', 14))
lb.place(rely=0.25, relx=0.5, anchor='center')

# Entry
yt_url = tk.StringVar()     # 用來取得使用者輸入的網址資料
entry = tk.Entry(input_fm, textvariable=yt_url, width=50)
entry.place(rely=0.5, relx=0.5, anchor='center')

# 下載影片Button
btn = tk.Button(input_fm, text='download', command = click_func, 
                bg='#FFD700', fg='Black',font=('標楷體', 10))
btn.place(rely=0.5, relx=0.85, anchor='center')


# Frame：下方顯示下載清單區域 
dload_fm = tk.Frame(window, width=640, height=480-120)
dload_fm.pack()

# Label
lb = tk.Label(dload_fm, text='download status', 
              fg='black', font=('標楷體', 14))
lb.place(rely=0.1, relx=0.5, anchor='center')

# Listbox
listbox = tk.Listbox(dload_fm, width=65, height=15)
listbox.place(rely=0.5, relx=0.5, anchor='center')

# Scrollbar
sbar = tk.Scrollbar(dload_fm)
sbar.place(rely=0.5, relx=0.87, anchor='center', relheight=0.7)
    
# List 與 Scrollbar 的連結
listbox.config(yscrollcommand = sbar.set)
sbar.config(command = listbox.yview)


window.mainloop()    
    
    