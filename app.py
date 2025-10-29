import customtkinter as ctk
from tkinter import filedialog
import os
import subprocess 
import threading 
import sys 

# Uygulamanın ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# =================================================================================
# KRİTİK FFmpeg YOLU VE BAYRAKLARI
# =================================================================================
def resource_path(relative_path):
    """EXE icindeyken dosyanin (ffmpeg.exe) dogru yolunu bulur."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

FFMPEG_PATH = resource_path("ffmpeg.exe")
# CMD penceresini kesin olarak gizleyen bayrak (Hala en stabil yolumuz)
creation_flags_silent = 0x08000000 
# =================================================================================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere ayarları
        self.title("Media Transformatör | Dark-Pro v1.1.2") # Sürüm numarasını koruyoruz
        self.geometry("650x570")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.selected_file_path = None 
        
        # Arayüz Kurulumu
        self.main_frame = ctk.CTkFrame(self, fg_color="#2C2C2C")
        self.main_frame.grid(row=0, column=0, rowspan=4, padx=20, pady=20, sticky="nsew") 
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="🚀 MEDIA TRANSFORMATÖR", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # ------------------- 1. INPUT FRAME (Dosya Seçme) -------------------
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#3A3A3A")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew") 
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.file_path_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Dönüştürülecek Dosyayı Seçin...", width=400, fg_color="#454545")
        self.file_path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.select_button = ctk.CTkButton(self.input_frame, text="Dosya Seç", command=self.select_file, fg_color="#3498DB", hover_color="#2980B9")
        self.select_button.grid(row=0, column=1, padx=10, pady=10)
        
        # ------------------- 2. KIRPMA ALANI -------------------
        self.trim_frame = ctk.CTkFrame(self.main_frame, fg_color="#3A3A3A")
        self.trim_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew") 
        self.trim_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.trim_label = ctk.CTkLabel(self.trim_frame, text="VİDEO KIRPMA (KLİP) AYARLARI (saniye/hh:mm:ss):", font=ctk.CTkFont(size=12, weight="bold"))
        self.trim_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="w")
        
        self.start_label = ctk.CTkLabel(self.trim_frame, text="Başlangıç (sn):", font=ctk.CTkFont(size=10))
        self.start_label.grid(row=1, column=0, padx=(10, 0), pady=(5, 10), sticky="w")
        self.start_entry = ctk.CTkEntry(self.trim_frame, placeholder_text="0", width=80)
        self.start_entry.grid(row=1, column=1, padx=(0, 10), pady=(5, 10), sticky="ew")

        self.end_label = ctk.CTkLabel(self.trim_frame, text="Bitiş (sn):", font=ctk.CTkFont(size=10))
        self.end_label.grid(row=1, column=2, padx=(10, 0), pady=(5, 10), sticky="w")
        self.end_entry = ctk.CTkEntry(self.trim_frame, placeholder_text="Son", width=80)
        self.end_entry.grid(row=1, column=3, padx=(0, 10), pady=(5, 10), sticky="ew")
        
        # ------------------- 3. SEÇENEKLER & İKONLAR -------------------
        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.options_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)

        self.format_label = ctk.CTkLabel(self.options_frame, text="İŞLEM SEÇENEKLERİ:", font=ctk.CTkFont(size=14, weight="bold"))
        self.format_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.format_var = ctk.StringVar(value="gif") 

        ctk.CTkRadioButton(self.options_frame, text="🎥 Video'dan GIF'e Dönüştür", variable=self.format_var, value="gif").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🎞️ MP4 Boyutunu Küçült (Sıkıştır)", variable=self.format_var, value="mp4_kucult").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🎧 MP3'e Dönüştür (Sesi Çıkar)", variable=self.format_var, value="mp3").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🖼️ Fotoğraftan GIF Yap (5s Animasyon)", variable=self.format_var, value="single_photo_to_gif").grid(row=4, column=0, padx=20, pady=5, sticky="w") 

        # ------------------- 4. İŞLEM BÖLÜMÜ -------------------
        self.process_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.process_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.process_frame.grid_columnconfigure(0, weight=1)

        self.progressbar = ctk.CTkProgressBar(self.process_frame, orientation="horizontal", mode="determinate", progress_color="#2ECC71")
        self.progressbar.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.progressbar.set(0)

        self.status_label = ctk.CTkLabel(self.process_frame, text="Hazır. Dosyanızı seçin.", text_color="#1ABC9C", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.start_button = ctk.CTkButton(self.process_frame, text="DÖNÜŞTÜRMEYİ BAŞLAT", command=self.run_conversion_thread, fg_color="#2ECC71", hover_color="#27AE60", height=40)
        self.start_button.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="ew")

    # ------------------- DOSYA SEÇME FONKSİYONU -------------------
    def select_file(self):
        current_format = self.format_var.get()
        if current_format == "single_photo_to_gif":
            file_path = filedialog.askopenfilename(
                title="Dönüştürülecek Fotoğrafı Seçin",
                filetypes=(("Görüntü Dosyaları", "*.jpg *.png *.jpeg"), ("Tüm Dosyalar", "*.*"))
            )
        else:
            file_path = filedialog.askopenfilename(
                title="Dönüştürülecek Dosyayı Seçin",
                filetypes=(("Video Dosyaları", "*.mp4 *.mov *.avi *.mkv"), ("Tüm Dosyalar", "*.*"))
            )
        
        if file_path:
            self.selected_file_path = file_path 
            
            # UX DÜZELTMESİ: Dosya ismini kısalt 
            file_name_short = os.path.basename(file_path)
            if len(file_name_short) > 30:
                file_name_short = file_name_short[:27] + '...'
            
            self.file_path_entry.delete(0, 'end')
            self.file_path_entry.insert(0, file_path) 
            
            # UX DÜZELTMESİ: Bitiş kutusunu temizle ve placeholder'a bırak
            self.end_entry.delete(0, 'end') 
            
            # Statü mesajını süre okumadan direkt dosya hazır olarak güncelle
            self.status_label.configure(text=f"'{file_name_short}' hazır. (Manuel kırpma ayarlarını girin)", text_color="#1abc9c")
        
        else:
            self.status_label.configure(text="Dosya seçimi iptal edildi.", text_color="orange")

    def run_conversion_thread(self):
        conversion_thread = threading.Thread(target=self.start_conversion)
        conversion_thread.start()

    # =================================================================================
    # DÖNÜŞTÜRME FONKSİYONU (FFMPEG ve SUBPROCESS)
    # =================================================================================
    def start_conversion(self):
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            self.status_label.configure(text="Lütfen Önce Geçerli Bir Dosya Seçin!", text_color="red")
            return

        input_file = self.selected_file_path
        output_format = self.format_var.get()
        base, ext = os.path.splitext(input_file)
        
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        self.status_label.configure(text="Dönüştürülüyor... Lütfen Bekleyin. %0", text_color="yellow")
        self.progressbar.set(0)
        self.start_button.configure(state="disabled", text="İşleniyor...")

        try:
            output_file = ""
            self.progressbar.set(0.3)
            self.status_label.configure(text="Dönüştürülüyor... %30", text_color="yellow")

            # FFMPEG Komut Ayarları
            trim_start_options = []
            trim_end_options = []
            
            # KIRPMA MANTIK KONTROLÜ
            if output_format in ["gif", "mp4_kucult"]:
                if start_time and start_time != '0':
                    trim_start_options += ['-ss', start_time]

                # Bitiş kutusu boşsa, end_time otomatik olarak boş kalır ve FFMPEG videonun sonuna kadar işler.
                if end_time and end_time.lower() not in ['son', '']:
                    trim_end_options += ['-to', end_time]
            
            # Komutun Ana Yapısı: FFMPEG_PATH + BAŞLANGIÇ + INPUT
            final_command = [FFMPEG_PATH] + trim_start_options + ['-i', input_file, '-y']
            
            # FFMPEG Komutlari (Output Formatına Göre Değişir)
            if output_format == "gif":
                output_file = base + "_v1_1_klip.gif"
                final_command += trim_end_options + ['-filter:v', 'fps=15', '-loop', '0', output_file]

            elif output_format == "mp4_kucult":
                output_file = base + "_v1_1_kucuk.mp4"
                final_command += trim_end_options + ['-c:v', 'libx264', '-crf', '28', '-preset', 'medium', output_file]

            elif output_format == "mp3":
                output_file = base + "_v1_1_audio.mp3"
                final_command = [FFMPEG_PATH, '-i', input_file, '-y', '-vn', '-c:a', 'libmp3lame', '-q:a', '2', output_file]

            elif output_format == "single_photo_to_gif":
                output_file = base + "_v1_1_animasyon.gif"
                final_command = [FFMPEG_PATH, '-loop', '1', '-i', input_file, '-y', '-t', '5', '-vf', 'scale=500:-1,format=rgb24', output_file]

            # subprocess ile çalıştırma
            subprocess.run(
                final_command, 
                check=True, 
                shell=True, 
                # CMD penceresi açılıp kapanacak, ama hata vermeyecek.
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.progressbar.set(1.0)
            self.status_label.configure(text=f"BAŞARILI! Dosya kaydedildi: {os.path.basename(output_file)}", text_color="green")
            
        except subprocess.CalledProcessError as e:
            self.progressbar.set(0)
            error_message = e.stderr.decode('utf8', errors='ignore')
            self.status_label.configure(text=f"FFMPEG HATA: {error_message[:100]}...", text_color="red")

        except Exception as e:
            self.progressbar.set(0)
            self.status_label.configure(text=f"BİLİNMEYEN HATA: {str(e)[:50]}...", text_color="red")
        
        finally:
            self.start_button.configure(state="normal", text="DÖNÜŞTÜRMEYİ BAŞLAT")
            
# Uygulamayı Çalıştır
if __name__ == "__main__":
    app = App()
    app.mainloop()