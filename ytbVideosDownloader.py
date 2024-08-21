import os
import json
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from ttkthemes import ThemedTk
from yt_dlp import YoutubeDL
from threading import Thread

# É necessário baixar o ffmpeg e adotalo como uma variavel de ambiente

# Variável global para controlar o cancelamento
cancel_download_flag = False

# Definindo o caminho absoluto para o config.json
config_path = os.path.join(os.path.expanduser("~"), "config.json")

# Função para lembrar a pasta de destino
def load_last_directory():
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('last_directory', os.getcwd())
    except FileNotFoundError:
        return os.getcwd()

# Função para salvar a pasta de destino
def save_last_directory(directory):
    with open(config_path, 'w') as f:
        json.dump({'last_directory': directory}, f)

# Função para atualizar a barra de progresso
def update_progress(percent):
    progress_var.set(percent)
    progress_bar.update()

# Função para exibir estatísticas de download
def update_stats(d):
    if cancel_download_flag:
        raise Exception("Download cancelado pelo usuário.")

    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', '0B/s')
        eta = d.get('eta', 0)
        percent = re.sub(r'\x1b\[[0-9;]*m', '', percent)  # Remove caracteres de formatação
        stats.set(f"Progresso: {percent}, Velocidade: {speed}, ETA: {eta}s")
        update_progress(float(percent.strip('%')))

# Função para verificar se o vídeo já foi baixado
def is_video_already_downloaded(url, destination):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,  
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', 'mp4')  
            video_path = os.path.join(destination, f"{video_title}.{video_ext}")
            
            if os.path.exists(video_path):
                return True
            return False
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar se o vídeo já foi baixado: {str(e)}")
        return False

# Função para baixar o vídeo completo
def download_video(url, destination):
    global cancel_download_flag
    cancel_download_flag = False  

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
        'ffmpeg_location': 'ffmpeg.exe PATH HERE',
        'progress_hooks': [update_stats],
        'cookies': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        if "Download cancelado pelo usuário." not in str(e):
            messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {str(e)}")
        else:
            messagebox.showinfo("Cancelado", "O download foi cancelado.")

# Função para baixar uma playlist completa
def download_playlist(url, destination):
    global cancel_download_flag
    cancel_download_flag = False  

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
        'ffmpeg_location': 'ffmpeg.exe PATH HERE',
        'progress_hooks': [update_stats],
        'cookies': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'yes_playlist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        if "Download cancelado pelo usuário." not in str(e):
            messagebox.showerror("Erro", f"Erro ao baixar a playlist: {str(e)}")
        else:
            messagebox.showinfo("Cancelado", "O download foi cancelado.")

# Função para iniciar o download do vídeo em uma thread separada
def start_video_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira o link do vídeo.")
        return

    destination = folder_path.get()
    if not destination:
        messagebox.showerror("Erro", "Por favor, escolha a pasta de destino.")
        return

    if is_video_already_downloaded(url, destination):
        messagebox.showinfo("Aviso", "O vídeo já foi baixado na pasta selecionada.")
        return

    save_last_directory(destination)
    download_thread = Thread(target=download_video, args=(url, destination))
    download_thread.start()

# Função para iniciar o download da playlist em uma thread separada
def start_playlist_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira o link da playlist ou vídeo.")
        return

    destination = folder_path.get()
    if not destination:
        messagebox.showerror("Erro", "Por favor, escolha a pasta de destino.")
        return

    # Não faz sentido algum verificar se a playlist inteira já foi baixada, pois ela pode conter vídeos novos
    save_last_directory(destination)
    download_thread = Thread(target=download_playlist, args=(url, destination))
    download_thread.start()

# Função para cancelar o download
def cancel_download():
    global cancel_download_flag
    cancel_download_flag = True  # Ativa o flag de cancelamento

# Função para escolher a pasta de destino
def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

# GUI
root = ThemedTk(theme="scidgreen")
root.title("YouTube Video & Playlist Downloader")
root.configure(bg="#d3d3d3")
icon_image = tk.PhotoImage(file="ytbDownloadVideosIcon.png")  
root.iconphoto(True, icon_image)


url_label = ttk.Label(root, text="Link do Vídeo/Playlist:")
url_label.pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

folder_label = ttk.Label(root, text="Pasta de Destino:")
folder_label.pack(pady=5)
folder_path = tk.StringVar(value=load_last_directory())
folder_entry = ttk.Entry(root, textvariable=folder_path, width=50)
folder_entry.pack(pady=5)

choose_button = ttk.Button(root, text="Escolher Pasta", command=choose_folder)
choose_button.pack(pady=5)

download_video_button = ttk.Button(root, text="Baixar Vídeo", command=start_video_download)
download_video_button.pack(pady=5)

download_playlist_button = ttk.Button(root, text="Baixar Playlist", command=start_playlist_download)
download_playlist_button.pack(pady=5)

cancel_button = ttk.Button(root, text="Cancelar Download", command=cancel_download)
cancel_button.pack(pady=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=10)

stats = tk.StringVar()
stats_label = ttk.Label(root, textvariable=stats)
stats_label.pack(pady=5)

root.mainloop()
