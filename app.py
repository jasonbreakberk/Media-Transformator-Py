import customtkinter as ctk
from tkinter import filedialog
import os
import ffmpeg 
import threading # Arka plan işlemci (Thread) kullanarak arayüzün donmasını engeller

# YENİ KÜTÜPHANE: Font ve İkon Desteği için
from PIL import Image

# Uygulamanın ayarları (Siyah/Gri Profesyonel Tema)
ctk.set_appearance_mode("Dark")  # Koyu Tema
ctk.set_default_color_theme("green") # Aksan rengi olarak yeşili (başarı rengi) kullanıyoruz

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere ayarları
        self.title("Media Transformatör | Dark-Pro")
        self.geometry("650x500") # Boyutu biraz daha büyüttük
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.selected_file_path = None 
        
        # Ekranı bölmek için Ana Çerçeve
        self.main_frame = ctk.CTkFrame(self, fg_color="#2C2C2C")
        self.main_frame.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Başlık
        self.title_label = ctk.CTkLabel(self.main_frame, text="🚀 MEDIA TRANSFORMATÖR", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # ------------------- INPUT FRAME (Dosya Seçme) -------------------
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#3A3A3A")
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.file_path_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Dönüştürülecek Dosyayı Seçin...", width=400, fg_color="#454545")
        # HATA DÜZELTİLDİ: pady=10 eklendi.
        self.file_path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Dosya Seç butonu (Aksan rengi mavi)
        self.select_button = ctk.CTkButton(self.input_frame, text="Dosya Seç", command=self.select_file, fg_color="#3498DB", hover_color="#2980B9")
        # HATA DÜZELTİLDİ: pady=10 eklendi.
        self.select_button.grid(row=0, column=1, padx=10, pady=10)
        
        # ------------------- SEÇENEKLER & İKONLAR -------------------

        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)

        self.format_label = ctk.CTkLabel(self.options_frame, text="İŞLEM SEÇENEKLERİ:", font=ctk.CTkFont(size=14, weight="bold"))
        self.format_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.format_var = ctk.StringVar(value="gif") 

        # Radyo Butonları
        ctk.CTkRadioButton(self.options_frame, text="🎥 Video'dan GIF'e Dönüştür", variable=self.format_var, value="gif").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🎞️ MP4 Boyutunu Küçült (Sıkıştır)", variable=self.format_var, value="mp4_kucult").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🎧 MP3'e Dönüştür (Sesi Çıkar)", variable=self.format_var, value="mp3").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkRadioButton(self.options_frame, text="🖼️ Fotoğraftan GIF Yap (5s Animasyon)", variable=self.format_var, value="single_photo_to_gif").grid(row=4, column=0, padx=20, pady=5, sticky="w") 


        # ------------------- İŞLEM BÖLÜMÜ (İlerleme Çubuğu ve Buton) -------------------

        self.process_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.process_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.process_frame.grid_columnconfigure(0, weight=1)

        # İlerleme Çubuğu
        self.progressbar = ctk.CTkProgressBar(self.process_frame, orientation="horizontal", mode="determinate", progress_color="#2ECC71")
        self.progressbar.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.progressbar.set(0) # Başlangıçta 0

        # Durum Etiketi (Yüzdeyi Gösterecek)
        self.status_label = ctk.CTkLabel(self.process_frame, text="Hazır. Dosyanızı seçin.", text_color="#1ABC9C", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Başlat Butonu
        self.start_button = ctk.CTkButton(self.process_frame, text="DÖNÜŞTÜRMEYİ BAŞLAT", command=self.run_conversion_thread, fg_color="#2ECC71", hover_color="#27AE60", height=40)
        self.start_button.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="ew")

    # ------------------- DOSYA SEÇME FONKSİYONU -------------------

    def select_file(self):
        current_format = self.format_var.get()
        
        # Seçenek fotoğraftan GIF yapma ise, sadece resim dosyalarına izin ver
        if current_format == "single_photo_to_gif":
            file_path = filedialog.askopenfilename(
                title="Dönüştürülecek Fotoğrafı Seçin",
                filetypes=(
                    ("Görüntü Dosyaları", "*.jpg *.png *.jpeg"),
                    ("Tüm Dosyalar", "*.*")
                )
            )
        else:
            # Diğer tüm seçenekler için video seçimine izin ver
            file_path = filedialog.askopenfilename(
                title="Dönüştürülecek Dosyayı Seçin",
                filetypes=(
                    ("Video Dosyaları", "*.mp4 *.mov *.avi *.mkv"),
                    ("Tüm Dosyalar", "*.*")
                )
            )

        if file_path:
            self.file_path_entry.delete(0, 'end')
            self.file_path_entry.insert(0, file_path)
            self.selected_file_path = file_path 
            self.status_label.configure(text=f"'{os.path.basename(file_path)}' hazır.", text_color="#1abc9c")
        else:
            self.status_label.configure(text="Dosya seçimi iptal edildi.", text_color="orange")

    # ------------------- DÖNÜŞTÜRME İŞLEMİNİ ARKA PLANA ATMA -------------------
    
    def run_conversion_thread(self):
        # Arka planda çalışacak bir thread başlatır.
        conversion_thread = threading.Thread(target=self.start_conversion)
        conversion_thread.start()

    # ------------------- DÖNÜŞTÜRME FONKSİYONU (FFMPEG) -------------------
    
    def start_conversion(self):
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            self.status_label.configure(text="Lütfen Önce Geçerli Bir Dosya Seçin!", text_color="red")
            return

        input_file = self.selected_file_path
        output_format = self.format_var.get()
        base, ext = os.path.splitext(input_file)

        # Durum ve Buton Güncelleme
        self.status_label.configure(text="Dönüştürülüyor... Lütfen Bekleyin. %0", text_color="yellow")
        self.progressbar.set(0)
        self.start_button.configure(state="disabled", text="İşleniyor...")

        try:
            output_file = ""
            
            # Basitleştirilmiş statik ilerleme
            self.progressbar.set(0.3)
            self.status_label.configure(text="Dönüştürülüyor... %30", text_color="yellow")

            if output_format == "gif":
                # Video'dan GIF'e dönüştürme
                output_file = base + "_converted.gif"
                stream = ffmpeg.input(input_file)
                stream = ffmpeg.filter(stream, 'fps', fps=15)
                stream.output(output_file, loop=0).run(cmd='ffmpeg', overwrite_output=True)
                
            elif output_format == "mp4_kucult":
                # MP4 sıkıştırma
                output_file = base + "_compressed.mp4"
                stream = ffmpeg.input(input_file)
                stream.output(output_file, crf=28).run(cmd='ffmpeg', overwrite_output=True) 
                
            elif output_format == "mp3":
                # Ses çıkarma
                output_file = base + "_audio.mp3"
                stream = ffmpeg.input(input_file)
                stream.output(output_file, vn=None).run(cmd='ffmpeg', overwrite_output=True)

            elif output_format == "single_photo_to_gif":
                # Tek Fotoğraftan GIF yapma (JPG/PNG destekli)
                output_file = base + "_animated.gif"
                
                (
                    ffmpeg
                    .input(input_file, loop=1) 
                    .output(output_file, t=5, vf='scale=500:-1,format=rgb24') 
                    .run(cmd='ffmpeg', overwrite_output=True)
                )

            # Başarılı Mesajı
            self.progressbar.set(1.0)
            self.status_label.configure(text=f"BAŞARILI! Dosya kaydedildi: {os.path.basename(output_file)}", text_color="green")
            
        except ffmpeg.Error as e:
            # Hata oluştuğunda (FFmpeg hatası)
            self.progressbar.set(0)
            error_message = e.stderr.decode('utf8', errors='ignore')
            self.status_label.configure(text=f"HATA OLUŞTU! Detay: {error_message[:100]}...", text_color="red")

        except AttributeError:
            # Dosya seçilmedi hatası
            self.progressbar.set(0)
            self.status_label.configure(text="Dosya seçilmedi veya geçersiz format seçildi.", text_color="red")

        except Exception as e:
            # Diğer bilinmeyen hatalar
            self.progressbar.set(0)
            self.status_label.configure(text=f"BİLİNMEYEN HATA: {str(e)[:50]}...", text_color="red")
        
        finally:
            # İşlem bittikten sonra butonu tekrar aktif et
            self.start_button.configure(state="normal", text="DÖNÜŞTÜRMEYİ BAŞLAT")
            
# Uygulamayı Çalıştır
if __name__ == "__main__":
    app = App()
    app.mainloop()