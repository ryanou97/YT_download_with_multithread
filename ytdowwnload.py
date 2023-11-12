from bs4 import BeautifulSoup
import requests
import threading
from pytube import YouTube
import tkinter as tk
import ytube_module as m
from tkinter import messagebox


def get_urls(url):
    
    urls = []   # 影片清單網址
    if '&list=' not in url : return urls    # 單一影片
    response = requests.get(url)    # 發送 GET 請求
    if response.status_code != 200:
        print('請求失敗')
        return
    
    # 請求成功
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
    listbox.insert(tk.END, f'{no:02d}:{name}.....下載中')
    print('插入:', no, name)
    lock.release()              # release lock
    
    yt.streams.first().download('.//video')   # 開始下載到該目錄下
    
    
    lock.acquire()              # lock
    print('更新:', no, name)
    listbox.delete(no)
    listbox.insert(no, f'{no:02d}:●{name}.....下載完成')
    lock.release()              # release lock
    

# 按鈕事件
def click_func():
    
    url = yt_url.get()          # 取得文字輸入框的網址
    
    try:    #  pytube 是否支援該網址
        YouTube(url)
    except:
        messagebox.showerror('錯誤','pytube 不支援此影片或者網址錯誤')   
        return
    
    # 進行爬蟲
    urls = m.get_urls(url)
    
    # 輸入網址中有影片清單 
    if urls and messagebox.askyesno('確認方塊', 
            '是否下載清單內所有影片？(選擇 否(N) 則下載單一影片)') :
        
    # 下載清單中所有影片 
        print('開始下載清單')    
        for u in urls:     # 建立與啟動執行緒
            threading.Thread(target = m.start_download, 
                             args=(u, listbox)).start()
   
    # 下載單一影片 
    else:   
        yt = YouTube(url)   
        if messagebox.askyesno('確認方塊', 
                               f'是否下載{yt.title}影片？') :
            threading.Thread(target = m.start_download, 
                             args=(url, listbox)).start()  
        else:
            print('取消下載')
            

# 主視窗
window = tk.Tk()                   # 建立主視窗物件
window.geometry('640x480')         # 主視窗尺寸
window.title('YouTube Downloader')  # 主視窗標題

# Frame：上方輸入網址區域 
input_fm = tk.Frame(window, bg='blue',   # 建立 Frame
                    width=640, height=120)
input_fm.pack()

# Label
lb = tk.Label(input_fm, text='輸入 YouTube 網址', 
              bg='blue', fg='white',font=('細明體', 12))
lb.place(rely=0.25, relx=0.5, anchor='center')

# Entry
yt_url = tk.StringVar()     # 用來取得使用者輸入的網址資料
entry = tk.Entry(input_fm, textvariable=yt_url, width=50)
entry.place(rely=0.5, relx=0.5, anchor='center')

# Button
btn = tk.Button(input_fm, text='下載影片', command = click_func, 
                bg='#FFD700', fg='Black',font=('細明體', 10))
btn.place(rely=0.5, relx=0.85, anchor='center')


# Frame：下方顯示下載清單區域 
dload_fm = tk.Frame(window, width=640, height=480-120)
dload_fm.pack()

# Label
lb = tk.Label(dload_fm, text='下載狀態', 
              fg='black', font=('細明體', 10))
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
    
    